import io
import json
from pathlib import Path
import re
import tomllib
import unittest
import zipfile
import build

ROOT = Path(__file__).resolve().parent


class SourceTests(unittest.TestCase):
    def test_manifest_identity_and_loader(self):
        m = json.loads((ROOT / 'manifest.json').read_text())
        self.assertEqual(m['name'], "Dane Lord's Create Aero")
        self.assertEqual(m['version'], '1.3')
        self.assertEqual(m['minecraft']['version'], '1.21.1')
        self.assertEqual(m['minecraft']['modLoaders'], [{'id': 'neoforge-21.1.265', 'primary': True}])
        self.assertEqual(m['overrides'], 'overrides')

    def test_manifest_project_file_pairs(self):
        files = json.loads((ROOT / 'manifest.json').read_text())['files']
        self.assertEqual(len(files), 269)
        pairs = [(m['projectID'], m['fileID']) for m in files]
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertTrue(all(isinstance(a, int) and a > 0 and isinstance(b, int) and b > 0 for a, b in pairs))

    def test_baseline_lock(self):
        lock = json.loads(build.LOCK.read_text())
        self.assertEqual(lock['baseline']['sha256'], 'a8b75c71b4c7305fe7a6165a246af99ffa28be81760a061fc21382087450d828')
        paths = [item['path'] for item in lock['external_files']]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all(build.safe_path(n) for n in paths))
        self.assertTrue(all(re.fullmatch('[a-f0-9]{64}', item['sha256']) for item in lock['external_files']))

    def test_all_toml_parses(self):
        paths = list((ROOT / 'overrides').rglob('*.toml'))
        self.assertGreater(len(paths), 200)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                tomllib.loads(path.read_text(encoding='utf-8-sig'))

    def test_original_quest_chapters_and_unique_ids(self):
        quests = ROOT / 'overrides/config/ftbquests/quests'
        self.assertEqual(len(list((quests / 'chapters').glob('*.snbt'))), 13)
        self.assertEqual(len(list((quests / 'reward_tables').glob('*.snbt'))), 3)
        ids = []
        for path in quests.rglob('*.snbt'):
            ids.extend(re.findall(r'\bid\s*:\s*"([0-9A-F]{16})"', path.read_text()))
        self.assertGreater(len(ids), 500)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all('-' not in p.stem for p in (quests / 'chapters').glob('*.snbt')))

    def test_privacy_exclusions(self):
        names = set(build.source_entries()) | {item['path'] for item in json.loads(build.LOCK.read_text())['external_files']}
        bad_prefixes = ('overrides/config/CSC/backup/', 'overrides/config/CSC/Data/', 'overrides/config/CSC/Log/', 'overrides/config/CSC/online/', 'overrides/config/jei/world/', 'overrides/config/jei/server/', 'overrides/config/xaero/', 'overrides/config/e4mc/')
        self.assertFalse(any(n.startswith(bad_prefixes) or n.endswith(('.log', '.legacy', '.jar')) for n in names))
        self.assertNotIn('overrides/config/sodium-fingerprint.json', names)
        self.assertNotIn('servers.dat', names)

    def test_quest_art_format_and_files(self):
        art = ROOT / 'resourcepack-src/quest-art'
        self.assertEqual(json.loads((art / 'pack.mcmeta').read_text())['pack']['pack_format'], 34)
        self.assertTrue((art / 'pack.png').is_file())
        self.assertTrue((art / 'assets/create_aero/textures/quests/tutorial_header.png').is_file())

    def test_no_dependency_archives_in_source(self):
        self.assertFalse(list((ROOT / 'overrides').rglob('*.jar')))
        self.assertFalse(list((ROOT / 'overrides').rglob('*.zip')))

    def test_unsafe_paths_rejected(self):
        for name in ('../escape', '/absolute', 'a/../../escape', 'a\\b', 'C:/drive'):
            self.assertFalse(build.safe_path(name), name)
        with self.assertRaises(ValueError):
            build.zip_bytes({'../escape': b'x'})

    def test_duplicate_members_rejected(self):
        import warnings
        payload = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(payload, 'w') as archive:
                archive.writestr('same', b'a')
                archive.writestr('same', b'b')
        with zipfile.ZipFile(io.BytesIO(payload.getvalue())) as archive:
            with self.assertRaises(ValueError):
                build.validate_archive(archive)

    def test_deterministic_zip_bytes(self):
        a = build.zip_bytes({'z': b'last', 'a': b'first'})
        b = build.zip_bytes({'a': b'first', 'z': b'last'})
        self.assertEqual(a, b)
        with zipfile.ZipFile(io.BytesIO(a)) as archive:
            self.assertEqual(archive.namelist(), ['a', 'z'])
            self.assertIsNone(archive.testzip())


if __name__ == '__main__':
    unittest.main()
