import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from opening_patch.apply_patch import apply
from opening_patch.build_patch import build_delta


class OpeningPatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base, self.target, self.patch, self.output = [
            self.root / name for name in ('base.apk', 'target.apk', 'opening.patch', 'output.apk')]
        for path, version in ((self.base, b'102'), (self.target, b'103-new-startup')):
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('assets/unchanged', bytes(range(256)) * 512)
                archive.writestr('classes2.dex', version, compress_type=zipfile.ZIP_DEFLATED)
                archive.writestr('movie.mp4', b'unchanged movie' * 1000,
                                 compress_type=zipfile.ZIP_DEFLATED if path == self.base else zipfile.ZIP_STORED)
            with path.open('ab') as stream:
                stream.write(b'trailing data ' + version)
        build_delta(self.base, self.target, self.patch)

    def test_exact_bytes_with_compressed_entries_and_trailer(self):
        apply(self.base, self.patch, self.output)
        self.assertEqual(self.output.read_bytes(), self.target.read_bytes())
        self.assertLess(self.patch.stat().st_size, self.target.stat().st_size // 5)

    def test_wrong_base_is_rejected_without_output(self):
        self.base.write_bytes(b'wrong version')
        with self.assertRaisesRegex(ValueError, '不匹配'):
            apply(self.base, self.patch, self.output)
        self.assertFalse(self.output.exists())

    def test_compressed_movie_is_reused_as_playable_uncompressed_resource(self):
        with zipfile.ZipFile(self.patch) as archive:
            meta = json.loads(archive.read('patch.json'))
        self.assertIn(['inflate', 'movie.mp4', 15000], meta['operations'])
        apply(self.base, self.patch, self.output)
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(archive.getinfo('movie.mp4').compress_type, zipfile.ZIP_STORED)
            self.assertEqual(archive.read('movie.mp4'), b'unchanged movie' * 1000)

    def test_existing_output_and_source_are_never_overwritten(self):
        self.output.write_bytes(b'keep me')
        for destination in (self.output, self.base, self.patch):
            before = destination.read_bytes()
            with self.assertRaises(ValueError):
                apply(self.base, self.patch, destination)
            self.assertEqual(destination.read_bytes(), before)

    def rewrite_meta(self, transform):
        with zipfile.ZipFile(self.patch) as archive:
            files = {name: archive.read(name) for name in archive.namelist()}
        meta = json.loads(files['patch.json'])
        transform(meta)
        files['patch.json'] = json.dumps(meta).encode()
        with zipfile.ZipFile(self.patch, 'w') as archive:
            for name, data in files.items():
                archive.writestr(name, data)

    def test_bad_target_hash_leaves_no_partial_apk(self):
        self.rewrite_meta(lambda meta: meta.update(target_sha256='0' * 64))
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            apply(self.base, self.patch, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.opening-*')), [])

    def test_out_of_bounds_copy_is_rejected(self):
        self.rewrite_meta(lambda meta: meta['operations'].insert(0, ['copy', 10**9, 1]))
        with self.assertRaisesRegex(ValueError, '超出'):
            apply(self.base, self.patch, self.output)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
