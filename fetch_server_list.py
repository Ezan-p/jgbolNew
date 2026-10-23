"""Fetch the public game server list without starting a channel SDK.

Run with .runtime/venv/bin/python (uses the already installed luaparser).
Only Lua literal tables are read; downloaded Lua is never executed.
"""
from pathlib import Path
import argparse
import hashlib
import ipaddress
import json
from datetime import datetime
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from luaparser import ast, astnodes as nodes

ROOT = Path(__file__).resolve().parent
URL = 'http://jgbupdate02.shangyoo.com/update/jgb/p360_a/server_list.txt'


def literal(node):
    if isinstance(node, nodes.Table):
        values, index = {}, 1
        for field in node.fields:
            if field.key is None:
                key = index
                index += 1
            elif isinstance(field.key, nodes.Name):
                key = field.key.id
            else:
                key = literal(field.key)
            if key in values:
                raise ValueError('列表中存在重复字段：' + str(key))
            values[key] = literal(field.value)
        return values
    if isinstance(node, nodes.String):
        return node.s.decode('utf-8') if isinstance(node.s, bytes) else node.s
    if isinstance(node, nodes.Number):
        return node.n
    if isinstance(node, nodes.TrueExpr):
        return True
    if isinstance(node, nodes.FalseExpr):
        return False
    if isinstance(node, nodes.Nil):
        return None
    raise ValueError('列表含有非静态数据，拒绝解析：' + type(node).__name__)


def parse_server_list(data):
    # The game stores fields of an outer table rather than a standalone chunk.
    chunk = ast.parse('return {\n' + data.decode('utf-8-sig') + '\n}')
    statements = chunk.body.body
    if len(statements) != 1 or not isinstance(statements[0], nodes.Return):
        raise ValueError('不是静态服务器列表')
    table = literal(statements[0].values[0])
    groups = table.get(1)
    if not isinstance(groups, dict) or not groups:
        raise ValueError('服务器列表为空或格式不符')
    servers = list(groups.values())
    ids = set()
    for server in servers:
        if not isinstance(server, dict):
            raise ValueError('服务器条目格式不符')
        if type(server.get('id')) is not int or server['id'] in ids:
            raise ValueError('服务器 ID 无效或重复')
        ids.add(server['id'])
        ipaddress.ip_address(server['ip'])
        if type(server.get('port')) is not int or not 1 <= server['port'] <= 65535:
            raise ValueError('服务器端口无效')
        if not isinstance(server.get('name'), str):
            raise ValueError('服务器名称无效')
    return table.get('version'), servers, table.get('notices', {})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'analysis/server_lists')
    args = parser.parse_args()
    with urlopen(Request(URL, headers={'User-Agent': 'JGBOL-ServerList-Reader/1.0'}),
                 timeout=20) as response:
        if response.status != 200:
            raise RuntimeError('服务器列表 HTTP 状态：' + str(response.status))
        data = response.read(2 * 1024 * 1024 + 1)
        if len(data) > 2 * 1024 * 1024:
            raise ValueError('列表响应超过 2 MiB，拒绝处理')
        headers = dict(response.headers)
        final_url = response.url
    version, servers, notices = parse_server_list(data)
    document = {
        'source_url': URL,
        'resolved_url': final_url,
        'source_channel': 'p360_a (old 360 directory, Android mixed-server list)',
        'fetched_at': datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds'),
        'http_last_modified': headers.get('Last-Modified'),
        'sha256': hashlib.sha256(data).hexdigest(),
        'version': version,
        'count': len(servers),
        'live_server_status_verified': False,
        'notices': notices,
        'servers': servers,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'server_list.raw.txt').write_bytes(data)
    (args.output / 'server_list.json').write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    lines = [
        '金箍棒安卓混服服务器列表（旧 360 公开目录）',
        f'获取时间：{document["fetched_at"]}', f'来源：{URL}',
        f'服务端文件最后修改时间：{document["http_last_modified"]}',
        f'列表版本：{version}；服务器条目：{len(servers)}',
        '通过公开 HTTP 获取，无需渠道登录。未验证各服务器在线或账号可登录。',
        '名称中的“新服/爆满”以及 status 数值均为源文件内容，不代表当前状态。',
        '', 'ID | 名称 | 登录服地址 | 源状态值',
    ]
    for server in servers:
        lines.append(f'{server["id"]} | {server["name"]} | '
                     f'{server["ip"]}:{server["port"]} | {server.get("status", "")}')
    (args.output / '服务器列表.txt').write_text('\n'.join(lines) + '\n')
    print(f'已获取 {len(servers)} 条服务器记录（版本 {version}），无需渠道登录。')
    print(args.output / '服务器列表.txt')


if __name__ == '__main__':
    main()
