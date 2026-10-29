"""Reconstruct an exactly signed update APK using only Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile


def sha256(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def apply(baseline, patch, output):
    baseline, patch, output = map(Path, (baseline, patch, output))
    if output.resolve() in (baseline.resolve(), patch.resolve()) or output.exists():
        raise ValueError('输出已存在或与输入相同；请选择新文件名，不覆盖原包。')
    temporary = None
    try:
        with zipfile.ZipFile(patch) as archive:
            meta = json.loads(archive.read('patch.json'))
            if meta['format'] != 'jgbol-apk-copy-v1':
                raise ValueError('不支持的补丁格式')
            if sha256(baseline) != meta['base_sha256']:
                raise ValueError('原 APK 与补丁不匹配：需要未修改的离线单机 v102 APK。')
            output.parent.mkdir(parents=True, exist_ok=True)
            with baseline.open('rb') as source, tempfile.NamedTemporaryFile(
                    dir=output.parent, prefix='.opening-', suffix='.tmp', delete=False) as dest:
                temporary = Path(dest.name)
                total = 0
                for operation in meta['operations']:
                    kind, offset, size = operation
                    if size < 0 or total + size > meta['target_size']:
                        raise ValueError('补丁长度异常')
                    if kind == 'copy':
                        if offset < 0 or offset + size > baseline.stat().st_size:
                            raise ValueError('补丁引用超出原包范围')
                        source.seek(offset)
                        remaining = size
                        while remaining:
                            block = source.read(min(1024 * 1024, remaining))
                            if not block:
                                raise ValueError('原包读取不完整')
                            dest.write(block)
                            remaining -= len(block)
                    elif kind in ('data', 'inflate'):
                        # Resource compression can change without shipping the movie again.
                        original_zip = zipfile.ZipFile(baseline) if kind == 'inflate' else None
                        data_archive = original_zip if original_zip is not None else archive
                        try:
                            literal = data_archive.open(offset)
                            with literal:
                                remaining = size
                                while remaining:
                                    block = literal.read(min(1024 * 1024, remaining))
                                    if not block:
                                        raise ValueError('补丁数据不完整')
                                    dest.write(block)
                                    remaining -= len(block)
                                if literal.read(1):
                                    raise ValueError('补丁数据长度异常')
                        finally:
                            if original_zip is not None:
                                original_zip.close()
                    else:
                        raise ValueError('未知补丁操作')
                    total += size
                if total != meta['target_size']:
                    raise ValueError('输出长度校验失败')
            if sha256(temporary) != meta['target_sha256']:
                raise ValueError('输出 SHA256 校验失败，不生成 APK')
            temporary.replace(output)
            temporary = None
        return output
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='将原离线单机 v102 APK 合成为带开场动画的 v103 更新 APK')
    parser.add_argument('baseline', type=Path, help='原版离线单机 APK（不是 ZIP）')
    parser.add_argument('--patch', type=Path, default=Path(__file__).with_name('opening.patch'))
    parser.add_argument('--output', type=Path, default=Path('金箍棒3.87-开场动画更新-v103.apk'))
    args = parser.parse_args()
    try:
        print('已生成并校验：', apply(args.baseline, args.patch, args.output))
        print('将新 APK 复制到手机覆盖安装；不要卸载旧版或清除数据。')
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + '\n')
