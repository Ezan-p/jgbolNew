import asyncio
import unittest

from network_redirect.server import HEALTH, LandingServer


class LandingTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.events = []
        self.payload = b'-- cached server list\nversion=1263,\n'
        self.server = LandingServer(0, self.payload, lambda kind, **row: self.events.append(dict(kind=kind, **row)))
        await self.server.start()
        self.port = self.server.server.sockets[0].getsockname()[1]

    async def asyncTearDown(self):
        await self.server.close()

    async def request(self, request, fragmented=False):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        if fragmented:
            for part in (request[:2], request[2:9], request[9:]):
                writer.write(part)
                await writer.drain()
                await asyncio.sleep(.01)
        else:
            writer.write(request)
            await writer.drain()
        result = await asyncio.wait_for(reader.read(), 2)
        writer.close()
        await writer.wait_closed()
        return result

    async def test_fragmented_health(self):
        response = await self.request(b'GET /__redirect_health HTTP/1.1\r\nHost: probe.invalid\r\n\r\n', True)
        self.assertTrue(response.startswith(b'HTTP/1.1 200'))
        self.assertEqual(response.split(b'\r\n\r\n', 1)[1], HEALTH)

    async def test_cached_list_bytes_and_query_redaction(self):
        response = await self.request(b'GET /update/jgb/p360_a/server_list.txt?secret=hide HTTP/1.1\r\nHost: original.example\r\n\r\n')
        self.assertEqual(response.split(b'\r\n\r\n', 1)[1], self.payload)
        self.assertNotIn('hide', str(self.events))
        event = next(e for e in self.events if e['kind'] == 'http_request')
        self.assertEqual(event['host'], 'original.example')

    async def test_unknown_endpoint_not_fake_success(self):
        response = await self.request(b'POST /login HTTP/1.1\r\nHost: sdk.invalid\r\nContent-Length: 3\r\n\r\nabc')
        self.assertTrue(response.startswith(b'HTTP/1.1 501'))

    async def test_tls_reaches_local_without_downgrade(self):
        response = await self.request(b'\x16\x03\x01\x00\x00', True)
        self.assertEqual(response, b'')
        self.assertTrue(any(e['kind'] == 'tls_received' for e in self.events))

    async def test_head_and_traversal(self):
        response = await self.request(b'HEAD /update/jgb/p360_a/server_list.txt HTTP/1.1\r\n\r\n')
        self.assertEqual(response.split(b'\r\n\r\n', 1)[1], b'')
        response = await self.request(b'GET /../../game.json HTTP/1.1\r\n\r\n')
        self.assertTrue(response.startswith(b'HTTP/1.1 501'))

    async def test_short_binary_and_shutdown(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        writer.write(b'\x01\x02')
        await writer.drain()
        writer.write_eof()
        self.assertEqual(await reader.read(), b'')
        writer.close()
        await writer.wait_closed()
        self.assertTrue(any(e['kind'] == 'tcp_received' and e['bytes'] == 2 for e in self.events))

    async def test_concurrent_connections_have_separate_complete_logs(self):
        requests = [b'GET /__redirect_health HTTP/1.1\r\nHost: one.invalid\r\n\r\n',
                    b'HEAD /update/jgb/p360_a/server_list.txt HTTP/1.1\r\nHost: two.invalid\r\n\r\n']
        responses = await asyncio.gather(*(self.request(request, True) for request in requests))
        await asyncio.sleep(.01)
        accepts = [e for e in self.events if e['kind'] == 'local_accept']
        self.assertEqual(len({e['connection_id'] for e in accepts}), 2)
        for request, response, host in zip(requests, responses, ('one.invalid', 'two.invalid')):
            http = next(e for e in self.events if e['kind'] == 'http_request' and e['host'] == host)
            close = next(e for e in self.events if e['kind'] == 'local_close'
                         and e['connection_id'] == http['connection_id'])
            self.assertEqual(close['read_bytes'], len(request))
            self.assertEqual(close['written_bytes'], len(response))
            self.assertEqual(close['reason'], 'completed')

    async def test_shutdown_closes_waiting_clients_and_records_reason(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        writer.write(b'raw tcp data')
        await writer.drain()
        for _ in range(100):
            if any(e['kind'] == 'tcp_received' for e in self.events):
                break
            await asyncio.sleep(.01)
        await self.server.close()
        self.assertEqual(await asyncio.wait_for(reader.read(), 2), b'')
        writer.close()
        await writer.wait_closed()
        self.assertFalse(self.server.tasks)
        close = next(e for e in self.events if e['kind'] == 'local_close')
        self.assertEqual(close['reason'], 'server_shutdown')
        self.assertEqual(close['read_bytes'], len(b'raw tcp data'))

    async def test_truncated_request_does_not_poison_listener(self):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        writer.write(b'\x01\x02')
        await writer.drain()
        writer.write_eof()
        await reader.read()
        writer.close()
        await writer.wait_closed()
        response = await self.request(b'GET /__redirect_health HTTP/1.1\r\n\r\n')
        self.assertIn(HEALTH, response)
        closed = next(e for e in self.events if e['kind'] == 'local_close' and e['reason'] == 'peer_closed')
        self.assertEqual(closed['read_bytes'], 2)


if __name__ == '__main__':
    unittest.main()
