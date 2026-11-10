"""Build a reviewed CurseForge export without vendoring third-party assets."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import io
import json
import re
import stat
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
LOCK = ROOT / 'baseline.lock.json'
ART_PATH = 'overrides/resourcepacks/Dane-Lords-Create-Aero-Quest-Art.zip'


def safe_path(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and '\\' not in name and not re.match(r'^[A-Za-z]:', name)


def validate_archive(archive):
    names = archive.namelist()
    if len(names) != len(set(names)):
        raise ValueError('Duplicate archive paths')
    for info in archive.infolist():
        if not safe_path(info.filename) or stat.S_ISLNK(info.external_attr >> 16):
            raise ValueError('Unsafe archive member')
    if archive.testzip() is not None:
        raise ValueError('Archive CRC failure')


def source_entries():
    entries = {}
    for base in (ROOT / 'overrides',):
        for path in sorted(base.rglob('*')):
            if path.is_symlink():
                raise ValueError('Source symlinks are not allowed')
            if path.is_file():
                name = path.relative_to(ROOT).as_posix()
                if not safe_path(name):
                    raise ValueError('Unsafe source path')
                entries[name] = path.read_bytes()
    for name in ('manifest.json', 'modlist.html'):
        entries[name] = (ROOT / name).read_bytes()
    return entries


def zip_bytes(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, payload in sorted(entries.items()):
            if not safe_path(name):
                raise ValueError('Unsafe output path')
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload)
    return output.getvalue()


def build(baseline, output=None):
    lock = json.loads(LOCK.read_text())
    raw = Path(baseline).read_bytes()
    if hashlib.sha256(raw).hexdigest() != lock['baseline']['sha256']:
        raise ValueError('Baseline SHA-256 mismatch; use the pinned CurseForge export')
    entries = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        validate_archive(archive)
        for item in lock['external_files']:
            name = item['path']
            if not safe_path(name):
                raise ValueError('Unsafe lock path')
            payload = archive.read(name)
            if len(payload) != item['size'] or hashlib.sha256(payload).hexdigest() != item['sha256']:
                raise ValueError('External payload mismatch')
            entries[name] = payload
        entries.update(source_entries())
        art_root = ROOT / 'resourcepack-src' / 'quest-art'
        art = {}
        for path in sorted(art_root.rglob('*')):
            if path.is_symlink():
                raise ValueError('Source symlinks are not allowed')
            if path.is_file():
                art[path.relative_to(art_root).as_posix()] = path.read_bytes()
        original_art = archive.read(ART_PATH)
        with zipfile.ZipFile(io.BytesIO(original_art)) as nested:
            validate_archive(nested)
            original = {i.filename: nested.read(i.filename) for i in nested.infolist() if not i.is_dir()}
        entries[ART_PATH] = original_art if art == original else zip_bytes(art)
    manifest = json.loads(entries['manifest.json'])
    if manifest.get('overrides') != 'overrides' or manifest.get('manifestType') != 'minecraftModpack':
        raise ValueError('Expected a CurseForge modpack manifest')
    destination = Path(output or ROOT / 'dist' / f'Create-Aero-{manifest["version"]}-source-build.zip')
    if destination.resolve() == Path(baseline).resolve():
        raise ValueError('Refusing to overwrite baseline')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(zip_bytes(entries))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Existing pinned CurseForge ZIP')
    parser.add_argument('--download', action='store_true', help='Download the pinned baseline into .cache/')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    baseline = args.baseline
    lock = json.loads(LOCK.read_text())
    if args.download:
        if baseline is not None:
            parser.error('Choose --baseline or --download, not both')
        baseline = ROOT / '.cache' / lock['baseline']['filename']
        baseline.parent.mkdir(parents=True, exist_ok=True)
        if not baseline.exists():
            with urllib.request.urlopen(lock['baseline']['url'], timeout=90) as response:
                raw = response.read()
            if hashlib.sha256(raw).hexdigest() != lock['baseline']['sha256']:
                raise ValueError('Downloaded baseline SHA-256 mismatch')
            baseline.write_bytes(raw)
    if baseline is None:
        parser.error('Supply --baseline FILE.zip or --download')
    result = build(baseline, args.output)
    print(result)
    print('SHA256', hashlib.sha256(result.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
