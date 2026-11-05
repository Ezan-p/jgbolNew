import asyncio
import unittest
from unittest.mock import Mock
from network_redirect.request_timing import current, phase
from network_redirect.server import LandingServer
from network_redirect.protocol import encode


class TimingTests(unittest.IsolatedAsyncioTestCase):
    async def test_failed_backend_emits_timing_and_resets_context(self):
        reader = asyncio.StreamReader()
        reader.feed_data(encode(2999, {}))
        writer = Mock()
        async def closed(): pass
        writer.wait_closed = closed
        events = []
        backend = Mock()
        backend.respond.side_effect = ValueError('bad request')
        server = LandingServer(0, b'', lambda kind, **kw: events.append((kind, kw)), backend=backend)
        await server.handle(reader, writer)
        row = next(row for kind, row in events if kind == 'game_request_timing')
        self.assertEqual(row['status'], 'error')
        self.assertEqual(row['response_count'], 0)
        self.assertGreaterEqual(row['respond_ms'], 0)
        self.assertIsNone(current.get())

    def test_phase_accumulates_even_on_error(self):
        metrics = {}
        token = current.set(metrics)
        try:
            with phase('save'): pass
            first = metrics['save_ms']
            with self.assertRaises(ValueError):
                with phase('save'): raise ValueError()
            self.assertGreaterEqual(metrics['save_ms'], first)
        finally:
            current.reset(token)
