"""Run the unchanged game backend inside the Android application process.

The Android bootstrap extracts each immutable payload into files/program/<hash>.
Only files/save/game.sqlite3 and files/logs belong to the running game. Replacing
the APK or program payload never initializes, copies over, or deletes that save.
"""
import asyncio
import fcntl
import json
import os
from pathlib import Path
import ssl
import sys
import tempfile
import threading
import time
import traceback

PORT = 18770
_runtime = None
_guard = threading.Lock()


class BundledTLS:
    """The packaged loopback certificate needs no on-device openssl executable."""

    def __init__(self, resource_root):
        directory = Path(resource_root) / 'offline_android/tls'
        self.ca = directory / 'ca.pem'
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.minimum_version = ssl.TLSVersion.TLSv1
        # The original 32-bit game contains OpenSSL with TLS 1.0 support only.
        # TLS is confined to the application host's loopback interface.
        try:
            self.context.set_ciphers('DEFAULT:AES128-SHA:@SECLEVEL=0')
        except ssl.SSLError:
            # The existing macOS development Python uses LibreSSL without the
            # OpenSSL security-level selector. Android CPython uses OpenSSL.
            self.context.set_ciphers('DEFAULT:AES128-SHA')
        self.context.load_cert_chain(directory / 'server.pem', directory / 'server.key')


def local_server_list(resource_root, port):
    """Keep the existing list content, changing only the transport addresses."""
    import re
    data = (Path(resource_root) / 'analysis/server_lists/server_list.raw.txt').read_text(encoding='utf-8-sig')
    data = re.sub(r'(\bip\s*=\s*)"[^"\r\n]*"', r'\1"127.0.0.1"', data)
    data = re.sub(r'(\bport\s*=\s*)\d+', lambda match: match[1] + str(port), data)
    return data.encode('utf-8')


class Runtime:
    def __init__(self, files_dir, resource_root, port):
        self.files_dir = Path(files_dir).resolve()
        self.resource_root = Path(resource_root).resolve()
        self.save_dir = self.files_dir / 'save'
        if self.save_dir == self.resource_root or self.save_dir.is_relative_to(self.resource_root):
            raise ValueError('Player saves must be outside the program payload')
        if not 0 <= port <= 65535:
            raise ValueError('Invalid loopback port')
        self.port = port
        self.ready = threading.Event()
        self.ended = threading.Event()
        self.error = ''
        self.running = False
        self.loop = None
        self.stopped = None
        self.thread = threading.Thread(target=self._thread_main, name='JGBOL-Offline', daemon=True)

    def status(self):
        return dict(ready=self.running, port=self.port, error=self.error,
                    database=str(self.save_dir / 'game.sqlite3'),
                    resource_root=str(self.resource_root),
                    ca_path=str(self.resource_root / 'offline_android/tls/ca.pem'))

    def emit(self, kind, **fields):
        # Bound disk usage and never persist credentials or complete protocol data.
        if kind not in ('offline_ready', 'offline_error', 'offline_stopped',
                        'http_request', 'local_connection_end', 'game_response'):
            return
        log = self.files_dir / 'logs/backend.jsonl'
        try:
            if log.exists() and log.stat().st_size > 512 * 1024:
                log.replace(log.with_suffix('.previous.jsonl'))
            allowed = ('message', 'path', 'status', 'message_id', 'bytes', 'reason')
            record = dict(time=time.time(), kind=kind,
                          **{key: fields[key] for key in allowed if key in fields})
            with log.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(record, ensure_ascii=False) + '\n')
        except OSError:
            pass  # A diagnostic log must never change a game transaction.

    async def _serve(self):
        # Imports happen on the backend thread after its isolated path is set.
        # All SQLite connections stay on this same thread for their full lifetime.
        from network_redirect.accounts import Accounts
        from network_redirect.backend import Backend, login_fields
        from network_redirect.server import LandingServer
        import network_redirect
        actual_root = Path(network_redirect.__file__).resolve().parents[1]
        if actual_root != self.resource_root:
            raise RuntimeError('Backend modules were loaded from a different program payload')
        # ANTLR builds its parser tables on first import. On the original ARM32
        # engine this may exceed the client's login timeout, so complete that
        # unchanged parser initialization before exposing the ready game screen.
        if login_fields('{access_token="offline-bootstrap"}') != {'access_token': 'offline-bootstrap'}:
            raise RuntimeError('Bundled login parser failed its startup check')
        # First bootstrap imports activity modules and builds immutable NPC/data
        # caches. Do this against a disposable database before the client starts
        # its 12-second BS deadline. Never warm against any real player account.
        cache = self.files_dir / 'cache'
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='startup-', dir=cache) as temporary:
            warmup = Backend(Path(temporary), self.port, lambda *args, **kwargs: None,
                             account='android-startup-warmup')
            try:
                warmup.bootstrap()
            finally:
                warmup.close()
        self.loop = asyncio.get_running_loop()
        self.stopped = asyncio.Event()
        backend = Accounts(self.save_dir, self.port, self.emit)
        server = None
        try:
            if backend.db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                raise RuntimeError('Player database integrity check failed; save was not replaced')
            tls = BundledTLS(self.resource_root)
            server = LandingServer(self.port, local_server_list(self.resource_root, self.port),
                                   self.emit, backend=backend, tls=tls)
            await server.start()
            self.port = server.port
            backend.port = backend.base.port = self.port
            server.server_list = local_server_list(self.resource_root, self.port)
            self.running = True
            self.emit('offline_ready', message='Offline game service is ready')
            self.ready.set()
            await self.stopped.wait()
        finally:
            self.running = False
            if server is not None:
                await server.close()
            backend.close()

    def _thread_main(self):
        lock = None
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            self.save_dir.chmod(0o700)
            (self.files_dir / 'logs').mkdir(parents=True, exist_ok=True)
            lock = (self.save_dir / 'service.lock').open('a')
            # An accidental second Android process must not race a running save.
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            sys.dont_write_bytecode = True
            if str(self.resource_root) not in sys.path:
                sys.path.insert(0, str(self.resource_root))
            asyncio.run(self._serve())
        except BaseException:
            self.error = traceback.format_exc()
            self.emit('offline_error', message=self.error)
        finally:
            self.running = False
            if lock is not None:
                lock.close()
            self.ready.set()
            self.ended.set()
            self.emit('offline_stopped')

    def stop(self, timeout=10.0):
        if self.loop and self.stopped and not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self.stopped.set)
        self.thread.join(timeout)
        if self.thread.is_alive():
            raise TimeoutError('Offline game service is still shutting down')


def start(files_dir, resource_root=None, port=PORT, timeout=90.0):
    """Called by the Android bootstrap worker; return only after the listener binds.

    CPython remains initialized for the process lifetime. The native bootstrap
    must release the GIL after this call, and must not call Py_Finalize.
    """
    global _runtime
    resource_root = Path(resource_root) if resource_root else Path(__file__).resolve().parents[1]
    with _guard:
        if _runtime is not None and _runtime.thread.is_alive():
            if (_runtime.files_dir != Path(files_dir).resolve()
                    or _runtime.resource_root != resource_root.resolve()):
                raise RuntimeError('A different offline game instance is already running')
        else:
            _runtime = Runtime(files_dir, resource_root, port)
            _runtime.thread.start()
        runtime = _runtime
    if not runtime.ready.wait(timeout):
        raise TimeoutError('Offline game service did not become ready')
    if not runtime.running:
        runtime.thread.join(timeout=5)
        raise RuntimeError(runtime.error or 'Offline game service stopped during startup')
    return runtime.status()


def status():
    return _runtime.status() if _runtime else dict(ready=False, error='', port=PORT)


def stop(timeout=10.0):
    """For controlled process shutdown and tests, never Activity pause/resume."""
    if _runtime is not None:
        _runtime.stop(timeout)
    return status()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--files-dir', required=True)
    parser.add_argument('--resource-root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--port', type=int, default=PORT)
    args = parser.parse_args()
    print(json.dumps(start(args.files_dir, args.resource_root, args.port)), flush=True)
    try:
        _runtime.ended.wait()
    except KeyboardInterrupt:
        stop()
