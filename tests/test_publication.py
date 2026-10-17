"""Offline documentation and publication checks; no account or network access."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def test_readme_language_navigation(self):
        en = (ROOT / 'README.md').read_text(encoding='utf-8')
        ja = (ROOT / 'README.ja.md').read_text(encoding='utf-8')
        self.assertIn('[日本語](README.ja.md)', '\n'.join(en.splitlines()[:5]))
        self.assertIn('[English](README.md)', '\n'.join(ja.splitlines()[:5]))
        self.assertIn('remain in Japanese', en)

    def test_readme_commands_match(self):
        pattern = r'^```(?:bash|json)\n(.*?)^```'
        en = re.findall(pattern, (ROOT / 'README.md').read_text(encoding='utf-8'), re.M | re.S)
        ja = re.findall(pattern, (ROOT / 'README.ja.md').read_text(encoding='utf-8'), re.M | re.S)
        self.assertGreater(len(en), 5)
        self.assertEqual(en, ja)

    def test_local_markdown_links_exist(self):
        # Validate file destinations, not external URLs or platform-generated anchors.
        names = ['README.md', 'README.ja.md', 'THIRD_PARTY.md', 'CHANGELOG.md', 'TEST_REPORT.md']
        for name in names:
            path = ROOT / name
            text = re.sub(r'^```.*?^```', '', path.read_text(encoding='utf-8'), flags=re.M | re.S)
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                parsed = urlsplit(target.strip())
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                local = path.parent / unquote(parsed.path)
                with self.subTest(document=name, target=target):
                    self.assertTrue(local.exists(), f'Missing relative link: {local}')

    def test_publication_files_present(self):
        for name in ['LICENSE', 'NOTICE', 'README.md', 'README.ja.md', 'THIRD_PARTY.md',
                     'CHANGELOG.md', 'TEST_REPORT.md', 'VERSION', '.gitignore']:
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())
                self.assertGreater((ROOT / name).stat().st_size, 0)

    def test_full_apache_license_text(self):
        # Full unmodified Apache-2.0 text, including its standard application appendix.
        canonical = 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
        text = (ROOT / 'LICENSE').read_bytes().replace(b'\r\n', b'\n')
        self.assertEqual(hashlib.sha256(text).hexdigest(), canonical)
        notice = (ROOT / 'NOTICE').read_text(encoding='utf-8')
        self.assertIn('Slide Workspace contributors', notice)
        self.assertIn('Apache License, Version 2.0', notice)

    def test_package_metadata(self):
        data = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
        self.assertEqual(data['version'], (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(data['license'], 'Apache-2.0')
        self.assertIs(data['private'], True)  # Prevent npm publication, not GitHub visibility.


@unittest.skipUnless(shutil.which('git'), 'Git is needed to check Git ignore behavior')
class GitIgnoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='slide-publication-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copy2(ROOT / '.gitignore', self.root / '.gitignore')
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
        subprocess.run(['git', '-c', 'init.defaultBranch=main', 'init', '--quiet', str(self.root)],
                       check=True, capture_output=True, env=self.env)

    def ignored(self, name: str) -> bool:
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('Test fixture only\n', encoding='utf-8')
        result = subprocess.run(['git', '-C', str(self.root), 'check-ignore', '--no-index', '-q', '--', name],
                                capture_output=True, env=self.env)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode == 0

    def test_private_and_generated_files_ignored(self):
        for name in ['.env', '.env.local', '.claude/settings.local.json', '.claude.json',
                     '.claude.json.backup', 'CLAUDE.local.md', '.npmrc', '.pypirc', '.netrc',
                     '.DS_Store', 'Thumbs.db', '.setup/environment.txt', '.venv/bin/python',
                     'node_modules/example/index.js', 'projects/my-talk/inputs/source.pdf',
                     'projects/my-talk/outputs/talk-r01.pptx', 'projects/my-talk/CLAUDE.md',
                     'settings.json.bak-slide-workspace-test']:
            with self.subTest(name=name):
                self.assertTrue(self.ignored(name), name)

    def test_shared_source_and_templates_not_ignored(self):
        for name in ['CLAUDE.md', 'MAKE_SLIDES.md', 'START_PROMPT.md', 'README.md', 'README.ja.md',
                     'LICENSE', 'NOTICE', 'THIRD_PARTY.md', 'setup.sh', 'requirements.txt',
                     'package.json', 'package-lock.json', 'project-template/CLAUDE.md',
                     'project-template/talk-brief.md', 'project-template/inputs/README.md',
                     'project-template/inputs/assets/.gitkeep', 'projects/.gitkeep']:
            with self.subTest(name=name):
                self.assertFalse(self.ignored(name), name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
