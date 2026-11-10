"""Persistent, role-scoped quarantine for time rewards (not an anti-root system)."""
import copy
from contextvars import ContextVar
from functools import wraps
import hashlib
import hmac
import inspect
import json
import secrets
from pathlib import Path

VERSION = 1
MESSAGE = '系统时间或存档时间记录异常，异常编号：TIME-001'
_preview = ContextVar('time_guard_preview', default=False)
TIME_KEYS = {'clock', 'day', 'shop_day', 'rank_day', 'strength_day', 'start_day',
             'week_start_day', 'week', 'shop_week', 'last_rank_week'}


def timeline(value):
    if isinstance(value, dict):
        result = {}
        for raw, v in sorted(value.items(), key=lambda pair: str(pair[0])):
            k = str(raw)
            child = v if k in TIME_KEYS or k.endswith(('_clock', '_recovery_at')) else timeline(v)
            if child != {} and child != []:
                result[k] = child
        return result
    if isinstance(value, list):
        return [child for v in value if (child := timeline(v))]
    return {}


def canonical(scope):
    # These legacy activities share daily counters in activity.prepare.
    shared = {'rank', 'feed', 'visit', 'pray', 'party', 'trial', 'convert',
              'practice', 'drug', 'duty', 'rape'}
    if scope in {'activity_' + name for name in shared}:
        return 'activity'
    if scope in {'activity_moon', 'activity_rice', 'activity_food'}:
        return 'activity_seasonal'
    if scope in {'activity_spring', 'activity_caishen', 'activity_tangwang'}:
        return 'activity_spring'
    if scope and scope.startswith('guild_'):
        return 'guild'
    for parent in ('babel', 'home', 'land', 'abyss', 'hunt', 'rape'):
        if scope and scope.startswith('activity_' + parent + '_'):
            return canonical('activity_' + parent)
    return scope


def blocked(role, scope):
    if scope is None:
        return False
    scopes = role.get('time_guard', {}).get('blocked', [])
    if not scopes:
        return False
    scopes = [canonical(s) for s in scopes]
    scope = canonical(scope)
    return '*' in scopes or scope in scopes or (scope.startswith('activity_') and 'activity' in scopes)


def require(role, scope):
    if blocked(role, scope) and not _preview.get():
        from .formation import Rejected
        raise Rejected(MESSAGE)


def protect(namespace):
    """Blocked maintenance runs on an isolated projection; it cannot pay rewards.

    Every role-taking function is covered, including helpers called from other
    features. Explicit action entry points reject before touching the role.
    """
    module = namespace['__name__']
    scope = module.rsplit('.', 1)[-1]
    if scope.startswith('guild_'):
        scope = 'guild'
    # Helper modules belong to their parent activity.
    for parent in ('babel', 'home', 'land', 'abyss', 'hunt', 'rape'):
        if scope.startswith('activity_' + parent + '_'):
            scope = 'activity_' + parent
    def decorate(fn):
        signature = inspect.signature(fn)
        @wraps(fn)
        def wrapped(*args, **kwargs):
            role = args[0] if args else kwargs.get('role')
            if scope == 'welfare' and (fn.__name__ == 'mail_request' or
                    (fn.__name__ == 'settle' and (args[1] if len(args) > 1 else kwargs.get('mid')) in (1102, 1103))):
                return fn(*args, **kwargs)
            if not isinstance(role, dict) or _preview.get() or not blocked(role, scope):
                return fn(*args, **kwargs)
            if fn.__name__.startswith(('settle', 'use_', 'claim', 'battle', 'move', 'fight', 'buy', 'panic_buy')):
                require(role, scope)
            bound = signature.bind(*args, **kwargs)
            # Copy all arguments together to preserve aliases (role + nested state).
            bound.arguments = copy.deepcopy(bound.arguments)
            if 'now' in signature.parameters:
                bound.arguments['now'] = role['time_guard']['since']
            token = _preview.set(True)
            try:
                return fn(*bound.args, **bound.kwargs)
            finally:
                _preview.reset(token)
        return wrapped
    for name, fn in list(namespace.items()):
        if inspect.isfunction(fn) and fn.__module__ == module:
            params = list(inspect.signature(fn).parameters)
            limited = {
                'summon': {'prepare', 'remaining', 'settle'},
                'market': {'prepare', 'catalog', 'panic_snapshot', 'buy', 'panic_buy'},
                'equipment_crafting': {'prepare_week', 'compose_list', 'settle'},
            }
            if scope in limited and name not in limited[scope]:
                continue
            if params and params[0] == 'role':
                namespace[name] = decorate(fn)


def mail_scope(key):
    for prefix, scope in (('nine-sky', 'nine_sky'), ('save-monkey', 'save_monkey'),
                          ('land-week', 'land'), ('pavilion', 'pavilion'),
                          ('hunt', 'hunt'), ('babel', 'babel'), ('home', 'home'),
                          ('caishen', 'caishen'), ('fish', 'fish'), ('duty', 'duty'),
                          ('abyss', 'abyss'), ('monday', 'monday'), ('tangwang', 'tangwang'),
                          ('party', 'party'), ('moon-recycle-', 'seasonal'),
                          ('rice-recycle-', 'seasonal')):
        if key.startswith(prefix):
            return 'activity_' + scope
    if key == 'anniversary':
        return 'welfare'
    if key.startswith('guild-'):
        return 'guild'
    return None


class Guard:
    def __init__(self, db, directory):
        self.db = db
        db.execute('CREATE TABLE IF NOT EXISTS time_guard (account TEXT PRIMARY KEY, data TEXT NOT NULL, seal TEXT NOT NULL)')
        path = Path(directory) / 'time_guard.key'
        if not path.exists():
            if db.execute('SELECT 1 FROM time_guard LIMIT 1').fetchone():
                raise RuntimeError('时间校验密钥缺失，请恢复完整备份')
            try:
                with path.open('xb') as stream:
                    stream.write(secrets.token_bytes(32))
                path.chmod(0o600)
            except FileExistsError:
                pass
        self.key = path.read_bytes()
        if len(self.key) != 32:
            raise RuntimeError('时间校验密钥无效')
        db.commit()

    def seal(self, account, data):
        return hmac.new(self.key, (account + '\0' + data).encode(), hashlib.sha256).hexdigest()

    def load(self, account, role, now, *, clock_blocked=False):
        row = self.db.execute('SELECT data,seal FROM time_guard WHERE account=?', (account,)).fetchone()
        if row is None:
            # Wall dates / future timestamps alone never establish illicit gain.
            info = dict(version=VERSION, status='legacy_unverified', blocked=[], since=now,
                        reason='旧存档无可信收益流水，保留原有进度')
        else:
            data, seal = row
            valid = hmac.compare_digest(self.seal(account, data), seal)
            record = json.loads(data) if valid else {}
            info = record.get('guard', {})
            if valid and record.get('timeline') == timeline(role) and (not clock_blocked or '*' in info.get('blocked', [])):
                role['time_guard'] = info
                return info
            if not valid or record.get('timeline') != timeline(role):
                info = dict(version=VERSION, status='blocked', blocked=['*'], since=now,
                            reason='升级后的受保护时间记录与校验记录不一致', code='TIME-001')
        if clock_blocked or (row is None and role.get('time_guard')):
            info = dict(version=VERSION, status='blocked', blocked=['*'], since=now,
                        reason='系统时间跳变、共享时钟被修改或已迁移角色的校验记录丢失', code='TIME-001')
        role['time_guard'] = info
        # Commit quarantine before gameplay, including failed/rejected requests.
        self.checkpoint(account, role)
        self.db.commit()
        return info

    def enforce(self, account, role):
        row = self.db.execute('SELECT data,seal FROM time_guard WHERE account=?', (account,)).fetchone()
        if row and hmac.compare_digest(self.seal(account, row[0]), row[1]):
            role['time_guard'] = json.loads(row[0])['guard']

    def checkpoint(self, account, role):
        data = json.dumps(dict(guard=role['time_guard'], timeline=timeline(role)), sort_keys=True, ensure_ascii=False)
        self.db.execute('INSERT OR REPLACE INTO time_guard VALUES (?,?,?)',
                        (account, data, self.seal(account, data)))

    def confirm(self, account, scopes, evidence, now):
        """Operator-only: reviewed evidence, never accepted from game requests."""
        allowed = {'*', 'activity', 'daily', 'welfare', 'guild', 'market', 'summon', 'xianling', 'equipment_crafting'} | {p.stem for p in Path(__file__).parent.glob('activity*.py')}
        if not evidence.strip() or not scopes or not set(scopes) <= allowed:
            raise ValueError('必须提供已复核的异常收益证据和活动范围')
        row = self.db.execute('SELECT data FROM roles WHERE account=?', (account,)).fetchone()
        if row is None:
            raise ValueError('角色不存在')
        role = json.loads(row[0])
        self.load(account, role, now)
        info = role['time_guard']
        if not info['blocked']:
            info['since'] = now
        info.update(status='blocked', blocked=sorted(set(info['blocked']) | {canonical(scope) for scope in scopes}),
                    reason=evidence, code='TIME-001')
        with self.db:
            self.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(role, ensure_ascii=False), account))
            self.checkpoint(account, role)
        return info


def request_scope(mid, req):
    scopes = {1353:'babel',1346:'save_monkey',1325:'dream',1309:'nine_sky',
              1351:'rulai',1334:'yuanshi',1226:'hunt',1227:'pavilion',1219:'monday',
              1243:'monday',1350:'arena',1043:'duty',1029:'rape',1041:'rape',
              1060:'rape',1072:'rape',1021:'rank',1203:'rank',1208:'fish',
              1210:'spring',1211:'spring',1213:'spring',1329:'abyss',1303:'land',
              1302:'land',1348:'home',1349:'undergo',1064:'trial',1202:'party',
              1040:'feed',1030:'visit',1085:'pray'}
    scope = scopes.get(mid)
    if mid == 1026:
        scope = {2:'rank',3:'rape',12:'rape',5:'duty'}.get(req.get('fight_type'), 'trial')
    if mid == 1051:
        scope = {1363:'home',1243:'nine_sky',1367:'rulai',1368:'rulai',1808:'yuanshi',
                 1036:'hunt',1037:'hunt',1324:'hunt',1021:'rank'}.get(req.get('item_type'), 'seasonal')
    if mid == 1201:
        scope = 'rank' if req.get('flag') == 2 else 'party'
    return 'activity_' + scope if scope else 'activity'
