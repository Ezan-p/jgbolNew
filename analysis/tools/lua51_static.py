"""Read Lua 5.1 chunks as data; never execute client code."""
import struct
import json

OPS = ('MOVE LOADK LOADBOOL LOADNIL GETUPVAL GETGLOBAL GETTABLE SETGLOBAL '
       'SETUPVAL SETTABLE NEWTABLE SELF ADD SUB MUL DIV MOD POW UNM NOT LEN '
       'CONCAT JMP EQ LT LE TEST TESTSET CALL TAILCALL RETURN FORLOOP FORPREP '
       'TFORLOOP SETLIST CLOSE CLOSURE VARARG').split()

class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 12
        assert data[:12] == bytes.fromhex('1b4c75615100010404040800'), data[:12].hex()

    def read(self, n):
        b = self.data[self.pos:self.pos+n]
        assert len(b) == n
        self.pos += n
        return b

    def u32(self): return struct.unpack('<I', self.read(4))[0]
    def byte(self): return self.read(1)[0]
    def string(self):
        n = self.u32()
        return self.read(n)[:-1].decode('utf8', 'replace') if n else None

    def proto(self):
        p = {'offset': self.pos, 'source': self.string(), 'line': self.u32(), 'last_line': self.u32()}
        p.update(zip(('nups', 'params', 'vararg', 'stack'), self.read(4)))
        p['code'] = [self.u32() for _ in range(self.u32())]
        p['constants'] = []
        for _ in range(self.u32()):
            t = self.byte()
            if t == 0: v = None
            elif t == 1: v = bool(self.byte())
            elif t == 3: v = struct.unpack('<d', self.read(8))[0]
            elif t == 4: v = self.string()
            else: raise ValueError(t)
            p['constants'].append(v)
        p['protos'] = [self.proto() for _ in range(self.u32())]
        p['lines'] = [self.u32() for _ in range(self.u32())]
        p['locals'] = [{'name': self.string(), 'start': self.u32(), 'end': self.u32()} for _ in range(self.u32())]
        p['upvalues'] = [self.string() for _ in range(self.u32())]
        return p

def parse(data):
    r = Reader(data)
    p = r.proto()
    assert r.pos == len(data), (r.pos, len(data))
    return p

def walk(p, path='main'):
    yield path, p
    for i, child in enumerate(p['protos']):
        yield from walk(child, path + '.' + str(i))

def decode(i):
    return i & 63, (i >> 6) & 255, (i >> 23) & 511, (i >> 14) & 511, i >> 14

def listing(p):
    out = []
    for path, f in walk(p):
        out.append(f'FUNCTION {path} offset=0x{f["offset"]:x} source_lines={f["line"]}-{f["last_line"]} params={f["params"]}')
        out.append('LOCALS ' + json.dumps(f['locals'], ensure_ascii=False))
        k = f['constants']
        rk = lambda n: ('K' + str(n-256) + '=' + repr(k[n-256])) if n >= 256 else 'R' + str(n)
        for pc, i in enumerate(f['code']):
            op, a, b, c, bx = decode(i)
            name = OPS[op]
            extra = ''
            if name in ('LOADK', 'GETGLOBAL', 'SETGLOBAL'): extra = repr(k[bx])
            elif name in ('GETTABLE', 'SELF'): extra = 'R%d %s' % (b, rk(c))
            elif name in ('SETTABLE', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'EQ', 'LT', 'LE'): extra = rk(b) + ' ' + rk(c)
            elif name == 'CLOSURE': extra = path + '.' + str(bx)
            elif name in ('JMP', 'FORLOOP', 'FORPREP'): extra = 'target=' + str(pc + 2 + bx - 131071)
            line = f['lines'][pc] if pc < len(f['lines']) else '?'
            out.append(f'{pc+1:05d} [L{line}] {name:10s} A={a} B={b} C={c} {extra}')
        out.append('')
    return '\n'.join(out)
