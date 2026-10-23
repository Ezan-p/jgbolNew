"""Project-local CA and TLS MemoryBIO transport for the multiplexed listener."""
import asyncio
import hashlib
import os
from pathlib import Path
import re
import ssl
import subprocess


class LocalTLS:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        os.chmod(self.directory, 0o700)
        self.ca = self.directory / 'ca.pem'
        key = self.directory / 'ca.key'
        if not self.ca.exists():
            config = self.directory / 'ca.cnf'
            config.write_text('[req]\ndistinguished_name=dn\nx509_extensions=ca\nprompt=no\n'
                              '[dn]\nCN=JGBOL Local Development CA\n[ca]\nbasicConstraints=critical,CA:TRUE\n'
                              'keyUsage=critical,keyCertSign,cRLSign\nsubjectKeyIdentifier=hash\n')
            self.openssl('req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-sha256', '-days', '365',
                         '-keyout', key, '-out', self.ca, '-config', config)
            os.chmod(key, 0o600)
        self.contexts = {}
        self.context = self.for_name('jgbol-local.invalid')
        self.context.set_servername_callback(self.sni)

    def openssl(self, *args):
        subprocess.run(['openssl', *map(str, args)], check=True, capture_output=True, timeout=30)

    def for_name(self, hostname):
        if not re.fullmatch(r'[a-zA-Z0-9.-]{1,253}', hostname):
            raise ValueError('Invalid TLS hostname')
        if hostname in self.contexts:
            return self.contexts[hostname]
        stem = hashlib.sha256(hostname.encode()).hexdigest()[:24]
        cert, key = self.directory / (stem + '.pem'), self.directory / (stem + '.key')
        if not cert.exists():
            csr, config = self.directory / (stem + '.csr'), self.directory / (stem + '.cnf')
            config.write_text('[req]\ndistinguished_name=dn\nprompt=no\n[dn]\nCN=' + hostname + '\n'
                              '[leaf]\nbasicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\n'
                              'extendedKeyUsage=serverAuth\nsubjectAltName=DNS:' + hostname + '\n')
            self.openssl('req', '-new', '-newkey', 'rsa:2048', '-nodes', '-keyout', key, '-out', csr, '-config', config)
            self.openssl('x509', '-req', '-in', csr, '-CA', self.ca, '-CAkey', self.directory / 'ca.key',
                         '-set_serial', str(int(stem, 16)), '-days', '365', '-sha256', '-out', cert,
                         '-extfile', config, '-extensions', 'leaf')
            os.chmod(key, 0o600)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # The bundled OpenSSL only supports TLS 1.0. This listener is loopback-only.
        context.minimum_version = ssl.TLSVersion.TLSv1
        context.set_ciphers('DEFAULT:AES128-SHA')
        context.load_cert_chain(cert, key)
        self.contexts[hostname] = context
        return context

    def sni(self, sock, name, context):
        if name:
            sock.context = self.for_name(name)


class TLSStream:
    def __init__(self, reader, writer, context, initial):
        self.reader, self.writer = reader, writer
        self.incoming, self.outgoing = ssl.MemoryBIO(), ssl.MemoryBIO()
        self.ssl = context.wrap_bio(self.incoming, self.outgoing, server_side=True)
        self.incoming.write(initial)
        self.buffer = bytearray()

    async def flush(self):
        while self.outgoing.pending:
            self.writer.write(self.outgoing.read())
        await self.writer.drain()

    async def receive(self):
        await self.flush()
        chunk = await self.reader.read(65536)
        if not chunk:
            self.incoming.write_eof()
            raise EOFError('TLS peer closed')
        self.incoming.write(chunk)

    async def handshake(self):
        while True:
            try:
                self.ssl.do_handshake()
                await self.flush()
                return
            except ssl.SSLWantReadError:
                await self.receive()

    async def read(self, n=65536):
        if self.buffer:
            data = bytes(self.buffer[:n])
            del self.buffer[:n]
            return data
        while True:
            try:
                return self.ssl.read(n)
            except ssl.SSLWantReadError:
                await self.receive()
            except ssl.SSLZeroReturnError:
                return b''

    async def readexactly(self, n):
        data = bytearray()
        while len(data) < n:
            chunk = await self.read(n - len(data))
            if not chunk:
                raise asyncio.IncompleteReadError(bytes(data), n)
            data.extend(chunk)
        return bytes(data)

    async def readuntil(self, separator):
        data = bytearray()
        while True:
            chunk = await self.read(4096)
            if not chunk:
                raise asyncio.IncompleteReadError(bytes(data), None)
            data.extend(chunk)
            end = data.find(separator)
            if end >= 0:
                end += len(separator)
                self.buffer[:0] = data[end:]
                return bytes(data[:end])
            if len(data) > 16384:
                raise ValueError('TLS HTTP headers too large')

    def write(self, data):
        offset = 0
        while offset < len(data):
            offset += self.ssl.write(data[offset:offset + 16384])

    async def drain(self):
        await self.flush()
