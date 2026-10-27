"""Lossless battle transport over the original 32 KiB Lua-event protocol.

A long event/replay is preloaded through event 121 chunks before a small
reference is delivered to the original callback. Chunks never alter combat
resolution, drop effects, or remove history. Saved replays remain full objects.
"""
import hashlib
import copy

from . import summon
from .protocol import encode

PACKET_BUDGET = 24 * 1024
# The client permits at most 4 MiB / 256 chunks per preload. Keep each
# reconstructed object below half that limit; large histories and flat event
# tables preload bounded sibling groups instead of one oversized transfer.
PRELOAD_BUDGET = 2 * 1024 * 1024
REFERENCE_KEY = '_local_replay_id'
CHUNK_KEY = 'offline_battle_chunk'
RESULT_MARKER = 255


def _packet(message_id, fields, literal):
    return encode(message_id, dict(fields, data=literal))


def _small_packet(message_id, fields, literal):
    if len(literal.encode('utf-8')) > PACKET_BUDGET:
        return None
    packet = _packet(message_id, fields, literal)
    return packet if len(packet) <= PACKET_BUDGET else None


def _chunks(kind, literal, fight_id=0):
    """Split a Lua literal as text; each envelope remains a complete Lua table."""
    key = hashlib.sha256(literal.encode('utf-8')).hexdigest()
    pieces = []
    offset = 0
    # Size using an upper bound for index/total digits, including escaping and
    # UTF-8. Never split an encoded Unicode character or assume character=byte.
    count_bound = max(1, len(literal))
    while offset < len(literal):
        low, high = 1, min(len(literal)-offset, PACKET_BUDGET)
        best = 0
        while low <= high:
            length = (low+high)//2
            envelope = dict(fight_id=fight_id, offline_battle_chunk=dict(
                kind=kind, key=key, index=count_bound, total=count_bound,
                payload=literal[offset:offset+length]))
            if _small_packet(2998, dict(id=121), summon.lua(envelope)) is not None:
                best = length; low = length+1
            else:
                high = length-1
        if not best:
            raise ValueError('Battle chunk envelope exceeds the transport budget')
        pieces.append(literal[offset:offset+best]); offset += best
    packets = []
    for index, piece in enumerate(pieces, 1):
        envelope = dict(fight_id=fight_id, offline_battle_chunk=dict(
            kind=kind, key=key, index=index, total=len(pieces), payload=piece))
        packet = _packet(2998, dict(id=121), summon.lua(envelope))
        assert len(packet) <= PACKET_BUDGET
        packets.append(packet)
    return key, packets


def effect_packets(data):
    """Publish one complete effect cache, including an empty-cache reset."""
    data = {int(k) if str(k).isdigit() else k: v for k, v in data.items()}
    literal = summon.lua(data)
    packet = _small_packet(2998, dict(id=121), literal)
    if packet is not None:
        return [packet]
    if len(literal.encode('utf-8')) > PRELOAD_BUDGET:
        return lua_packets(2998, dict(id=121), data, data.get('fight_id', 0))
    return _chunks('events', literal, data.get('fight_id', 0))[1]


def _preload(payload, packets, fight_id):
    literal = summon.lua(payload)
    if len(literal.encode('utf-8')) > PRELOAD_BUDGET:
        if not isinstance(payload, (dict, list)):
            raise ValueError('A single battle field exceeds the preload budget')
        # Group small siblings. Preloading each event separately turns a few
        # megabytes into tens of thousands of packets. Original numeric keys
        # are retained, so the client merges list fragments without reindexing.
        groups, group, size = [], {}, 2
        items = payload.items() if isinstance(payload, dict) else enumerate(payload, 1)
        for key, value in items:
            entry_size = len(summon.lua({key: value}).encode('utf-8')) - 2
            if entry_size + 2 > PRELOAD_BUDGET:
                value = _preload(value, packets, fight_id)
                entry_size = len(summon.lua({key: value}).encode('utf-8')) - 2
            if group and size + entry_size + 1 > PRELOAD_BUDGET:
                groups.append(_preload(group, packets, fight_id)); group, size = {}, 2
            size += entry_size + bool(group)
            group[key] = value
        if group:
            groups.append(_preload(group, packets, fight_id))
        payload = {'_local_replay_parts': groups}
        literal = summon.lua(payload)
        if len(literal.encode('utf-8')) > PRELOAD_BUDGET:
            raise ValueError('Battle metadata exceeds the bounded preload budget')
    key, chunks = _chunks('replay', literal, fight_id)
    packets.extend(chunks)
    return {REFERENCE_KEY: key}


def lua_packets(message_id, fields, payload, fight_id=0):
    """Encode an arbitrary nested response without truncating its contents."""
    literal = summon.lua(payload)
    packet = _small_packet(message_id, fields, literal)
    if packet is not None:
        return [packet]
    packets = []
    reference = _preload(payload, packets, fight_id)
    packets.append(_packet(message_id, fields, summon.lua(reference)))
    return packets


def event_packets(kind, payload, fight_id=0):
    return lua_packets(2998, dict(id=kind), payload, fight_id)


def result_message(fields):
    """Native-shaped result without the byte-sized action count limitation.

    Nested replay records are Lua data, so an encode/decode round trip would
    impose a transport restriction on a perfectly valid thirty-round battle.
    """
    value = dict(serial_num=0, fight_id=0, fight_type=0, guide_stage=0, final_result=0)
    value.update(copy.deepcopy(fields))
    value['fight_result'] = list(value.get('fight_result', []))
    value['fight_round'] = len(value['fight_result'])
    for row in value['fight_result']:
        for key, default in (('self_use', False), ('skill_type', 0), ('is_src', False),
                             ('result', 0), ('src_order', 0), ('des_order', 0), ('cur_round', 0)):
            row.setdefault(key, default)
        row['damage_list'] = list(row.get('damage_list', []))
        row['damage_count'] = len(row['damage_list'])
    return value


def result_packets(message_id, fields):
    """Preload long results, then notify the original 1027/1140 receiver.

    The client resolves the marked notification before the native handler
    runs. A missing preload fails explicitly instead of playing an empty win.
    """
    if message_id not in (1027, 1140):
        raise ValueError('Not a battle-result message')
    value = result_message(fields)
    if value['fight_round'] <= 255:
        try:
            return [encode(message_id, value)]
        except ValueError as error:
            if str(error) != 'Packet too large':
                raise
    packets = event_packets(121, dict(fight_id=value['fight_id'],
                                      offline_battle_result=value), value['fight_id'])
    # Backend assigns serial_num after encoding, so it cannot carry the marker.
    # Stage 255 is reserved for this adapter and removed before native handlers.
    notice = dict(value, guide_stage=RESULT_MARKER, fight_round=0, fight_result=[])
    packets.append(encode(message_id, notice))
    return packets
