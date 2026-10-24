"""Audio forwarding works even when the ARM32 host audio backend is disabled."""
import asyncio
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

from aiohttp import ClientSession, CookieJar, WSMsgType
from aiohttp.test_utils import TestServer
from android_emulator import gateway
from android_emulator.config import normalize_config
from android_emulator.profiles import emulator_command


class AudioTests(unittest.IsolatedAsyncioTestCase):
    async def test_arm32_audio_forward_disconnect_and_reconnect(self):
        cfg = normalize_config(dict(title='Audio', package='org.example.audio', activity='.Main',
                                    required_abis=[], runtime_profile='arm32-native'),
                               Path('/tmp/audio-test/game.json'))
        # Keep the safe null host backend while using gRPC capture.
        self.assertEqual(emulator_command(cfg)[-2:], ['-audio', 'none'])
        app = gateway.make_app(cfg)
        app.cleanup_ctx.clear()
        streams = []
        pcm = b'\x01\x00\xff\xff' * 128

        class Stream:
            def __init__(self):
                self.cancelled = False
                self.sent = False
            def __aiter__(self):
                return self
            async def __anext__(self):
                if self.sent:
                    await asyncio.Event().wait()
                self.sent = True
                return SimpleNamespace(audio=pcm)
            def cancel(self):
                self.cancelled = True

        def stream_audio(fmt):
            self.assertEqual(fmt.samplingRate, 44100)
            stream = Stream()
            streams.append(stream)
            return stream

        app['stub'] = SimpleNamespace(streamAudio=stream_audio,
                                     getStatus=AsyncMock(return_value=SimpleNamespace(version='test')))
        async with TestServer(app) as server, ClientSession(cookie_jar=CookieJar(unsafe=True)) as client:
            await client.get(server.make_url('/'))
            with patch.object(gateway, 'device_info', AsyncMock(return_value={'issue': None})):
                status = await (await client.get(server.make_url('/api/status'))).json()
            self.assertTrue(status['audio'])
            for _ in range(2):
                async with client.ws_connect(server.make_url('/ws/audio')) as ws:
                    msg = await ws.receive(timeout=2)
                    self.assertEqual(msg.type, WSMsgType.BINARY)
                    self.assertEqual(msg.data, pcm)
                    self.assertEqual((await client.get(server.make_url('/ws/audio'))).status, 409)
                for _ in range(50):
                    if app['audio_client'] is None:
                        break
                    await asyncio.sleep(.01)
                self.assertIsNone(app['audio_client'])
                self.assertTrue(streams[-1].cancelled)
            self.assertEqual(app['audio_packets'], 2)
            # A failed token lookup must release the single audio slot too.
            app['stub'].streamAudio = lambda fmt: (_ for _ in ()).throw(FileNotFoundError('missing token'))
            async with client.ws_connect(server.make_url('/ws/audio')) as ws:
                msg = await ws.receive(timeout=2)
                self.assertEqual(msg.json()['type'], 'error')
                await ws.receive(timeout=2)
            await asyncio.sleep(.02)
            self.assertIsNone(app['audio_client'])
