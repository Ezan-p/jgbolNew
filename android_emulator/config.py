"""Per-game settings; all paths resolve against the selected JSON file."""
import json
import os
import re
import zipfile
from pathlib import Path

PROFILE_NAMES = ('arm64', 'arm32-software', 'arm32-native')


def load_config(path, *, defaults=None, env_prefix='ANDROID_GAME_'):
    path = Path(path).expanduser().resolve()
    raw = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(raw, dict):
        raise ValueError('配置必须是 JSON 对象')
    return normalize_config({**(defaults or {}), **raw}, path, env_prefix=env_prefix)


def normalize_config(raw, path, *, env_prefix='ANDROID_GAME_'):
    path = Path(path).expanduser().resolve()
    base = path.parent
    config = dict(raw)
    config['config_path'] = path
    config.setdefault('title', '安卓游戏')
    config.setdefault('runtime_profile', 'arm64')
    config.setdefault('runtime_dir', '.runtime')
    config.setdefault('mode', 'emulator')
    config.setdefault('console_port', 5556)
    config.setdefault('grpc_port', 8556)
    config.setdefault('web_port', 8767)
    config.setdefault('serial', 'emulator-' + str(config['console_port']))
    config.setdefault('avd_name', 'android_game')
    config.setdefault('required_abis', None)  # None: inspect APK; []: no native libraries.
    config.setdefault('services', [])
    config.setdefault('ui', {})
    for key in ('mode', 'serial', 'adb_path'):
        if env_prefix + key.upper() in os.environ:
            config[key] = os.environ[env_prefix + key.upper()]
    if config['runtime_profile'] not in PROFILE_NAMES:
        raise ValueError('未知 runtime_profile')
    if config['mode'] not in ('emulator', 'adb'):
        raise ValueError('mode 必须是 emulator 或 adb')
    if not isinstance(config['serial'], str) or not re.fullmatch(r'[A-Za-z0-9_.:-]+', config['serial']):
        raise ValueError('请配置明确的 ADB serial')
    if not isinstance(config['title'], str) or not config['title'].strip():
        raise ValueError('title 必须是非空文本')
    for key in ('package', 'activity', 'avd_name'):
        pattern = r'[A-Za-z0-9_.]+' if key == 'avd_name' else r'[A-Za-z0-9_.$]+'
        if not isinstance(config.get(key), str) or not re.fullmatch(pattern, config[key]):
            raise ValueError('无效配置：' + key)
    for key in ('console_port', 'grpc_port', 'web_port'):
        if type(config[key]) is not int or not 1024 <= config[key] <= 65535:
            raise ValueError('端口必须是 1024—65535 的整数：' + key)
    if not 5554 <= config['console_port'] <= 5682 or config['console_port'] % 2:
        raise ValueError('console_port 必须是 5554—5682 的偶数')
    ports = [config['console_port'], config['console_port'] + 1, config['grpc_port'], config['web_port']]
    if len(set(ports)) != len(ports):
        raise ValueError('安卓控制、ADB、gRPC、网页端口不能重叠')
    if config['mode'] == 'emulator' and config['serial'] != f"emulator-{config['console_port']}":
        raise ValueError('内置模拟器 serial 必须与 console_port 对应')
    def resolve(value):
        return (base / Path(value).expanduser()).resolve()
    config['runtime_dir'] = resolve(config['runtime_dir'])
    config['sdk_path'] = resolve(config.get('sdk_path', config['runtime_dir'] / 'sdk'))
    config['adb_path'] = resolve(config.get('adb_path', config['sdk_path'] / 'platform-tools/adb'))
    # Keep the venv symlink: resolving it selects the system interpreter and loses dependencies.
    config['python_path'] = Path(os.path.abspath(base / Path(config.get('python_path', config['runtime_dir'] / 'venv/bin/python')).expanduser()))
    if 'token_discovery_dir' in config:
        config['token_discovery_dir'] = resolve(config['token_discovery_dir'])
    if config.get('apk'):
        config['apk'] = resolve(config['apk'])
    else:
        config['apk'] = None
    if 'game_root' in config:
        config['game_root'] = resolve(config['game_root'])
    abis = config['required_abis']
    if abis is not None and (not isinstance(abis, list) or any(not isinstance(x, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', x) for x in abis)):
        raise ValueError('required_abis 必须是 ABI 字符串数组或 null')
    if not isinstance(config['ui'], dict) or any(not isinstance(v, str) for v in config['ui'].values()):
        raise ValueError('ui 必须是文本字段对象')
    if not isinstance(config['services'], list):
        raise ValueError('services 必须是数组')
    names = {'emulator', 'gateway'}
    services = []
    for item in config['services']:
        service = dict(item)
        name, port = service.get('name'), service.get('port')
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', name) or name in names:
            raise ValueError('服务名称无效或重复')
        if type(port) is not int or not 1024 <= port <= 65535 or port in ports:
            raise ValueError('服务端口无效或重叠')
        service['script'] = resolve(service['script'])
        names.add(name)
        ports.append(port)
        services.append(service)
    config['services'] = services
    config['component'] = config['package'] + '/' + config['activity']
    return config


def apk_abis(path):
    """Native ABIs actually present in a standalone APK (no manifest rewriting)."""
    with zipfile.ZipFile(path) as archive:
        return sorted({parts[1] for name in archive.namelist()
                       for parts in [name.split('/')]
                       if len(parts) == 3 and parts[0] == 'lib' and parts[2].endswith('.so')})


def required_abis(config, apk=None):
    if apk is not None:
        return apk_abis(apk)
    if config.get('required_abis') is not None:
        return config['required_abis']
    if config.get('apk') and config['apk'].is_file():
        return apk_abis(config['apk'])
    raise RuntimeError('无法确认游戏 ABI：请配置 required_abis 或提供可读取的 APK；纯 Java 游戏使用 []。')


def abi_error(abis, abis32, required):
    supported = set(abis.split(',')) | set(abis32.split(','))
    if required and not supported.intersection(required):
        return ('此设备未声明支持游戏所需的 ABI（需要任一：' + ','.join(required)
                + '；设备：' + (abis or abis32 or '未知') + '）。请使用兼容镜像或 ADB 设备；修改库目录名不能转换原生代码。')
    return None


def device_environment(config):
    runtime, sdk = config['runtime_dir'], config['sdk_path']
    return {**os.environ, 'ANDROID_SDK_ROOT': str(sdk), 'ANDROID_HOME': str(sdk),
            'ANDROID_AVD_HOME': str(runtime / 'avd'),
            'ANDROID_USER_HOME': str(runtime / 'android-user'),
            'ANDROID_EMULATOR_HOME': str(runtime / 'android-user'),
            'PYTHONPYCACHEPREFIX': str(runtime / 'pycache'), 'ANDROID_ADB_SERVER_PORT': '5037'}
