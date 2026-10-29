"""Build a compact exact-byte APK delta; APK signatures survive reconstruction."""
import json
from pathlib import Path
import struct
import zipfile

from opening_patch.apply_patch import sha256


def data_offset(stream, entry):
    stream.seek(entry.header_offset)
    header = stream.read(30)
    if header[:4] != b'PK\x03\x04':
        raise ValueError('Invalid ZIP local header')
    name, extra = struct.unpack_from('<HH', header, 26)
    return entry.header_offset + 30 + name + extra


def build_delta(baseline, target, output):
    baseline, target, output = map(Path, (baseline, target, output))
    operations = []
    with zipfile.ZipFile(baseline) as old_zip, zipfile.ZipFile(target) as new_zip, \
            baseline.open('rb') as old, target.open('rb') as new, \
            zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as patch:
        previous = {entry.filename: entry for entry in old_zip.infolist()}
        cursor = 0

        def literal(start, end):
            if end <= start:
                return
            name = 'data/' + str(len(operations))
            new.seek(start)
            patch.writestr(name, new.read(end - start))
            operations.append(['data', name, end - start])

        for entry in sorted(new_zip.infolist(), key=lambda item: item.header_offset):
            prior = previous.get(entry.filename)
            if (prior is not None and prior.compress_type == zipfile.ZIP_DEFLATED
                    and entry.compress_type == zipfile.ZIP_STORED
                    and (prior.CRC, prior.file_size) == (entry.CRC, entry.file_size)
                    and old_zip.read(prior) == new_zip.read(entry)):
                start = data_offset(new, entry)
                literal(cursor, start)
                operations.append(['inflate', entry.filename, entry.file_size])
                cursor = start + entry.compress_size
                continue
            if prior is None or (prior.CRC, prior.compress_size, prior.compress_type) != (
                    entry.CRC, entry.compress_size, entry.compress_type):
                continue
            start = data_offset(new, entry)
            old_start = data_offset(old, prior)
            old.seek(old_start)
            new.seek(start)
            if old.read(prior.compress_size) != new.read(entry.compress_size):
                continue
            literal(cursor, start)
            operations.append(['copy', old_start, entry.compress_size])
            cursor = start + entry.compress_size
        literal(cursor, target.stat().st_size)
        meta = dict(format='jgbol-apk-copy-v1', base_sha256=sha256(baseline),
                    target_sha256=sha256(target), target_size=target.stat().st_size,
                    operations=operations)
        patch.writestr('patch.json', json.dumps(meta, separators=(',', ':')))
    return meta
