"""3.87 coupon protocol [A]; local issuance and eligibility policy [B]."""
import json
import re
from pathlib import Path

from . import daily, formation, journey, summon

RULES = Path(__file__).resolve().parents[1] / 'server_config/gift_code_rules.json'
CODE = re.compile(r'[A-Z0-9-]{1,18}', re.ASCII)


def load_rules(path=RULES):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    validate(rules)
    return rules


def validate(rules):
    require = formation.require
    require(rules['schema_version'] == 1 and rules['mode'] == 'inferred', '兑换码配置版本无效')
    require(isinstance(rules['revision'], str) and bool(rules['revision']), '兑换码配置修订号无效')
    require(isinstance(rules['platform'], str) and bool(rules['platform']), '兑换平台无效')
    seen = set()
    for row in rules['codes']:
        require(isinstance(row['code'], str) and CODE.fullmatch(row['code']) is not None, '兑换码须为1至18位大写字母、数字或连字符')
        require(row['code'] not in seen, '兑换码重复')
        seen.add(row['code'])
        require(isinstance(row['name'], str) and 0 < len(row['name']) <= 60, '礼包名称无效')
        require(isinstance(row['group'], str) and 0 < len(row['group']) <= 64, '礼包互斥组无效')
        require(type(row['enabled']) is bool and type(row['issued']) is bool, '礼包启用/发放状态无效')
        for key in ('starts_at', 'expires_at', 'max_uses'):
            require(type(row[key]) is int and row[key] >= 0, '礼包时间或次数无效')
        require(not row['expires_at'] or row['expires_at'] > row['starts_at'], '礼包有效期无效')
        for key in ('account', 'platform'):
            require(row.get(key) is None or isinstance(row[key], str) and bool(row[key]), '礼包绑定信息无效')
        for key in ('role_id', 'server_id'):
            require(row.get(key) is None or type(row[key]) is int and row[key] > 0, '礼包绑定编号无效')
        require(isinstance(row['prizes'], list) and 1 <= len(row['prizes']) <= 20, '礼包须含1至20项奖励')
        for prize in row['prizes']:
            daily.validate_prize(prize)


def initialize(db):
    # Shared across accounts and Backend instances in this database.
    db.execute('''CREATE TABLE IF NOT EXISTS gift_code_claims (
        code TEXT NOT NULL, account TEXT NOT NULL, gift_group TEXT NOT NULL,
        claimed_at INTEGER NOT NULL, revision TEXT NOT NULL, rewards TEXT NOT NULL,
        PRIMARY KEY(code, account), UNIQUE(account, gift_group))''')
    db.commit()


def response(result, flag=0, **fields):
    return summon.event(18, dict(result=result, client_flag=flag, **fields))


def settle(db, role, account, req, now, rules):
    """Caller holds BEGIN IMMEDIATE and commits ledger + role in one transaction."""
    flag = req['flag']
    if flag != 0:
        return 15, response(15, flag)
    code = req['sn'].strip().upper()
    row = next((r for r in rules['codes'] if r['code'] == code), None) if CODE.fullmatch(code) else None
    result = 1
    if row is None or not row['enabled']:
        result = 2
    elif not row['issued'] or now < row['starts_at']:
        result = 4
    elif row['expires_at'] and now >= row['expires_at']:
        result = 14
    elif row.get('account') is not None and row['account'] != account:
        result = 6
    elif row.get('role_id') is not None and row['role_id'] != role['role_id']:
        result = 7
    elif row.get('server_id') is not None and row['server_id'] != role['area_id']:
        result = 8
    elif row.get('platform') is not None and row['platform'] != rules['platform']:
        result = 9
    elif db.execute('SELECT 1 FROM gift_code_claims WHERE code=? AND account=?', (code, account)).fetchone():
        result = 13
    elif db.execute('SELECT 1 FROM gift_code_claims WHERE account=? AND gift_group=?', (account, row['group'])).fetchone():
        result = 12
    elif row['max_uses'] and db.execute('SELECT count(*) FROM gift_code_claims WHERE code=?', (code,)).fetchone()[0] >= row['max_uses']:
        result = 5
    if result != 1:
        return result, response(result, flag)
    prizes = [journey.grant(role, p) for p in row['prizes']]
    formation.require(all(0 <= role[k] <= 2147483647 for k in ('gold_coin', 'silver_coin')), '礼包货币超出协议上限')
    db.execute('INSERT INTO gift_code_claims VALUES (?,?,?,?,?,?)',
               (code, account, row['group'], now, rules['revision'], json.dumps(row['prizes'])))
    return 1, response(1, flag, name=row['name'], attach_count=len(prizes), attach_list=prizes)
