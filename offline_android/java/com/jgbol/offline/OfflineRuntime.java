package com.jgbol.offline;

import android.content.Context;
import android.content.Intent;
import android.app.Activity;
import android.os.Looper;
import android.util.Log;
import java.util.Properties;
import java.io.*;
import java.security.MessageDigest;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

/** Immutable versioned program files and runtime; never extracts into save/. */
public final class OfflineRuntime {
    public static volatile boolean ready;
    public static volatile String error;
    public static volatile String message = "正在准备本地游戏，首次启动需要解包资源…";
    private static boolean started;
    private static final CountDownLatch completion = new CountDownLatch(1);

    public static synchronized void begin(final Context context) {
        if (started) return;
        started = true;
        new Thread(new Runnable() {
            @Override public void run() {
                try {
                    Properties meta = new Properties();
                    InputStream metadata = context.getAssets().open("offline/build.properties");
                    try { meta.load(metadata); } finally { metadata.close(); }
                    File files = context.getFilesDir();
                    File program = extract(context, files, "program", meta.getProperty("program_sha256"));
                    File python = extract(context, files, "runtime", meta.getProperty("runtime_sha256"));
                    installClientOverlay(context, program, meta.getProperty("program_sha256"));
                    message = "正在启动本地服务…";
                    System.loadLibrary("python_bootstrap");
                    String result = PythonBridge.start(files.getAbsolutePath(), program.getAbsolutePath(), python.getAbsolutePath());
                    Log.i("JGBOffline", "Python ready: " + result);
                    message = "正在载入游戏…";
                    System.loadLibrary("xiyoujilua");
                    System.loadLibrary("pocketsphinx_jni");
                    System.loadLibrary("offline");
                    NativeBridge.install(program.getAbsolutePath(), new File(program, "offline_android/tls/ca.pem").getAbsolutePath());
                    ready = true;
                    Log.i("JGBOffline", "OFFLINE_READY " + meta.getProperty("program_sha256"));
                } catch (Throwable problem) {
                    Log.e("JGBOffline", "Offline startup failed", problem);
                    error = problem.toString();
                } finally {
                    completion.countDown();
                }
            }
        }, "JGBOfflineStartup").start();
    }

    /** Worker-thread helper only. Restored Activities use relaunch instead. */
    public static void awaitReady() {
        if (Looper.myLooper() == Looper.getMainLooper()) {
            throw new IllegalStateException("Do not wait for the offline backend on the UI thread");
        }
        try {
            if (!completion.await(90, TimeUnit.SECONDS)) throw new IllegalStateException("本地服务启动超时");
            if (!ready) throw new IllegalStateException(error);
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(interrupted);
        }
    }

    /** Return a process-restored, uninitialized game Activity to the async gate. */
    public static void relaunch(Activity activity) {
        Log.i("JGBOffline", "RESTORE_REDIRECT: waiting in LauncherActivity");
        Intent launcher = new Intent(activity, LauncherActivity.class);
        launcher.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        activity.startActivity(launcher);
        activity.finish();
    }

    private static String read(InputStream source) throws IOException {
        try {
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            copy(source, output);
            return output.toString("UTF-8");
        } finally { source.close(); }
    }

    private static void copy(InputStream source, OutputStream output) throws IOException {
        byte[] buffer = new byte[65536];
        int count;
        while ((count = source.read(buffer)) != -1) output.write(buffer, 0, count);
    }

    private static String hex(byte[] value) {
        StringBuilder result = new StringBuilder();
        for (byte item : value) result.append(String.format("%02x", item & 255));
        return result.toString();
    }

    private static File extract(Context context, File files, String kind, String digest) throws Exception {
        if (!digest.matches("[0-9a-f]{64}")) throw new IOException("Invalid bundle hash");
        File parent = new File(files, kind);
        File destination = new File(parent, digest);
        File marker = new File(destination, ".complete");
        if (marker.isFile() && read(new FileInputStream(marker)).equals(digest)) return destination;
        if (!parent.isDirectory() && !parent.mkdirs()) throw new IOException("Cannot create " + kind);
        File archive = new File(parent, digest + ".zip.tmp");
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        InputStream input = context.getAssets().open("offline/" + kind + ".zip");
        FileOutputStream output = new FileOutputStream(archive);
        try {
            byte[] buffer = new byte[65536];
            int count;
            while ((count = input.read(buffer)) != -1) { sha.update(buffer, 0, count); output.write(buffer, 0, count); }
            output.getFD().sync();
        } finally { output.close(); input.close(); }
        if (!hex(sha.digest()).equals(digest)) throw new IOException("离线资源校验失败");
        File staging = new File(parent, digest + ".staging");
        removeTree(staging);
        if (!staging.mkdirs()) throw new IOException("Cannot create staging directory");
        String prefix = staging.getCanonicalPath() + File.separator;
        ZipInputStream zip = new ZipInputStream(new FileInputStream(archive));
        try {
            ZipEntry entry;
            while ((entry = zip.getNextEntry()) != null) {
                File file = new File(staging, entry.getName());
                if (!file.getCanonicalPath().startsWith(prefix)) throw new IOException("Invalid resource path");
                if (entry.isDirectory()) { file.mkdirs(); continue; }
                file.getParentFile().mkdirs();
                FileOutputStream stream = new FileOutputStream(file);
                try { copy(zip, stream); } finally { stream.close(); }
            }
        } finally { zip.close(); }
        FileOutputStream seal = new FileOutputStream(new File(staging, ".complete"));
        try { seal.write(digest.getBytes("UTF-8")); seal.getFD().sync(); } finally { seal.close(); }
        removeTree(destination);
        if (!staging.renameTo(destination)) throw new IOException("Cannot publish program files");
        archive.delete();
        return destination;
    }

    private static void installClientOverlay(Context context, File program, String digest) throws IOException {
        File source = new File(program, "client/release_w");
        if (!source.isDirectory()) return;
        File data = new File(context.getApplicationInfo().dataDir);
        File target = new File(data, "release_w");
        File marker = new File(target, ".offline-version");
        if (marker.isFile() && read(new FileInputStream(marker)).equals(digest)) return;
        File staging = new File(data, "release_w.offline-staging");
        File previous = new File(data, "release_w.offline-previous");
        removeTree(staging);
        copyTree(source, staging);
        FileOutputStream seal = new FileOutputStream(new File(staging, ".offline-version"));
        try { seal.write(digest.getBytes("UTF-8")); seal.getFD().sync(); } finally { seal.close(); }
        removeTree(previous);
        if (target.exists() && !target.renameTo(previous)) throw new IOException("Cannot stage client update");
        if (!staging.renameTo(target)) {
            previous.renameTo(target);
            throw new IOException("Cannot publish client update");
        }
        removeTree(previous);
    }

    private static void copyTree(File from, File to) throws IOException {
        if (from.isDirectory()) {
            if (!to.mkdirs() && !to.isDirectory()) throw new IOException("Cannot create directory");
            File[] entries = from.listFiles();
            if (entries == null) throw new IOException("Cannot read program directory");
            for (File child : entries) copyTree(child, new File(to, child.getName()));
        } else {
            FileInputStream input = new FileInputStream(from);
            FileOutputStream output = new FileOutputStream(to);
            try { copy(input, output); } finally { output.close(); input.close(); }
        }
    }

    private static void removeTree(File file) throws IOException {
        if (!file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children == null) throw new IOException("Cannot inspect program directory");
            for (File child : children) removeTree(child);
        }
        if (!file.delete()) throw new IOException("Cannot replace program resource");
    }
}
