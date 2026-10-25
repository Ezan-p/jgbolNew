"""Loopback-only HTTP/TLS/game listener; optional explicit local-account backend."""
import asyncio
import hashlib
import json
import secrets
from pathlib import Path
from http.cookies import SimpleCookie, CookieError
import struct
import time
import uuid
from urllib.parse import urlsplit

from .protocol import HEADER, MAX_PACKET
from .tls import TLSStream

HEALTH = b'JGBOL_LOCAL_REDIRECT_OK\n'
LIST_PATHS = {'/update/jgb/p360_a/server_list.txt', '/update/jgb/p360_na/server_list.txt'}


class _ConnectionStream:
    """Count raw socket bytes consumed/queued, including TLS records."""

    def __init__(self, reader, writer):
        self.reader, self.writer = reader, writer
        self.read_bytes = self.written_bytes = 0

    async def _read(self, method, *args):
        try:
            data = await getattr(self.reader, method)(*args)
        except asyncio.IncompleteReadError as exc:
            self.read_bytes += len(exc.partial)
            raise
        self.read_bytes += len(data)
        return data

    async def read(self, size):
        return await self._read('read', size)

    async def readexactly(self, size):
        return await self._read('readexactly', size)

    async def readuntil(self, separator):
        return await self._read('readuntil', separator)

    def write(self, data):
        self.writer.write(data)
        self.written_bytes += len(data)

    async def drain(self):
        await self.writer.drain()


class LandingServer:
    def __init__(self, port, server_list, emit, *, backend=None, tls=None):
        self.port, self.server_list, self.emit = port, server_list, emit
        self.server = None
        self.tasks = set()
        self.backend, self.tls = backend, tls

    async def start(self):
        self.server = await asyncio.start_server(self.handle, '127.0.0.1', self.port, limit=16384)
        self.port = self.server.sockets[0].getsockname()[1]

    async def close(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for task in list(self.tasks):
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def handle(self, reader, writer):
        task = asyncio.current_task()
        self.tasks.add(task)
        peer = writer.get_extra_info('peername')
        connection_id = uuid.uuid4().hex[:12]
        started = time.monotonic()
        traffic = _ConnectionStream(reader, writer)
        reader = traffic
        end_reason = 'completed'

        def emit(kind, **fields):
            self.emit(kind, connection_id=connection_id, peer=str(peer), **fields)

        emit('local_accept', message=f'连接 {connection_id} 已到达，来源 {peer}')
        try:
            # HTTP methods and TLS records may be split over TCP packets.
            data = await asyncio.wait_for(reader.readexactly(5), timeout=10)
            if data[0] == 22 and data[1] == 3 and self.tls:
                stream = TLSStream(reader, traffic, self.tls.context, data)
                await asyncio.wait_for(stream.handshake(), timeout=15)
                emit('tls_established', version=stream.ssl.version(), cipher=stream.ssl.cipher()[0])
                reader, output = stream, stream
                data = await asyncio.wait_for(reader.readexactly(5), timeout=10)
            else:
                output = traffic
            if data in (b'GET /', b'GET h', b'HEAD ', b'POST ', b'PUT /', b'OPTIO', b'DELET', b'PATCH'):
                data += await asyncio.wait_for(reader.readuntil(b'\r\n\r\n'), timeout=10)
                first, *headers = data.decode('iso-8859-1').split('\r\n')
                method, target, _ = first.split(' ', 2)
                path = urlsplit(target).path
                host = next((h.split(':', 1)[1].strip() for h in headers if h.lower().startswith('host:')), '')
                content_type = 'text/plain; charset=utf-8'
                cookie_header = ''
                if self.backend and hasattr(self.backend, 'authenticate') and path in ('/local-login', '/local-auth'):
                    fields = {h.split(':', 1)[0].lower(): h.split(':', 1)[1].strip() for h in headers if ':' in h}
                    if host != f'127.0.0.1:{self.port}':
                        raise ValueError('Invalid authentication host')
                    if method == 'GET' and path == '/local-login':
                        cookies = SimpleCookie()
                        try:
                            cookies.load(fields.get('cookie', ''))
                        except CookieError:
                            pass
                        has_remembered = bool(cookies.get('jgbol_remember') and cookies['jgbol_remember'].value)
                        body = (Path(__file__).with_name('login.html').read_text()
                                .replace('__CSRF__', self.backend.csrf)
                                .replace('__AUTO_LOGIN__', 'true' if has_remembered else 'false')).encode()
                        code, reason, content_type = 200, 'OK', 'text/html; charset=utf-8'
                    elif method == 'POST' and path == '/local-auth':
                        if not secrets.compare_digest(fields.get('x-local-csrf', ''), self.backend.csrf):
                            raise ValueError('Invalid authentication request')
                        if fields.get('origin', f'http://{host}') != f'http://{host}':
                            raise ValueError('Cross-origin authentication denied')
                        length = int(fields.get('content-length', '0'))
                        if not 0 < length <= 4096 or 'transfer-encoding' in fields:
                            raise ValueError('Invalid authentication body')
                        raw = await asyncio.wait_for(reader.readexactly(length), timeout=10)
                        payload = {}
                        try:
                            payload = json.loads(raw)
                            if not isinstance(payload, dict):
                                raise ValueError('请求格式错误')
                            cookies = SimpleCookie()
                            cookies.load(fields.get('cookie', ''))
                            remembered = cookies.get('jgbol_remember')
                            result = self.backend.authenticate(payload, remembered.value if remembered else '')
                            if 'remember_token' in result:
                                credential = result.pop('remember_token')
                                age = 30 * 86400 if credential else 0
                                cookie_header = f'Set-Cookie: jgbol_remember={credential}; Max-Age={age}; Path=/; HttpOnly; SameSite=Strict\r\n'
                        except (ValueError, UnicodeError, CookieError) as exc:
                            if isinstance(payload, dict) and payload.get('action') == 'resume':
                                cookie_header = 'Set-Cookie: jgbol_remember=; Max-Age=0; Path=/; HttpOnly; SameSite=Strict\r\n'
                            result = {'ok': False, 'error': str(exc)}
                        body = json.dumps(result, ensure_ascii=False).encode()
                        code, reason, content_type = 200, 'OK', 'application/json; charset=utf-8'
                    else:
                        code, reason, body = 405, 'Method Not Allowed', b'Method not allowed'
                elif method in ('GET', 'HEAD') and path.rstrip('/') == '/dailypaper':
                    from .monument import weekly_html
                    code, reason, body = 200, 'OK', weekly_html()
                    content_type = 'text/html; charset=utf-8'
                elif method in ('GET', 'HEAD') and path == '/__redirect_health':
                    code, reason, body = 200, 'OK', HEALTH
                elif method in ('GET', 'HEAD') and path in LIST_PATHS:
                    code, reason, body = 200, 'OK', self.server_list
                else:
                    code, reason, body = 501, 'Not Implemented', b'Local endpoint not implemented.\n'
                    if self.backend:
                        # The original support client parses JSON even on HTTP errors.
                        content_type = 'application/json; charset=utf-8'
                        body = b'{"ok":0,"data":[],"error":"offline_endpoint_not_implemented"}\n'
                emit('http_request', method=method, host=host, path=path,
                          status=code, response_bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
                response = (f'HTTP/1.1 {code} {reason}\r\nContent-Length: {len(body)}\r\n'
                            f'{cookie_header}Content-Type: {content_type}\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n\r\n').encode()
                output.write(response + (b'' if method == 'HEAD' else body))
                await output.drain()
            elif data[0] == 22 and data[1] == 3:
                emit('tls_received', bytes=len(data), message='TLS 已到本地；当前层未提供证书或握手')
            else:
                if self.backend:
                    state = {}
                    while True:
                        header = data + await asyncio.wait_for(reader.readexactly(HEADER.size - len(data)), timeout=120)
                        mid, size, _ = HEADER.unpack(header)
                        if not HEADER.size <= size <= MAX_PACKET:
                            raise ValueError('Invalid game packet size')
                        packet = header + await asyncio.wait_for(reader.readexactly(size - HEADER.size), timeout=10)
                        for reply in self.backend.respond(packet, state):
                            output.write(reply)
                            emit('game_response', message_id=HEADER.unpack_from(reply)[0], bytes=len(reply))
                        await output.drain()
                        data = await asyncio.wait_for(reader.readexactly(5), timeout=120)
                emit('tcp_received', bytes=len(data), message='TCP 已到本地；业务协议待实现')
                # Keep enough time to observe additional bytes, without replying with a fake protocol.
                total = len(data)
                while total < 1024 * 1024:
                    chunk = await asyncio.wait_for(reader.read(65536), timeout=10)
                    if not chunk:
                        break
                    total += len(chunk)
                    emit('tcp_received', bytes=len(chunk), total_bytes=total,
                         message=f'TCP 追加接收 {len(chunk)} 字节，累计 {total} 字节')
        except asyncio.CancelledError:
            end_reason = 'server_shutdown'
            raise
        except asyncio.IncompleteReadError as exc:
            end_reason = 'peer_closed'
            if exc.partial:
                emit('tcp_received', bytes=len(exc.partial), message='连接提前关闭')
        except (asyncio.TimeoutError, asyncio.LimitOverrunError, ValueError, OSError, EOFError, struct.error) as exc:
            end_reason = type(exc).__name__
            emit('local_connection_end', reason=end_reason, message=str(exc) or end_reason)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except asyncio.CancelledError:
                end_reason = 'server_shutdown'
                raise
            except OSError:
                pass
            finally:
                self.tasks.discard(task)
                emit('local_close', reason=end_reason, read_bytes=traffic.read_bytes,
                     written_bytes=traffic.written_bytes, duration_ms=round((time.monotonic() - started) * 1000, 2),
                     message=f'连接 {connection_id} 关闭（{end_reason}），读取 {traffic.read_bytes} 字节，写入 {traffic.written_bytes} 字节')
