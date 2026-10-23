import asyncio
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, AsyncMock

from aiohttp import ClientSession, CookieJar
from aiohttp.test_utils import TestServer
from android_emulator.config import load_config, normalize_config, abi_error, apk_abis, device_environment
from android_emulator import manager, gateway
from android_emulator.avd import create_avd
from android_emulator.profiles import emulator_command


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.raw = dict(title='Another Game', package='org.example.other', activity='.GameActivity',
                        required_abis=['arm64-v8a'])
        self.config = normalize_config(self.raw, self.root / 'game.json')

    def apk(self, abis):
        path = self.root / 'game.apk'
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('AndroidManifest.xml', b'fixture')
            for abi in abis:
                archive.writestr('lib/' + abi + '/libgame.so', b'library')
            archive.writestr('assets/lib/armeabi/decoy.so', b'asset')
        return path

    def test_config_paths_are_relative_to_json_not_cwd(self):
        path = self.root / 'games/second/game.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({**self.raw, 'runtime_dir': '../../data/second', 'apk': 'game.apk'}))
        cfg = load_config(path)
        self.assertEqual(cfg['runtime_dir'], self.root / 'data/second')
        self.assertEqual(cfg['apk'], path.parent / 'game.apk')
        self.assertEqual(cfg['component'], 'org.example.other/.GameActivity')

    def test_python_venv_symlink_is_preserved(self):
        python = self.root / 'venv/bin/python'
        python.parent.mkdir(parents=True)
        python.symlink_to(sys.executable)
        cfg = normalize_config({**self.raw, 'python_path': 'venv/bin/python'}, self.root / 'game.json')
        self.assertEqual(cfg['python_path'], python)
        self.assertNotEqual(cfg['python_path'], python.resolve())

    def test_environment_and_commands_are_isolated(self):
        other = normalize_config({**self.raw, 'runtime_dir': 'other', 'avd_name': 'second',
                                  'console_port': 5562}, self.root / 'second.json')
        self.assertNotEqual(manager.Manager(other).state_path, manager.Manager(self.config).state_path)
        self.assertNotEqual(device_environment(other)['ANDROID_AVD_HOME'], device_environment(self.config)['ANDROID_AVD_HOME'])
        command = emulator_command(other)
        self.assertIn('second', command)
        self.assertIn('5562', command)
        self.assertEqual(command[0], str(other['sdk_path'] / 'emulator/emulator'))

    def test_env_overrides_and_legacy_prefix_do_not_leak(self):
        with patch.dict(os.environ, {'ANDROID_GAME_MODE': 'adb', 'ANDROID_GAME_SERIAL': 'usb-test',
                                     'JGB_SERIAL': 'wrong-device'}):
            cfg = normalize_config(self.raw, self.root / 'game.json')
        self.assertEqual(cfg['mode'], 'adb')
        self.assertEqual(cfg['serial'], 'usb-test')

    def test_invalid_ports_serial_and_service_collision(self):
        for change in [{'web_port': 5557}, {'console_port': 5557}, {'serial': 'emulator-5580'},
                       {'serial': '$(bad)'}, {'package': 'bad;command'}, {'required_abis': 'armeabi'},
                       {'services': [dict(name='api', port=8767, script='api.py')]}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                normalize_config({**self.raw, **change}, self.root / 'game.json')

    def test_abi_check_supports_multiple_games_and_java_only(self):
        self.assertIsNone(abi_error('arm64-v8a', '', ['arm64-v8a']))
        self.assertIsNone(abi_error('x86_64,x86', '', ['armeabi-v7a', 'x86']))
        self.assertIsNone(abi_error('x86', '', []))
        self.assertIsNotNone(abi_error('arm64-v8a,armeabi-v7a', '', ['armeabi']))
        self.assertEqual(apk_abis(self.apk(['arm64-v8a', 'x86_64'])), ['arm64-v8a', 'x86_64'])
        self.assertEqual(apk_abis(self.apk([])), [])

    def test_unknown_abi_is_not_silently_accepted(self):
        from android_emulator.config import required_abis
        with self.assertRaisesRegex(RuntimeError, '无法确认'):
            required_abis({**self.config, 'required_abis': None})

    def test_install_checks_actual_override_apk_before_touching_device(self):
        apk = self.apk(['armeabi'])
        cfg = {**self.config, 'mode': 'adb'}
        cfg['adb_path'].parent.mkdir(parents=True)
        cfg['adb_path'].touch()
        outputs = ['device', 'arm64-v8a', '', '1', '11']
        with patch.object(manager, 'adb', side_effect=outputs) as adb:
            with self.assertRaisesRegex(RuntimeError, 'armeabi'):
                manager.Manager(cfg).install(apk)
            self.assertFalse(any(call.args[1] == 'install' for call in adb.call_args_list))

    def test_install_launches_configured_game_without_resigning(self):
        apk = self.apk(['arm64-v8a'])
        with patch.object(manager, 'ready_device') as ready, patch.object(manager, 'adb', return_value='Success') as adb:
            manager.Manager(self.config).install(apk)
        self.assertEqual(ready.call_args_list[0].kwargs['apk'], apk)
        self.assertEqual(adb.call_args_list[0].args[1:], ('install', '--no-streaming', '-r', str(apk)))
        self.assertEqual(adb.call_args_list[1].args[-1], 'org.example.other/.GameActivity')

    def test_avd_creation_is_configured_and_preserves_existing_data(self):
        image = self.root / 'image'
        image.mkdir()
        (image / 'system.img').touch()
        from android_emulator.profiles import profiles_for
        profiles = profiles_for(self.config)
        profiles['arm64']['image'] = image
        create_avd(self.config, profiles=profiles)
        path = self.config['runtime_dir'] / 'avd/android_game.avd/config.ini'
        original = path.read_bytes()
        self.assertIn(b'abi.type=arm64-v8a', original)
        self.assertNotIn('金箍棒', original.decode())
        with self.assertRaisesRegex(RuntimeError, '已存在'):
            create_avd(self.config, profiles=profiles)
        self.assertEqual(path.read_bytes(), original)

    def test_stop_does_not_kill_external_adb_emulator(self):
        runtime = manager.Manager({**self.config, 'mode': 'adb'})
        runtime.write_state({'emulator': 4321})
        with patch.object(runtime, 'owned_pid', return_value=True), patch.object(manager.os, 'kill') as kill:
            runtime.stop()
        kill.assert_not_called()
        self.assertEqual(runtime.read_state(), {'emulator': 4321})

    def test_process_identity_requires_selected_avd_and_port(self):
        runtime = manager.Manager(self.config)
        command = emulator_command(self.config)
        for changed in [command, [x if x != 'android_game' else 'different_game' for x in command],
                        [x if x != '5556' else '5560' for x in command]]:
            with patch.object(manager.subprocess, 'run', return_value=SimpleNamespace(stdout=' '.join(changed))):
                self.assertEqual(runtime.owned_pid('emulator', 12345), changed == command)

    def test_busy_foreign_port_is_not_taken_over(self):
        runtime = manager.Manager({**self.config, 'python_path': Path(sys.executable)})
        with patch.object(manager, 'listening', return_value=True), patch.object(manager.subprocess, 'Popen') as spawn:
            with self.assertRaisesRegex(RuntimeError, '拒绝接管'):
                runtime.start()
        spawn.assert_not_called()

    def test_runtime_archives_install_in_configured_directory(self):
        import hashlib
        import tarfile
        from android_emulator.runtime_setup import setup_runtime
        runtime = self.config['runtime_dir']
        runtime.mkdir()
        indexes = {'repository.xml': [], 'images.xml': []}
        fixtures = [
            ('platform-tools.zip', 'repository.xml', 'platform-tools', 'platform-tools/adb'),
            ('build-tools.zip', 'repository.xml', 'build-tools;35.0.0', 'android-15/zipalign'),
            ('emulator.zip', 'repository.xml', 'emulator', 'emulator/lib/emulator_controller.proto'),
            ('image.zip', 'images.xml', 'system-images;android-30;google_apis;arm64-v8a', 'arm64-v8a/system.img')]
        for archive, index, package, member in fixtures:
            path = runtime / archive
            with zipfile.ZipFile(path, 'w') as bundle:
                bundle.writestr(member, b'fixture')
            checksum = hashlib.sha1(path.read_bytes()).hexdigest()
            indexes[index].append(f'<remotePackage path="{package}"><archives><archive><complete>'
                                  f'<checksum>{checksum}</checksum><url>{archive}</url>'
                                  '</complete></archive></archives></remotePackage>')
        for index, entries in indexes.items():
            (runtime / index).write_text('<repository>' + ''.join(entries) + '</repository>')
        with tarfile.open(runtime / 'jdk.tar.gz', 'w:gz') as bundle:
            entry = tarfile.TarInfo('jdk/Contents/Home/bin/java')
            entry.size = 7
            bundle.addfile(entry, io.BytesIO(b'fixture'))
        setup_runtime(self.config)
        self.assertTrue((self.config['sdk_path'] / 'platform-tools/adb').is_file())
        self.assertTrue((self.config['sdk_path'] / 'build-tools/35.0.0/zipalign').is_file())
        self.assertTrue((runtime / 'java/jdk/Contents/Home/bin/java').is_file())
        self.assertEqual(len(json.loads((runtime / 'downloads.json').read_text())), 4)
        self.assertEqual((runtime / 'emulator_controller.proto').read_bytes(), b'fixture')

    def test_copied_module_is_independent_of_original_project(self):
        source = Path(__file__).resolve().parents[1]
        copy = self.root / 'isolated/android_emulator'
        shutil.copytree(source, copy, ignore=shutil.ignore_patterns('__pycache__', '.runtime', 'tests'))
        cfg = copy.parent / 'game.json'
        cfg.write_text(json.dumps(self.raw))
        result = subprocess.run([sys.executable, str(copy / 'run.py'), '--config', str(cfg), 'doctor'],
                                cwd=copy.parent, capture_output=True, text=True,
                                env={k: v for k, v in os.environ.items() if k != 'PYTHONPATH'})
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['game'], 'Another Game')
        self.assertIn('未找到 ADB', report['device_error'])
        # Protocol and assets also import without the legacy project on sys.path.
        result = subprocess.run([sys.executable, '-c',
                                 'from android_emulator.config import load_config; '
                                 'from android_emulator.gateway import make_app; '
                                 'app=make_app(load_config("game.json")); print(app["config"]["title"])'],
                                cwd=copy.parent, capture_output=True, text=True,
                                env={k: v for k, v in os.environ.items() if k != 'PYTHONPATH'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Another Game', result.stdout)


class GatewayIsolationTests(unittest.IsolatedAsyncioTestCase):
    async def test_two_games_have_separate_branding_sessions_and_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            configs = [normalize_config(dict(title=title, package='org.example.' + name, activity='.Main',
                                            required_abis=[], mode='adb', serial=name, runtime_dir=name),
                                        Path(tmp) / (name + '.json'))
                       for name, title in [('one', '游戏 A'), ('two', '<script>alert(1)</script>')]]
            async with contextlib.AsyncExitStack() as stack:
                servers, clients = [], []
                for cfg in configs:
                    app = gateway.make_app(cfg)
                    app.cleanup_ctx.clear()
                    app['stub'] = SimpleNamespace(getStatus=AsyncMock(return_value=SimpleNamespace(version='test')))
                    srv = await stack.enter_async_context(TestServer(app))
                    client = await stack.enter_async_context(ClientSession(cookie_jar=CookieJar(unsafe=True)))
                    servers.append(srv)
                    clients.append(client)
                    response = await client.get(srv.make_url('/'))
                    text = await response.text()
                    self.assertNotIn('<script>alert(1)</script>', text)
                    self.assertNotIn('金箍棒', text)
                    self.assertIn('游戏 A' if cfg == configs[0] else '&lt;script&gt;', text)
                    self.assertEqual((await client.get(srv.make_url('/app.js'))).status, 200)
                    self.assertEqual((await client.get(srv.make_url('/style.css'))).status, 200)
                    with patch.object(gateway, 'device_info', AsyncMock(return_value={'issue': None})):
                        payload = await (await client.get(srv.make_url('/api/status'))).json()
                    self.assertEqual(payload['package'], cfg['package'])
                    self.assertEqual(payload['ui']['title'], cfg['title'])
                self.assertNotEqual(servers[0].app['session'], servers[1].app['session'])
                self.assertNotEqual(servers[0].app['cookie_name'], servers[1].app['cookie_name'])
                # Cookies are shared across ports in a browser; loading game two must
                # not invalidate the session established for game one.
                await clients[0].get(servers[1].make_url('/'))
                with patch.object(gateway, 'device_info', AsyncMock(return_value={'issue': None})):
                    response = await clients[0].get(servers[0].make_url('/api/status'))
                    self.assertEqual(response.status, 200)
                # A cookie from another game must not authorize access.
                async with ClientSession() as stranger:
                    response = await stranger.get(servers[1].make_url('/api/status'),
                                                  cookies={servers[1].app['cookie_name']: servers[0].app['session']})
                    self.assertEqual(response.status, 401)

    async def test_failure_still_reports_game_branding(self):
        cfg = normalize_config(dict(title='Offline Game', package='org.example.offline', activity='.Main',
                                    required_abis=[], mode='adb', serial='usb'), Path('/tmp/offline/game.json'))
        app = gateway.make_app(cfg)
        app.cleanup_ctx.clear()
        app['stub'] = SimpleNamespace(getStatus=AsyncMock(side_effect=RuntimeError('设备离线')))
        response = await gateway.status(SimpleNamespace(app=app))
        payload = json.loads(response.text)
        self.assertEqual(payload['ui']['title'], 'Offline Game')
        self.assertFalse(payload['emulator'])
        self.assertIn('设备离线', payload['message'])


if __name__ == '__main__':
    unittest.main()
