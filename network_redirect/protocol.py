"""JGB 3.87 wire codec, derived from the client's registered field definitions.

Header: little-endian uint16 type, uint32 total size, uint32 connection ID.
'd' is an IEEE double, 's' a NUL-terminated string (not a length-prefixed one).
"""
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
TABLES = json.loads((ROOT / 'analysis/evidence/protocol_tables.json').read_text())
DEFS = {v['id']: v['def'] for group in ('common_def', 'lscl_msg', 'gscl_msg')
        for v in TABLES[group].values()}
FORMATS = {'I': 'I', 'i': 'i', 'W': 'H', 'w': 'h', 'B': 'B', 'b': 'B', 'l': '?', 'f': 'f', 'd': 'd'}
HEADER = struct.Struct('<HII')
MAX_PACKET = 32768


def fields(message_id):
    for field in DEFS[message_id].split(','):
        name, kind = field.split('=')
        yield name, kind


def encode_body(message_id, values):
    parts = []
    previous = None
    for name, kind in fields(message_id):
        value = values.get(name, '' if kind.startswith(('S', 's', 'N')) else 0)
        if kind in FORMATS:
            parts.append(struct.pack('<' + FORMATS[kind], value))
        elif kind == 's':
            raw = str(value).encode('utf-8')
            if b'\0' in raw:
                raise ValueError('NUL in string')
            parts.append(raw + b'\0')
        elif re.fullmatch(r'[SN]\[\d+\]', kind):
            size = int(kind[2:-1])
            raw = value if isinstance(value, bytes) else str(value).encode('utf-8')
            if len(raw) > size or (kind[0] == 'S' and len(raw) == size):
                raise ValueError('Fixed string too long: ' + name)
            parts.append(raw.ljust(size, b'\0'))
        elif re.fullmatch(r'[IiWwBbldf]\[\d+\]', kind):
            limit = int(kind[2:-1])
            value = values.get(name, [])
            if previous is None or previous[1] not in ('B', 'b') or values.get(previous[0], 0) != len(value):
                raise ValueError('Array count mismatch: ' + name)
            if len(value) > min(limit, 255):
                raise ValueError('Array too large: ' + name)
            parts.append(struct.pack('<' + FORMATS[kind[0]] * len(value), *value))
        elif re.fullmatch(r'\$\d+\{\d+\}', kind):
            subtype, limit = map(int, re.findall(r'\d+', kind))
            value = values.get(name, [])
            # Native push_complicated_value reads the preceding byte as count.
            if previous is None or previous[1] not in ('B', 'b') or values.get(previous[0], 0) != len(value):
                raise ValueError('Array count mismatch: ' + name)
            if len(value) > min(limit, 255):
                raise ValueError('Array too large: ' + name)
            parts.extend(encode_body(subtype, item) for item in value)
        else:
            raise ValueError('Unsupported field: ' + kind)
        previous = (name, kind)
    return b''.join(parts)


def encode(message_id, values, connection_id=0):
    body = encode_body(message_id, values)
    if len(body) + HEADER.size > MAX_PACKET:
        raise ValueError('Packet too large')
    return HEADER.pack(message_id, len(body) + HEADER.size, connection_id) + body


def decode(packet):
    if len(packet) < HEADER.size:
        raise ValueError('Truncated header')
    message_id, size, connection_id = HEADER.unpack_from(packet)
    if size != len(packet) or not HEADER.size <= size <= MAX_PACKET:
        raise ValueError('Invalid packet size')
    if message_id not in DEFS:
        return message_id, connection_id, None
    values, offset = decode_body(message_id, packet, HEADER.size)
    if offset != size:
        raise ValueError('Trailing bytes')
    return message_id, connection_id, values


def decode_body(message_id, packet, offset):
    values, size, previous = {}, len(packet), None
    for name, kind in fields(message_id):
        if kind in FORMATS:
            fmt = '<' + FORMATS[kind]
            length = struct.calcsize(fmt)
            if offset + length > size:
                raise ValueError('Truncated field: ' + name)
            value = struct.unpack_from(fmt, packet, offset)[0]
        elif kind == 's':
            end = packet.find(b'\0', offset)
            if end < 0:
                raise ValueError('Unterminated string')
            length = end - offset + 1
            value = packet[offset:end].decode('utf-8')
        elif re.fullmatch(r'[SN]\[\d+\]', kind):
            length = int(kind[2:-1])
            if offset + length > size:
                raise ValueError('Truncated string')
            raw = packet[offset:offset + length]
            value = raw.split(b'\0', 1)[0].decode('utf-8') if kind[0] == 'S' else raw
        elif re.fullmatch(r'[IiWwBbldf]\[\d+\]', kind):
            limit = int(kind[2:-1])
            if previous is None or previous[1] not in ('B', 'b'):
                raise ValueError('Unsupported array count: ' + name)
            count = values[previous[0]]
            if count > limit:
                raise ValueError('Array too large: ' + name)
            fmt = '<' + FORMATS[kind[0]] * count
            length = struct.calcsize(fmt)
            if offset + length > size:
                raise ValueError('Truncated array: ' + name)
            value = list(struct.unpack_from(fmt, packet, offset))
        elif re.fullmatch(r'\$\d+\{\d+\}', kind):
            subtype, limit = map(int, re.findall(r'\d+', kind))
            if previous is None or previous[1] not in ('B', 'b'):
                raise ValueError('Unsupported array count: ' + name)
            count = values[previous[0]]
            if count > limit:
                raise ValueError('Array too large: ' + name)
            value, length = [], 0
            for _ in range(count):
                item, end = decode_body(subtype, packet, offset + length)
                value.append(item)
                length = end - offset
        else:
            raise ValueError('Unsupported field: ' + kind)
        values[name] = value
        offset += length
        previous = (name, kind)
    return values, offset
