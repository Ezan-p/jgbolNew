package com.jgbol.offline;

import android.app.Application;

public final class OfflineApplication extends Application {
    @Override public void onCreate() {
        super.onCreate();
        // LauncherActivity starts the worker. The new-role movie runs only
        // after login, when runtime/resource warm-up has already completed.
    }
}
