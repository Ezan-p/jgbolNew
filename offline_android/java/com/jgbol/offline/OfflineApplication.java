package com.jgbol.offline;

import android.app.Application;

public final class OfflineApplication extends Application {
    @Override public void onCreate() {
        super.onCreate();
        // LauncherActivity starts the worker after the movie. Competing with
        // Python/resource warm-up can starve software video decoding on ARM32.
    }
}
