"""Matched emulator engines and Android images; CPU architecture is not a label."""
from .config import device_environment

def profiles_for(config):
    RUNTIME, SDK = config["runtime_dir"], config["sdk_path"]
    return {
        "arm64": {
            "emulator": SDK / "emulator/emulator",
            "image": SDK / "system-images/android-30/google_apis/arm64-v8a",
            "api": 30, "abi": "arm64-v8a", "arch": "arm64", "tag": "google_apis",
            "memory": 4096, "cores": 4, "gpu": "host", "width": 1280, "height": 720,
            "density": 240, "extra": ["-no-metrics"],
        },
        "arm32-software": {
            "emulator": RUNTIME / "compat32/emulator/emulator",
            "image": SDK / "system-images/android-23/default/armeabi-v7a",
            "api": 23, "abi": "armeabi-v7a", "arch": "arm", "tag": "default",
            "memory": 1536, "cores": 1, "gpu": "swiftshader_indirect",
            "width": 960, "height": 540, "density": 160,
            "extra": ["-accel", "off"],
        },
        "arm32-native": {
            "emulator": RUNTIME / "compat32/native-engine/qemu-system-armel-headless",
            "image": SDK / "system-images/android-23/default/armeabi-v7a",
            "api": 23, "abi": "armeabi-v7a", "arch": "arm", "tag": "default",
            "memory": 1536, "cores": 1, "gpu": "host",
            "width": 960, "height": 540, "density": 160,
            # CoreAudio input can deadlock the ARM32 engine's main loop on macOS.
            "extra": ["-accel", "off", "-no-metrics", "-audio", "none"],
        },
    }


def profile_for(config):
    return profiles_for(config)[config.get("runtime_profile", "arm64")]


def emulator_environment(config):
    env = device_environment(config)
    if config.get("runtime_profile") == "arm32-native":
        env["ANDROID_EMULATOR_LAUNCHER_DIR"] = str(config["sdk_path"] / "emulator")
        env["ANDROID_EMU_ENABLE_CRASH_REPORTING"] = "0"
    return env


def emulator_command(config, dns=None):
    dns = dns or config.get("dns", "8.8.8.8,1.1.1.1")
    profile = profile_for(config)
    return [
        str(profile["emulator"]), "-avd", config["avd_name"],
        "-port", str(config["console_port"]), "-grpc", str(config["grpc_port"]),
        "-grpc-use-token", "-no-window", "-no-snapshot", "-no-boot-anim",
        "-gpu", profile["gpu"], "-memory", str(profile["memory"]),
        "-cores", str(profile["cores"]), "-dns-server", dns,
        *profile["extra"],
    ]
