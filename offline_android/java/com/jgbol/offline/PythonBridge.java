package com.jgbol.offline;

public final class PythonBridge {
    public static native String start(String filesDir, String programRoot, String pythonRoot);
}
