"""Redirect only downloadServerList's directory from p360_na to p360_a.

Edits the existing LuaJIT 2.0 dump without executing it. Channel identity and
login/update/payment methods are untouched. Original input files stay read-only.
"""
import struct

from .luajit_static import Reader, OPS, parse, decode


def uleb(value):
    result = bytearray()
    while value >= 128:
        result.append((value & 127) | 128)
        value >>= 7
    result.append(value)
    return bytes(result)


def patch(data):
    parsed = parse(data)
    matches = [p for p in parsed['protos'] if (p['line'], p['last_line']) == (158, 190)]
    if len(matches) != 1:
        raise ValueError('无法唯一定位原始 downloadServerList 函数')
    target = matches[0]
    expected = [(29, 'KSTR', 0, 8), (30, 'GGET', 1, 9), (53, 'GGET', 2, 9)]
    for pc, op, a, d in expected:
        actual = decode(target['code'][pc])
        if (actual[0], actual[1], actual[4]) != (op, a, d):
            raise ValueError('下载函数指令与已验证的 3.87 基线不符')
    if target['kgc'][8] != '' or target['kgc'][14] != 'getThirdPartyName':
        raise ValueError('下载函数常量与基线不符')

    r = Reader(data)
    r.read(4)
    flags = r.uleb()
    if flags & 1:
        raise ValueError('本补丁仅支持本项目的小端字节码')
    if not flags & 2:
        r.read(r.uleb())
    output = bytearray(data[:r.pos])
    changed = 0
    while True:
        size_start = r.pos
        size = r.uleb()
        if not size:
            output.extend(data[size_start:])
            break
        body_start = r.pos
        body = r.read(size)
        if body_start != target['offset']:
            output.extend(data[size_start:r.pos])
            continue
        h = Reader(body)
        header = h.read(4)
        ng, nn, ni = h.uleb(), h.uleb(), h.uleb()
        nd = 0 if flags & 2 else h.uleb()
        if nd:
            h.uleb()
            h.uleb()
        code_start = h.pos
        h.read(ni * 4 + header[3] * 2)
        constant_span = None
        for reverse_index in range(ng):
            start = h.pos
            kind = h.uleb()
            if kind >= 5:
                h.read(kind - 5)
            elif kind == 1:
                h.ktab()
            elif kind != 0:
                for _ in range(4 if kind == 4 else 2):
                    h.uleb()
            if ng - reverse_index - 1 == 8:
                if kind != 5:
                    raise ValueError('目标常量不是空字符串')
                constant_span = (start, h.pos)
        if constant_span is None:
            raise ValueError('缺少目标目录常量')
        modified = bytearray(body)
        # PC 30 initializes R0 to the directory. PC 31 then skips channel-name
        # construction and resumes the original URL builder at PC 54.
        instruction = OPS.index('JMP') | (1 << 8) | ((32768 + 22) << 16)
        struct.pack_into('<I', modified, code_start + 30 * 4, instruction)
        start, end = constant_span
        directory = b'p360_a/'
        modified[start:end] = uleb(5 + len(directory)) + directory
        output.extend(uleb(len(modified)))
        output.extend(modified)
        changed += 1
    if changed != 1:
        raise ValueError('函数补丁数量不符')
    result = bytes(output)
    updated = parse(result)
    # Compare every function's instructions/constants, allowing only these two
    # deliberately changed values; offsets naturally shift after the new string.
    for old, new in zip(parsed['protos'], updated['protos']):
        expected_code = list(old['code'])
        expected_constants = list(old['kgc'])
        if old['id'] == target['id']:
            expected_code[30] = instruction
            expected_constants[8] = 'p360_a/'
        if new['code'] != expected_code or new['kgc'] != expected_constants:
            raise ValueError('检测到预期之外的字节码修改')
    return result
