"""HTTPS verification and bounded quorum acquisition without live network."""
from email.message import Message
import ssl
import threading
import unittest
from unittest.mock import patch

from network_redirect import network_time as nt
from tests.test_game_clock import Source, NOW


class NetworkTransportTests(unittest.TestCase):
    def headers(self, date='Fri, 23 Oct 2026 12:00:00 GMT', age=None):
        result = Message()
        result['Date'] = date
        if age is not None:
            result['Age'] = age
        return result

    def test_date_cache_status_latency_and_zone_validation(self):
        self.assertGreater(nt.read_date(self.headers(), 200, 0.2), 0)
        for headers, status, latency in [
                (Message(), 200, 1), (self.headers(age='60'), 200, 1),
                (self.headers(age='nan'), 200, 1), (self.headers(), 500, 1),
                (self.headers(), 200, 10), (self.headers('bad'), 200, 1),
                (self.headers('Fri, 23 Oct 2026 12:00:00'), 200, 1)]:
            with self.subTest(headers=headers, status=status, latency=latency):
                with self.assertRaises((ValueError, TypeError)):
                    nt.read_date(headers, status, latency)
        headers = self.headers(); headers['Date'] = headers['Date']
        with self.assertRaises(ValueError):
            nt.read_date(headers, 200, 0.1)

    def test_quorum_rejects_single_duplicate_and_disagreement(self):
        source = Source()
        row = (nt.HOSTS[0], NOW, 100, 0.1)
        self.assertIsNone(nt.consensus([row], source))
        self.assertIsNone(nt.consensus([row, row], source))
        self.assertIsNone(nt.consensus([row, (nt.HOSTS[1], NOW+1000, 100, 0.1)], source))
        obs = nt.consensus([row, (nt.HOSTS[1], NOW+1, 100, 0.1),
                            (nt.HOSTS[2], NOW+10000, 100, 0.1)], source)
        self.assertEqual(set(obs.hosts), set(nt.HOSTS[:2]))
        self.assertAlmostEqual(obs.epoch, NOW + 0.5)

    def test_tls_validation_not_disabled_and_android_roots_supported(self):
        context = nt.tls_context()
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertGreaterEqual(context.minimum_version, ssl.TLSVersion.TLSv1_2)

    def test_fixed_https_request_nonce_no_redirects_or_user_data(self):
        with patch.object(nt.http.client, 'HTTPSConnection') as constructor:
            response = constructor.return_value.getresponse.return_value
            response.status = 302
            response.headers = self.headers(age='0')
            context = object()
            row = nt.fetch(nt.HOSTS[0], Source(), context)
            self.assertEqual(row[0], nt.HOSTS[0])
            constructor.assert_called_once_with(nt.HOSTS[0], timeout=nt.REQUEST_TIMEOUT, context=context)
            args, kw = constructor.return_value.request.call_args
            self.assertEqual(args[0], 'HEAD')
            self.assertTrue(args[1].startswith('/?jgbol_time_nonce='))
            self.assertNotIn('body', kw)
            self.assertEqual(constructor.return_value.getresponse.call_count, 1)
            constructor.return_value.close.assert_called_once()
        with self.assertRaises(ValueError):
            nt.fetch('attacker.example', Source(), context)

    def test_success_backoff_failure_keeps_previous_result_and_close(self):
        source = Source()
        failing = [False]
        def fetcher(host, source, context):
            if failing[0]:
                raise ssl.SSLError('verification failed')
            return (host, NOW, source.elapsed(), 0.1)
        service = nt.TimeService(source, fetcher=fetcher, context_factory=lambda: object())
        self.addCleanup(service.close)
        self.assertTrue(service.request(force=True))
        observation = service.wait(1)
        self.assertIsNotNone(observation)
        self.assertFalse(service.request(force=True))
        self.assertFalse(service.request())
        failing[0] = True
        service.last_attempt -= nt.REFRESH_INTERVAL
        self.assertTrue(service.request())
        service.wait(1)
        self.assertEqual(service.read(), observation)
        self.assertEqual(service.error, 'unavailable')
        service.close()
        self.assertFalse(service.request(force=True))

    def test_dns_stall_is_bounded_and_does_not_spawn_unlimited_workers(self):
        gate = threading.Event()
        def stalled(host, source, context):
            gate.wait(2)
            raise OSError('offline')
        service = nt.TimeService(Source(), fetcher=stalled, context_factory=lambda: object())
        self.addCleanup(service.close)
        self.addCleanup(gate.set)
        with patch.object(nt, 'ROUND_TIMEOUT', 0.05):
            service.request(force=True)
            self.assertIsNone(service.wait(0.5))
            self.assertFalse(service.running)
            workers = dict(service.workers)
            service.last_attempt -= nt.RETRY_INTERVAL
            service.request(force=True);service.wait(0.5)
            self.assertEqual(service.workers, workers)

    def test_certificate_failure_never_creates_anchor(self):
        def fail():
            raise ssl.SSLError('no trusted roots')
        service = nt.TimeService(Source(), context_factory=fail)
        self.addCleanup(service.close)
        service.request(force=True)
        self.assertIsNone(service.wait(1))
        self.assertEqual(service.error, 'unavailable')
