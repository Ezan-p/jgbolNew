"""Build the immutable Android backend payload without any player data.

Run with the project's venv so the exact existing Lua parser dependencies can be
vendored. Client APK assets are packaged by the Android build, independently.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESKTOP_MODULES = {'cli.py', 'repair.py', '__main__.py'}
DEPENDENCIES = ('luaparser', 'antlr4-python3-runtime', 'multimethod')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def collect_files(root=ROOT):
    """Map payload-relative names to unchanged, explicit baseline source files."""
    root = Path(root).resolve()
    files = {}

    def add(relative):
        relative = Path(relative)
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Missing or unsafe payload resource: ' + str(relative))
        if path.suffix in ('.sqlite3', '.db', '.pyc') or any(
                part in ('.runtime', 'save', '__pycache__') for part in relative.parts):
            raise ValueError('Player/development data cannot be included: ' + str(relative))
        files[relative.as_posix()] = path

    for path in sorted((root / 'network_redirect').iterdir()):
        if path.suffix in ('.py', '.lua', '.html') and path.name not in DESKTOP_MODULES:
            add(path.relative_to(root))
    for pattern in ('server_config/*.json', 'analysis/configs/**/*.csv'):
        for path in sorted(root.glob(pattern)):
            add(path.relative_to(root))
    for relative in ('analysis/evidence/protocol_tables.json',
                     'analysis/evidence/activity_enums.json',
                     'analysis/evidence/cheer/role_attributes.json',
                     'analysis/server_lists/server_list.raw.txt',
                     'analysis/npc_design/players/catalog.json',
                     'analysis/npc_design/v1/catalog.json',
                     'fetch_server_list.py',
                     'offline_android/__init__.py', 'offline_android/backend.py',
                     'offline_android/tls/ca.pem', 'offline_android/tls/server.pem',
                     'offline_android/tls/server.key'):
        add(relative)

    catalog = json.loads((root / 'analysis/npc_design/players/catalog.json').read_text())
    for entry in catalog['players']:
        relative = Path(entry['source_file'])
        if not relative.is_relative_to('analysis/npc_design') or relative.suffix != '.json':
            raise ValueError('Unexpected NPC snapshot path: ' + str(relative))
        add(relative)
    # Include explicit runtime paths stored in rules, including rank elite data.
    def referenced_paths(value):
        if isinstance(value, dict):
            for item in value.values():
                yield from referenced_paths(item)
        elif isinstance(value, list):
            for item in value:
                yield from referenced_paths(item)
        elif isinstance(value, str) and value.startswith('analysis/'):
            yield value
    for path in sorted((root / 'server_config').glob('*.json')):
        for relative in referenced_paths(json.loads(path.read_text())):
            add(relative)
    return files


def dependency_files():
    """Only pure Python code plus redistribution license/metadata, no host .so."""
    files, versions = {}, {}
    for name in DEPENDENCIES:
        distribution = importlib.metadata.distribution(name)
        versions[name] = distribution.version
        for item in distribution.files or ():
            relative = Path(item)
            if '..' in relative.parts:
                continue
            metadata = any(part.endswith('.dist-info') for part in relative.parts)
            if relative.suffix != '.py' and not (metadata and (
                    relative.name in ('METADATA', 'WHEEL', 'top_level.txt')
                    or 'LICENSE' in relative.name.upper() or 'COPYING' in relative.name.upper())):
                continue
            path = Path(distribution.locate_file(item)).resolve()
            if path.is_file():
                files[relative.as_posix()] = path
    return files, versions


def build_payload(output, root=ROOT):
    """Write a deterministic ZIP; return manifest incl. content-addressed bundle_id.

    The caller embeds this ZIP in assets and extracts it into
    files/program/<bundle_id>. It must never extract into files/save.
    """
    root = Path(root).resolve()
    files = collect_files(root)
    dependencies, versions = dependency_files()
    if set(files) & set(dependencies):
        raise ValueError('Dependency name collides with game payload')
    files.update(dependencies)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from network_redirect.summon import client_source, load_rules
    import network_redirect.summon
    if Path(network_redirect.summon.__file__).resolve().parents[1] != root:
        raise ValueError('Client patch generator was imported from a different baseline')
    login_page = files.pop('network_redirect/login.html').read_text(encoding='utf-8')
    login_page = login_page.replace('若服务未连接，请运行“自动修复登录”。',
                                    '若服务未连接，请关闭游戏后重新打开。')
    login_page = login_page.replace('本地服务连接失败，请运行“自动修复登录”后重试',
                                    '本地服务连接失败，请关闭游戏后重新打开')
    generated = {'offline_client.lua': client_source(load_rules()).encode('utf-8'),
                 'network_redirect/login.html': login_page.encode('utf-8')}
    entries = []
    for name, path in sorted(files.items()):
        data = path.read_bytes()
        entries.append(dict(path=name, size=len(data), sha256=sha256(data), source='baseline'))
    for name, data in generated.items():
        entries.append(dict(path=name, size=len(data), sha256=sha256(data), source='generated'))
    entries.sort(key=lambda entry: entry['path'])
    identity = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    manifest = dict(schema_version=1, bundle_id=sha256(identity), files=entries,
                    dependencies=versions,
                    player_database='files/save/game.sqlite3',
                    loopback_port=18770)
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + '.tmp')

    def write(archive, name, data):
        info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100600 << 16
        archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    try:
        with zipfile.ZipFile(temporary, 'w') as archive:
            checksums = {entry['path']: entry['sha256'] for entry in entries}
            for name, path in sorted(files.items()):
                data = path.read_bytes()
                if sha256(data) != checksums[name]:
                    raise RuntimeError('Source changed while packaging: ' + name)
                write(archive, name, data)
            for name, data in sorted(generated.items()):
                write(archive, name, data)
            write(archive, 'payload-manifest.json',
                  (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest


def verify_payload(directory):
    """Verify the extracted resource tree and its identifier without loading it."""
    directory = Path(directory).resolve()
    manifest = json.loads((directory / 'payload-manifest.json').read_text())
    entries = manifest['files']
    identity = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    if sha256(identity) != manifest['bundle_id']:
        raise ValueError('Payload identifier mismatch')
    seen = set()
    for entry in entries:
        relative = Path(entry['path'])
        path = (directory / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(directory) or relative.as_posix() in seen:
            raise ValueError('Unsafe or duplicate payload entry')
        seen.add(relative.as_posix())
        data = path.read_bytes()
        if len(data) != entry['size'] or sha256(data) != entry['sha256']:
            raise ValueError('Payload integrity mismatch: ' + entry['path'])
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    manifest = build_payload(args.output)
    print(json.dumps(dict(output=str(args.output), bundle_id=manifest['bundle_id'],
                          files=len(manifest['files']),
                          uncompressed_bytes=sum(item['size'] for item in manifest['files'])), indent=2))


if __name__ == '__main__':
    main()
