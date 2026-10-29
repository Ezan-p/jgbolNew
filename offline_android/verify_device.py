"""Host-side acceptance test of the backend actually running inside the APK.

An ADB forward may be used for testing only: tcp:<host-port> -> tcp:18770.
This tool never starts a desktop game service and is not included in the APK.
"""
import argparse
import hashlib
import http.client
import json
from pathlib import Path
import re
import socket
import time

from network_redirect.protocol import HEADER, decode, encode

ACCOUNT = 'offline_upgrade'
PASSWORD = 'OfflineAcceptance2026!'


class Device:
    def __init__(self, port, device_port=18770, account=ACCOUNT):
        self.port = port
        self.device_port = device_port
        self.account = account
        self.serial = 5000
        self.timings = []

    def http(self, path, payload=None, csrf=''):
        started = time.monotonic()
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=90)
        body = json.dumps(payload) if payload is not None else None
        connection.request('POST' if body is not None else 'GET', path, body,
                           {'Host': '127.0.0.1:' + str(self.device_port), 'X-Local-CSRF': csrf})
        response = connection.getresponse()
        if response.status != 200:
            raise RuntimeError('Unexpected HTTP status: ' + str(response.status))
        result = response.read()
        connection.close()
        self.timings.append(dict(operation='HTTP ' + path,
                                 milliseconds=round((time.monotonic() - started) * 1000, 1)))
        return result

    def authenticate(self, register=False):
        page = self.http('/local-login').decode()
        csrf = re.search(r"setRequestHeader\('X-Local-CSRF','([^']+)'\)", page)[1]
        payload = dict(action='register' if register else 'login', username=self.account,
                       password=PASSWORD, confirm=PASSWORD, remember=False)
        result = json.loads(self.http('/local-auth', payload, csrf))
        if not result['ok']:
            raise RuntimeError('Device authentication failed: ' + result.get('error', 'unknown'))
        self.token = result['token']

    def packet(self):
        def exact(size):
            data = b''
            while len(data) < size:
                more = self.connection.recv(size - len(data))
                if not more:
                    raise EOFError('Device game service closed the connection')
                data += more
            return data
        head = exact(HEADER.size)
        return decode(head + exact(HEADER.unpack(head)[1] - HEADER.size))

    def request(self, mid, **fields):
        started = time.monotonic()
        self.serial += 1
        self.connection.sendall(encode(mid, dict(serial_num=self.serial, **fields)))
        packets = []
        while True:
            packet = self.packet()
            packets.append(packet)
            m, _, data = packet
            if m == 2998 and data['id'] == 55:
                raise RuntimeError('Device rejected operation: ' + data['data'])
            if m == 1106 and data['req_serial_num'] == self.serial:
                self.timings.append(dict(operation='game ' + str(mid),
                                         stage=fields.get('stage'),
                                         milliseconds=round((time.monotonic() - started) * 1000, 1)))
                return packets

    def connect(self):
        self.connection = socket.create_connection(('127.0.0.1', self.port), timeout=90)
        self.connection.settimeout(90)
        started = time.monotonic()
        self.connection.sendall(encode(3001, dict(id=68, data='{access_token="' + self.token + '"}')))
        mid, _, ticket = self.packet()
        self.timings.append(dict(operation='LS 3001 -> 3002',
                                 milliseconds=round((time.monotonic() - started) * 1000, 1)))
        assert mid == 3002 and ticket['server_port'] == self.device_port and ticket['server_ip'] == '127.0.0.1'
        self.connection.sendall(encode(1001, {key: ticket[key] for key in ('auth_key', 'seed', 'account')}))
        started = time.monotonic()
        mid, _, result = self.packet()
        self.timings.append(dict(operation='BS 1001 -> 1002',
                                 milliseconds=round((time.monotonic() - started) * 1000, 1)))
        assert mid == 1002 and result['result'] == 0
        # A serialized read-only request supplies a definite end marker after
        # the complete login snapshot, so no timing-based packet draining is used.
        return self.request(1307, flag=2)

    def close(self):
        self.connection.shutdown(socket.SHUT_WR)
        while self.connection.recv(65536):
            pass
        self.connection.close()


def stable_snapshot(packets):
    role = next(data for mid, _, data in packets if mid == 1017)
    fields = ('role_name', 'role_id', 'level', 'head_type', 'guide_progress',
              'gold_coin', 'silver_coin', 'cur_exp', 'register_account', 'pf_account')
    result = {key: role[key] for key in fields if key in role}
    companions, attachments = [], []
    for mid, _, data in packets:
        if mid == 1034:
            companions.extend(data['cortege_list'])
        elif mid == 1035:
            attachments.extend(data['attach_list'])
    result['companions'] = sorted(({key: row[key] for key in ('id', 'type', 'level', 'order')}
                                    for row in companions), key=lambda row: row['id'])
    result['attachments'] = sorted(({key: row[key] for key in ('id', 'type_id', 'count', 'level')}
                                    for row in attachments), key=lambda row: row['id'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=18870)
    parser.add_argument('--device-port', type=int, default=18770)
    parser.add_argument('--account', default=ACCOUNT)
    parser.add_argument('--mode', choices=('prepare', 'verify'), required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    device = Device(args.port, args.device_port, args.account)
    assert device.http('/__redirect_health') == b'JGBOL_LOCAL_REDIRECT_OK\n'
    device.authenticate(register=args.mode == 'prepare')
    packets = device.connect()
    if args.mode == 'prepare':
        for stage in (1, 2, 3, 4, 5):
            fields = dict(stage=stage, name='', head_type=0)
            if stage == 1:
                fields.update(name='离线验收', head_type=101)
            elif stage == 2:
                fields['name'] = '1'
            responses = device.request(1204, **fields)
            if stage == 3:
                assert any(mid == 1027 for mid, _, _ in responses), 'Guide fight did not run'
        device.close()
        packets = device.connect()
        snapshot = stable_snapshot(packets)
        assert snapshot['role_name'] == '离线验收'
        assert snapshot['guide_progress'] & 62 == 62
        assert len(snapshot['companions']) == 2
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
    else:
        snapshot = stable_snapshot(packets)
        expected = json.loads(args.record.read_text())
        if snapshot != expected:
            raise AssertionError('Save progress differs after upgrade:\n' + json.dumps(
                dict(before=expected, after=snapshot), ensure_ascii=False, indent=2))
    device.close()
    fingerprint = hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()
    print(json.dumps(dict(result='PASS', mode=args.mode, account=args.account,
                          snapshot_sha256=fingerprint, progress=snapshot,
                          request_timings=device.timings), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
