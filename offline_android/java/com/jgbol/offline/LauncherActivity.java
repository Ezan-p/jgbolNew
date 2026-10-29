package com.jgbol.offline;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.content.Intent;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.ProgressBar;

public final class LauncherActivity extends Activity {
    private final Handler handler = new Handler();
    private TextView detail;
    private ProgressBar progress;
    private boolean visible;
    private boolean launched;
    private OpeningVideo opening;
    private final Runnable check = new Runnable() {
        @Override public void run() {
            if (isFinishing() || !visible || launched) return;
            if (opening.isFinished()) OfflineRuntime.begin(getApplicationContext());
            if (OfflineRuntime.error != null) {
                progress.setVisibility(android.view.View.GONE);
                detail.setText("启动未完成\n" + OfflineRuntime.error + "\n\n请关闭游戏后重试。存档保留在本机。");
            } else if (OfflineRuntime.ready && opening.isFinished()) {
                launched = true;
                Intent game = new Intent();
                game.setClassName(getPackageName(), "com.sygame.jingubang.uc.xiyoujilua");
                startActivity(game);
                finish();
            } else {
                detail.setText(OfflineRuntime.ready ? "准备就绪" : OfflineRuntime.message);
                handler.postDelayed(this, 200);
            }
        }
    };

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setPadding(40, 30, 40, 30);
        layout.setBackgroundColor(Color.rgb(23, 18, 15));
        TextView title = new TextView(this);
        title.setText("金箍棒 · 离线单机");
        title.setTextColor(Color.rgb(243, 211, 146));
        title.setTextSize(27);
        title.setGravity(Gravity.CENTER);
        layout.addView(title);
        progress = new ProgressBar(this);
        LinearLayout.LayoutParams pp = new LinearLayout.LayoutParams(50, 50);
        pp.setMargins(0, 24, 0, 24);
        layout.addView(progress, pp);
        detail = new TextView(this);
        detail.setTextColor(Color.WHITE);
        detail.setTextSize(16);
        detail.setGravity(Gravity.CENTER);
        layout.addView(detail);
        opening = new OpeningVideo(this, layout, state);
        setContentView(opening.getView());
    }

    @Override protected void onResume() {
        super.onResume();
        visible = true;
        opening.resume();
        handler.post(check);
    }

    @Override protected void onPause() {
        visible = false;
        opening.pause();
        handler.removeCallbacks(check);
        super.onPause();
    }

    @Override protected void onDestroy() {
        handler.removeCallbacks(check);
        opening.destroy();
        super.onDestroy();
    }

    @Override protected void onSaveInstanceState(Bundle state) {
        opening.save(state);
        super.onSaveInstanceState(state);
    }

    @Override public void onBackPressed() {
        if (!opening.isFinished()) opening.skip();
        else super.onBackPressed();
    }
}
