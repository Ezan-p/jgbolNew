package com.jgbol.offline;

import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;

/** UI-thread adapter to the game's existing onVideoFinish -> GL/Lua callback. */
public final class NewRoleOpening {
    private static volatile Activity owner;
    private static volatile OpeningVideo player;

    public static boolean active(Activity activity) {
        return owner == activity && player != null;
    }

    public static void play(final Activity activity) {
        if (owner == activity && player != null) return;
        if (owner != null) destroy(owner);
        owner = activity;
        final ViewGroup decor = (ViewGroup) activity.getWindow().getDecorView();
        player = new OpeningVideo(activity, new Runnable() {
            @Override public void run() {
                if (owner != activity || player == null) return;
                decor.removeView(player.getView());
                player = null;
                owner = null;
                try {
                    // The original method queues onVideoFinishedNative on the GL thread.
                    activity.getClass().getMethod("onVideoFinish").invoke(activity);
                } catch (Exception error) {
                    Log.e("JGBOpening", "native completion failed", error);
                }
            }
        });
        decor.addView(player.getView(), new ViewGroup.LayoutParams(-1, -1));
        Log.i("JGBOpening", "new-role playback started");
        player.resume();
    }

    public static void pause(Activity activity) {
        if (owner == activity && player != null) player.pause();
    }
    public static void resume(Activity activity) {
        if (owner == activity && player != null) player.resume();
    }
    public static boolean back(Activity activity, int keyCode) {
        if (keyCode != 4 || owner != activity || player == null) return false;
        player.skip();
        return true;
    }
    public static void destroy(Activity activity) {
        if (owner != activity || player == null) return;
        player.destroy();
        ((ViewGroup) activity.getWindow().getDecorView()).removeView(player.getView());
        player = null;
        owner = null;
    }
}
