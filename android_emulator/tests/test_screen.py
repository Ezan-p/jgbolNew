"""Frame negotiation, backpressure, and input while waiting for display ACK."""
import asyncio
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock

from aiohttp import ClientSession, CookieJar, WSMsgType
from aiohttp.test_utils import TestServer
from android_emulator import gateway
from android_emulator.config import normalize_config


class ScreenTests(unittest.IsolatedAsyncioTestCase):
    async def check_stream(self, mode, query, expected):
        cfg = normalize_config(dict(package='org.example.game', activity='.Main',
                                    required_abis=[], mode=mode), Path('/tmp/screen-test/game.json'))
        app = gateway.make_app(cfg)
        app.cleanup_ctx.clear()
        payload = bytes(8) if expected == 'rgba' else b'png-test'
        stub = SimpleNamespace(
            getScreenshot=AsyncMock(return_value=SimpleNamespace(
                image=payload, format=SimpleNamespace(width=2, height=1))),
            sendTouch=AsyncMock(), cancel_touches=lambda: None)
        app['stub'] = stub
        async with TestServer(app) as server, ClientSession(cookie_jar=CookieJar(unsafe=True)) as client:
            await client.get(server.make_url('/'))
            async with client.ws_connect(server.make_url('/ws/screen' + query)) as ws:
                info = (await ws.receive(timeout=2)).json()
                self.assertEqual(info['encoding'], expected)
                self.assertEqual((await ws.receive(timeout=2)).data, payload)
                fmt = stub.getScreenshot.call_args.args[0].format
                self.assertEqual(fmt, gateway.pb.ImageFormat.RGBA8888 if expected == 'rgba' else gateway.pb.ImageFormat.PNG)
                # Rendering ACK is withheld: no new screenshot, but touch still works.
                await ws.send_json(dict(type='touch', id=1, x=1, y=0, down=True))
                for _ in range(50):
                    if stub.sendTouch.call_count:
                        break
                    await asyncio.sleep(.01)
                self.assertEqual(stub.sendTouch.call_count, 1)
                await asyncio.sleep(.06)
                self.assertEqual(stub.getScreenshot.call_count, 1)
                await ws.send_json({'type': 'ack'})
                self.assertEqual((await ws.receive(timeout=2)).json()['type'], 'frame')
                self.assertEqual((await ws.receive(timeout=2)).type, WSMsgType.BINARY)
            for _ in range(50):
                if app['controller'] is None:
                    break
                await asyncio.sleep(.01)
            self.assertIsNone(app['controller'])

    async def test_rgba_emulator(self):
        await self.check_stream('emulator', '?format=rgba', 'rgba')

    async def test_legacy_png(self):
        await self.check_stream('emulator', '', 'png')

    async def test_adb_png_fallback(self):
        await self.check_stream('adb', '?format=rgba', 'png')
