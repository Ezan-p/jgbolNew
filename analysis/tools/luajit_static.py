"""Offline parser for LuaJIT 2.0 dump v1; never loads or executes Lua code.
Format references: https://github.com/LuaJIT/LuaJIT/blob/v2.0/src/lj_bcdump.h
and lj_bc.h / lj_bcread.c in the same official source tree.
"""
import struct
import json
import copy

OPS = '''ISLT ISGE ISLE ISGT ISEQV ISNEV ISEQS ISNES ISEQN ISNEN ISEQP ISNEP
ISTC ISFC IST ISF MOV NOT UNM LEN ADDVN SUBVN MULVN DIVVN MODVN
ADDNV SUBNV MULNV DIVNV MODNV ADDVV SUBVV MULVV DIVVV MODVV POW CAT
KSTR KCDATA KSHORT KNUM KPRI KNIL UGET USETV USETS USETN USETP UCLO FNEW
TNEW TDUP GGET GSET TGETV TGETS TGETB TSETV TSETS TSETB TSETM
CALLM CALL CALLMT CALLT ITERC ITERN VARG ISNEXT RETM RET RET0 RET1
FORI JFORI FORL IFORL JFORL ITERL IITERL JITERL LOOP ILOOP JLOOP JMP
FUNCF IFUNCF JFUNCF FUNCV IFUNCV JFUNCV FUNCC FUNCCW'''.split()

def string(b):
    try: return b.decode('utf8')
    except UnicodeDecodeError: return b.decode('gb18030', 'backslashreplace')

def signed(x): return x - 0x100000000 if x >= 0x80000000 else x

class Reader:
    def __init__(self, b): self.b, self.pos = b, 0
    def read(self, n):
        v = self.b[self.pos:self.pos+n]
        assert len(v) == n
        self.pos += n
        return v
    def byte(self): return self.read(1)[0]
    def uleb(self):
        v = shift = 0
        while True:
            b = self.byte(); v |= (b & 127) << shift
            if b < 128: return v
            shift += 7
            assert shift <= 35
    def num(self):
        lo, hi = self.uleb(), self.uleb()
        return struct.unpack('<d', struct.pack('<II', lo, hi))[0]
    def ktabk(self):
        t = self.uleb()
        if t >= 5: return string(self.read(t-5))
        if t == 3: return signed(self.uleb())
        if t == 4: return self.num()
        return [None,False,True][t]
    def ktab(self):
        na, nh = self.uleb(), self.uleb()
        tab = {}
        for i in range(na):
            v = self.ktabk()
            if v is not None: tab[i] = v
        for _ in range(nh):
            k, v = self.ktabk(), self.ktabk()
            assert k is not None
            tab[k] = v
        return {'kind':'table','value':tab}

def parse(b):
    r = Reader(b)
    assert r.read(4) == b'\x1bLJ\x01'
    flags = r.uleb()
    assert flags & ~7 == 0
    endian = '>' if flags & 1 else '<'
    source = None if flags & 2 else string(r.read(r.uleb()))
    protos, stack = [], []
    while True:
        size = r.uleb()
        if not size: break
        start = r.pos
        p = dict(zip(('flags','params','stack','nups'),r.read(4)))
        p.update({'offset':start,'source':source,'id':len(protos)})
        ng, nn, ni = r.uleb(), r.uleb(), r.uleb()
        nd = 0 if flags & 2 else r.uleb()
        first, span = (r.uleb(),r.uleb()) if nd else (0,0)
        p.update({'line':first,'last_line':first+span,'code':list(struct.unpack(endian+str(ni)+'I',r.read(ni*4)))})
        p['upvalue_refs'] = list(struct.unpack(endian+str(p['nups'])+'H',r.read(p['nups']*2)))
        kgc = []
        for _ in range(ng):
            t = r.uleb()
            if t >= 5: v = string(r.read(t-5))
            elif t == 0:
                assert stack
                v = {'kind':'proto','id':stack.pop()}
            elif t == 1: v = r.ktab()
            else: v = {'kind':'cdata','type':t,'words':[r.uleb() for _ in range(4 if t==4 else 2)]}
            kgc.append(v)
        p['kgc'] = kgc[::-1]
        p['numbers'] = []
        for _ in range(nn):
            v = r.uleb(); lo = v >> 1
            n = struct.unpack('<d',struct.pack('<II',lo,r.uleb()))[0] if v & 1 else signed(lo)
            p['numbers'].append(n)
        p['lines'],p['upvalues'] = [],[]
        if nd:
            dbg = Reader(r.read(nd)); width = 1 if span<256 else 2 if span<65536 else 4
            fmt={1:'B',2:'H',4:'I'}[width]
            p['lines'] = [first+x for x in struct.unpack(endian+str(ni)+fmt,dbg.read(ni*width))]
            for _ in range(p['nups']):
                end=dbg.b.index(0,dbg.pos);p['upvalues'].append(string(dbg.read(end-dbg.pos)));dbg.read(1)
            p['local_debug_hex'] = dbg.read(len(dbg.b)-dbg.pos).hex()
        assert r.pos == start+size,(r.pos,start,size)
        assert all((i & 255)<len(OPS)for i in p['code'])
        protos.append(p);stack.append(p['id'])
    assert r.pos==len(b) and len(stack)==1
    return {'source':source,'flags':flags,'root':stack[0],'protos':protos}

def decode(i): return OPS[i&255],(i>>8)&255,i>>24,(i>>16)&255,i>>16

def listing(chunk):
    out=['LuaJIT dump version=1; source='+repr(chunk['source'])+'; root=proto'+str(chunk['root'])]
    for p in chunk['protos']:
        out += ['',f'FUNCTION proto{p["id"]} offset=0x{p["offset"]:x} source_lines={p["line"]}-{p["last_line"]} params={p["params"]}', 'UPVALUES '+repr(p['upvalues'])]
        for pc,i in enumerate(p['code'],1):
            op,a,b,c,d=decode(i);extra=''
            if op in ('KSTR','KCDATA','TDUP','GGET','GSET','FNEW','ISEQS','ISNES','USETS'):extra=repr(p['kgc'][d])
            elif op in ('TGETS','TSETS'):extra=repr(p['kgc'][c])
            elif op in ('KNUM','ISEQN','ISNEN','USETN','TSETM'):extra=repr(p['numbers'][d])
            elif op=='KSHORT':extra=str(d if d<32768 else d-65536)
            elif op in ('UGET','USETV','USETS','USETN','USETP'):
                u=d if op=='UGET' else a;extra=p['upvalues'][u] if u<len(p['upvalues']) else '?'
            elif op in ('JMP','UCLO','FORI','FORL','ITERL','LOOP','ISNEXT'):extra='target='+str(pc+1+d-32768)
            line=p['lines'][pc-1]if p['lines']else '?'
            out.append(f'{pc:05d} [L{line}] {op:8s} A={a} B={b} C={c} D={d} {extra}')
    return '\n'.join(out)+'\n'

def static_tables(chunk):
    """Propagate only literal table construction in common.msg_def, no Lua calls."""
    p=chunk['protos'][chunk['root']];r={};g={};k=p['kgc'];n=p['numbers']
    fmt=lambda v:str(int(v))if isinstance(v,float)and v.is_integer()else str(v)
    for pc,ins in enumerate(p['code'],1):
        op,a,b,c,d=decode(ins)
        if op=='FNEW':break
        if op=='GGET':r[a]=g.get(k[d],'@'+k[d])
        elif op=='GSET':g[k[d]]=r[a]
        elif op=='KSTR':r[a]=k[d]
        elif op=='KNUM':r[a]=n[d]
        elif op=='KSHORT':r[a]=d if d<32768 else d-65536
        elif op=='KPRI':r[a]=[None,False,True][d]
        elif op=='KNIL':
            for j in range(a,d+1):r[j]=None
        elif op=='MOV':r[a]=r[d]
        elif op=='TNEW':r[a]={}
        elif op=='TDUP':r[a]=copy.deepcopy(k[d]['value'])
        elif op=='TGETS':r[a]=r[b][k[c]]
        elif op=='TGETB':r[a]=r[b][c]
        elif op=='TGETV':r[a]=r[b][r[c]]
        elif op=='TSETS':r[b][k[c]]=r[a]
        elif op=='TSETB':r[b][c]=r[a]
        elif op=='TSETV':r[b][r[c]]=r[a]
        elif op=='CAT':r[a]=''.join(fmt(r[j])for j in range(b,c+1))
        elif op=='CALL':assert r[a]=='@module'and r[a+1]=='common.msg_def'and b==1 and c==2
        else:raise ValueError((pc,op))
    return g
