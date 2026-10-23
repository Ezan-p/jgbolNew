from pathlib import Path
import unittest

from fetch_server_list import parse_server_list
from analysis.tools.patch_server_list import patch
from analysis.tools.luajit_static import parse, decode

ROOT = Path(__file__).resolve().parents[1]
VALID = b'''-- comments and notices may contain numbers
version=1263, notices={ [1]={title="maintenance",content="id=999"} },
{ {id=803,ip="123.103.22.249",port=9510,name="server",status=1} }
'''


class ServerListTests(unittest.TestCase):
    def test_parse_nested_data_and_ignore_comment_ids(self):
        version, servers, notices = parse_server_list(VALID)
        self.assertEqual(version, 1263)
        self.assertEqual([s['id'] for s in servers], [803])
        self.assertEqual(notices[1]['content'], 'id=999')

    def test_reject_executable_expression(self):
        with self.assertRaises(ValueError):
            parse_server_list(VALID.replace(b'name="server"', b'name=os.execute("false")'))

    def test_reject_invalid_endpoint_and_duplicate_fields(self):
        for data in (VALID.replace(b'port=9510', b'port=99999'),
                     VALID.replace(b'id=803,', b'id=803,id=804,')):
            with self.subTest(data=data), self.assertRaises(ValueError):
                parse_server_list(data)

    def test_reject_404_html(self):
        with self.assertRaises(Exception):
            parse_server_list(b'<html>404 Not Found</html>')

    def test_bytecode_changes_only_list_directory_and_branch(self):
        path = ROOT / 'jgbol3.87/assets/release_/771ef5cb7d6e7c013cbb305c6fcad41c.data'
        original = path.read_bytes()
        updated = patch(original)
        before, after = parse(original), parse(updated)
        changed = []
        for old, new in zip(before['protos'], after['protos']):
            if old['code'] != new['code'] or old['kgc'] != new['kgc']:
                changed.append(new)
        self.assertEqual(len(changed), 1)
        target = changed[0]
        self.assertEqual((target['line'], target['last_line']), (158, 190))
        self.assertEqual(target['kgc'][8], 'p360_a/')
        op, a, b, c, d = decode(target['code'][30])
        self.assertEqual(op, 'JMP')
        self.assertEqual(31 + 1 + d - 32768, 54)
        self.assertEqual(path.read_bytes(), original)
        with self.assertRaises(ValueError):
            patch(updated)  # Refuse an already modified or unrecognized baseline.


if __name__ == '__main__':
    unittest.main()
