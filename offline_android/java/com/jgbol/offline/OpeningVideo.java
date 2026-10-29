package com.jgbol.offline;

import android.app.Activity;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.VideoView;

/** Original bundled movie, once per process; no save files or network access. */
final class OpeningVideo {
    private static boolean seen;
    private final Activity activity;
    private final FrameLayout root;
    private final FrameLayout overlay;
    private final VideoView video;
    private final Handler handler = new Handler();
    private boolean finished, visible, prepared, loading;
    private int position;
    private int lastPosition = -1;
    private int stalled;
    private final Runnable watchdog = new Runnable() {
        @Override public void run() {
            if (!visible || finished) return;
            int current = video.getCurrentPosition();
            stalled = current == lastPosition ? stalled + 1 : 0;
            lastPosition = current;
            if (stalled >= 15) { finish("timeout"); return; }
            handler.postDelayed(this, 1000);
        }
    };

    OpeningVideo(Activity owner, View loadingView, Bundle state) {
        activity = owner;
        finished = seen || (state != null && state.getBoolean("opening.finished"));
        position = state == null ? 0 : state.getInt("opening.position", 0);
        root = new FrameLayout(owner);
        root.addView(loadingView, new FrameLayout.LayoutParams(-1, -1));
        overlay = new FrameLayout(owner);
        overlay.setBackgroundColor(Color.BLACK);
        video = new VideoView(owner);
        overlay.addView(video, new FrameLayout.LayoutParams(-1, -1, Gravity.CENTER));
        Button skip = new Button(owner);
        skip.setText("跳过动画 ›");
        skip.setTextSize(16);
        skip.setTextColor(Color.WHITE);
        skip.setBackgroundColor(0x99502e16);
        FrameLayout.LayoutParams button = new FrameLayout.LayoutParams(dp(126), dp(48), Gravity.RIGHT | Gravity.TOP);
        button.setMargins(dp(16), dp(16), dp(16), dp(16));
        overlay.addView(skip, button);
        skip.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View view) { skip(); }
        });
        if (!finished) root.addView(overlay, new FrameLayout.LayoutParams(-1, -1));
        video.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
            @Override public void onPrepared(MediaPlayer player) {
                if (finished) return;
                prepared = true;
                loading = false;
                player.setLooping(false);
                if (position > 0) video.seekTo(position);
                if (visible) video.start();
                Log.i("JGBOpening", "prepared duration=" + video.getDuration());
            }
        });
        video.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override public void onCompletion(MediaPlayer player) { finish("completed"); }
        });
        video.setOnErrorListener(new MediaPlayer.OnErrorListener() {
            @Override public boolean onError(MediaPlayer player, int what, int extra) {
                finish("error " + what + "/" + extra);
                return true;
            }
        });
    }

    private int dp(int value) { return Math.round(value * activity.getResources().getDisplayMetrics().density); }
    View getView() { return root; }
    boolean isFinished() { return finished; }
    void skip() { finish("skipped"); }

    void resume() {
        visible = true;
        if (finished) return;
        activity.getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        try {
            if (!prepared && !loading) {
                int resource = activity.getResources().getIdentifier("video", "raw", activity.getPackageName());
                if (resource == 0) { finish("missing resource"); return; }
                loading = true;
                video.setVideoURI(Uri.parse("android.resource://" + activity.getPackageName() + "/" + resource));
            }
            if (prepared) {
                if (position > 0) video.seekTo(position);
                video.start();
            }
        } catch (RuntimeException error) {
            finish("exception " + error.getClass().getSimpleName());
            return;
        }
        stalled = 0;
        lastPosition = -1;
        handler.removeCallbacks(watchdog);
        handler.postDelayed(watchdog, 1000);
    }

    void pause() {
        visible = false;
        handler.removeCallbacks(watchdog);
        activity.getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if (!finished) {
            if (prepared) position = video.getCurrentPosition();
            // Release the Surface/decoder on background; recreate and seek on resume.
            prepared = false;
            loading = false;
            video.stopPlayback();
            Log.i("JGBOpening", "paused position=" + position);
        }
    }

    void save(Bundle state) {
        state.putBoolean("opening.finished", finished);
        state.putInt("opening.position", prepared ? video.getCurrentPosition() : position);
    }

    private void finish(String reason) {
        if (finished) return;
        finished = true;
        seen = true;
        handler.removeCallbacks(watchdog);
        video.stopPlayback();
        root.removeView(overlay);
        activity.getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        Log.i("JGBOpening", "finished " + reason);
    }

    void destroy() {
        handler.removeCallbacks(watchdog);
        video.stopPlayback();
    }
}
