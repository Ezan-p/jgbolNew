"""Bounded HTTPS clock consensus. No game data, redirects or TLS bypass.

HTTP Date is second-resolution server time, not an atomic-clock service. Two
independent TLS hosts must agree; failures leave the last trusted clock intact.
Network threads never access SQLite. Only the backend thread consumes results.
"""
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
import http.client
import math
from pathlib import Path
import queue
import secrets
import ssl
import threading
import time

HOSTS = ('www.baidu.com', 'www.qq.com', 'www.cloudflare.com')
ROUND_TIMEOUT = 5.0
REQUEST_TIMEOUT = 3.0
MAX_RTT = 4.0
MAX_SKEW = 5.0
RETRY_INTERVAL = 60.0
REFRESH_INTERVAL = 15 * 60.0
RESUME_MARKER = 2147483646
WAIT_MESSAGE = '北京时间尚未联网校准，暂沿用已保存时间；跨重启离线收益待联网确认。'
FUTURE_MESSAGE = '北京时间已校准；存档有未来结算记录，相关额度将在北京时间追上后继续刷新。'


@dataclass(frozen=True)
class Observation:
    epoch: float
    elapsed: float
    wall: float
    boot: str
    hosts: tuple
    uncertainty: float
    token: str


def tls_context():
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    # Embedded CPython has no desktop CA bundle. Use Android's system roots,
    # never the game's loopback CA or a user-added certificate directory.
    for directory in ('/apex/com.android.conscrypt/cacerts', '/system/etc/security/cacerts'):
        root = Path(directory)
        if root.is_dir():
            for path in root.iterdir():
                if path.is_file():
                    try:
                        context.load_verify_locations(cadata=path.read_text())
                    except (OSError, UnicodeError, ssl.SSLError):
                        continue
    return context


def read_date(headers, status, rtt):
    if not 200 <= status < 400 or not 0 <= rtt <= MAX_RTT:
        raise ValueError('time response status/latency')
    dates = headers.get_all('Date', [])
    ages = headers.get_all('Age', [])
    if len(dates) != 1 or len(ages) > 1 or (ages and float(ages[0]) != 0):
        raise ValueError('missing, duplicate or cached time')
    stamp = parsedate_to_datetime(dates[0])
    if stamp.tzinfo is None:
        raise ValueError('time has no timezone')
    epoch = stamp.timestamp()
    if not math.isfinite(epoch) or not 1577836800 <= epoch <= 4102444800:
        raise ValueError('time outside supported range')
    return epoch + 0.5 + rtt / 2  # Date quantization and approximate transit.


def fetch(host, source, context):
    if host not in HOSTS:
        raise ValueError('unapproved time host')
    start = source.elapsed()
    connection = http.client.HTTPSConnection(host, timeout=REQUEST_TIMEOUT, context=context)
    try:
        connection.request('HEAD', '/?jgbol_time_nonce=' + secrets.token_hex(16), headers={
            'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache',
            'Connection': 'close', 'User-Agent': 'JGBOL-Time/1'})
        response = connection.getresponse()
        end = source.elapsed()
        return (host, read_date(response.headers, response.status, end - start), end, end - start)
    finally:
        connection.close()


def consensus(samples, source):
    now = source.elapsed()
    unique = {host: (epoch + now - elapsed, rtt) for host, epoch, elapsed, rtt in samples
              if host in HOSTS and 0 <= now - elapsed <= ROUND_TIMEOUT + MAX_RTT
              and math.isfinite(epoch) and 0 <= rtt <= MAX_RTT}
    rows = sorted((epoch, host, rtt) for host, (epoch, rtt) in unique.items())
    # Use a quorum, never an average that includes a distant outlier.
    for index in range(len(rows) - 1):
        a, b = rows[index:index + 2]
        if b[0] - a[0] <= MAX_SKEW:
            return Observation((a[0] + b[0]) / 2, now, source.wall(), source.boot_id,
                               (a[1], b[1]), 1 + max(a[2], b[2]) / 2 + (b[0] - a[0]) / 2,
                               secrets.token_hex(16))
    return None


class TimeService:
    def __init__(self, source, *, fetcher=fetch, context_factory=tls_context):
        self.source, self.fetcher, self.context_factory = source, fetcher, context_factory
        self.lock = threading.Lock()
        self.done = threading.Event()
        self.latest = None
        self.error = None
        self.closed = False
        self.running = False
        self.last_attempt = None
        self.workers = {}

    def request(self, *, force=False):
        with self.lock:
            now = self.source.elapsed()
            interval = RETRY_INTERVAL if force or self.latest is None or self.error else REFRESH_INTERVAL
            if self.closed or self.running or (self.last_attempt is not None and now - self.last_attempt < interval):
                return False
            self.running = True
            self.last_attempt = now
            self.done.clear()
            threading.Thread(target=self._run, name='JGBTimeConsensus', daemon=True).start()
            return True

    def _run(self):
        results = queue.Queue(maxsize=len(HOSTS))
        observation = None
        try:
            context = self.context_factory()
            def query(host):
                try:
                    results.put_nowait(self.fetcher(host, self.source, context))
                except Exception:
                    pass  # No account data or transport internals in UI/logs.
            for host in HOSTS:
                old = self.workers.get(host)
                if old is None or not old.is_alive():
                    worker = threading.Thread(target=query, args=(host,), daemon=True, name='JGBTimeHTTPS')
                    self.workers[host] = worker
                    worker.start()
            deadline = time.monotonic() + ROUND_TIMEOUT
            samples = []
            while time.monotonic() < deadline:
                try:
                    samples.append(results.get(timeout=min(0.1, max(0.001, deadline - time.monotonic()))))
                except queue.Empty:
                    if all(not worker.is_alive() for worker in self.workers.values()):
                        break
                observation = consensus(samples, self.source)
                if observation:
                    break
        except Exception:
            observation = None
        finally:
            with self.lock:
                if not self.closed:
                    if observation:
                        self.latest = observation
                    self.error = None if observation else 'unavailable'
                self.running = False
                self.done.set()

    def read(self):
        with self.lock:
            return self.latest

    def wait(self, timeout=ROUND_TIMEOUT + 0.5):
        self.done.wait(timeout)
        return self.read()

    def close(self):
        # Workers are bounded per host and daemonized; no shutdown network wait.
        with self.lock:
            self.closed = True
