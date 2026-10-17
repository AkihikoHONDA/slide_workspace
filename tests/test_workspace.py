"""Offline tests. No sudo, downloads, Claude authentication, or model calls."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('configure_claude', ROOT / 'scripts/configure_claude.py')
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class UserSettingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='slide-settings-')
        self.addCleanup(self.tmp.cleanup)
        self.settings = Path(self.tmp.name) / '.claude/settings.json'

    def configure(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return mod.configure(self.settings)

    def write(self, text):
        self.settings.parent.mkdir(parents=True, exist_ok=True)
        self.settings.write_text(text, encoding='utf-8')

    def test_fresh_defaults(self):
        self.configure()
        self.assertEqual(json.loads(self.settings.read_text()), {
            'model': 'opus', 'effortLevel': 'high', 'permissions': {'defaultMode': 'auto'}})
        self.assertEqual(self.settings.stat().st_mode & 0o777, 0o600)

    def test_idempotent_no_extra_backup(self):
        self.configure()
        before = self.settings.stat().st_mtime_ns
        self.configure()
        self.assertEqual(self.settings.stat().st_mtime_ns, before)
        self.assertEqual(list(self.settings.parent.glob('*.bak-*')), [])

    def test_preserves_existing_choices_and_rules(self):
        original = {'model': 'sonnet', 'effortLevel': 'medium',
                    'permissions': {'defaultMode': 'default', 'deny': ['Read(./secret)']},
                    'enabledPlugins': {'example@market': True}, 'autoMemoryEnabled': False}
        self.write(json.dumps(original))
        self.assertEqual(self.configure(), original)

    def test_adds_missing_fields_with_backup(self):
        text = '{"permissions":{"deny":["Read(./secret)"]}}\n'
        self.write(text)
        data = self.configure()
        backups = list(self.settings.parent.glob('*.bak-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), text)
        self.assertEqual(data['permissions']['deny'], ['Read(./secret)'])
        self.assertEqual(data['permissions']['defaultMode'], 'auto')

    def test_invalid_json_no_write(self):
        for bad in ('{broken', '[]', '{"permissions": null}'):
            self.write(bad)
            with self.assertRaises(ValueError):
                self.configure()
            self.assertEqual(self.settings.read_text(), bad)

    def test_no_bypass_env_or_hooks(self):
        data = self.configure()
        self.assertNotIn('hooks', data)
        self.assertNotIn('env', data)
        self.assertNotIn('allow', data['permissions'])
        self.assertNotIn('additionalDirectories', data['permissions'])


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='slide workspace 日本語 ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'workspace with spaces'
        self.root.mkdir()
        shutil.copy2(ROOT / 'new-project.sh', self.root)
        shutil.copytree(ROOT / 'project-template', self.root / 'project-template')

    def run_project(self, *args):
        return subprocess.run(['bash', str(self.root / 'new-project.sh'), *args],
                              capture_output=True, text=True)

    def test_create_and_repeat_does_not_overwrite(self):
        first = self.run_project('my-talk')
        self.assertEqual(first.returncode, 0, first.stderr)
        project = self.root / 'projects/my-talk'
        for name in ['talk-brief.md', 'CLAUDE.md', 'inputs/assets', 'work', 'outputs']:
            self.assertTrue((project / name).exists(), name)
        brief = project / 'talk-brief.md'
        brief.write_text('My edited brief')
        second = self.run_project('my-talk')
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(brief.read_text(), 'My edited brief')
        self.assertFalse((project / '.venv').exists())
        self.assertFalse((project / 'node_modules').exists())

    def test_invalid_names(self):
        for bad in ['../escape', '/tmp/escape', '.hidden', 'with space', 'a/b', '--resume']:
            with self.subTest(name=bad):
                result = self.run_project(bad)
                self.assertNotEqual(result.returncode, 0)

    def test_help_and_extra_arg(self):
        self.assertEqual(self.run_project('--help').returncode, 0)
        self.assertNotEqual(self.run_project('my-talk', '--resume').returncode, 0)

    def test_creation_does_not_launch_claude(self):
        # No Claude is needed in the temporary workspace, and the script has no invocation.
        source = (self.root / 'new-project.sh').read_text()
        self.assertNotIn('exec claude', source)
        self.assertNotIn('source .venv', source)
        self.assertNotIn('setup.sh"', source)


class BundleTests(unittest.TestCase):
    def test_shell_syntax(self):
        for script in ['setup.sh', 'new-project.sh']:
            subprocess.run(['bash', '-n', str(ROOT / script)], check=True)

    def test_no_obsolete_launcher_or_config(self):
        for name in ['start.sh', 'config.sh', 'scripts/env.sh']:
            self.assertFalse((ROOT / name).exists(), name)

    def test_policy_entry_points(self):
        root_instructions = (ROOT / 'CLAUDE.md').read_text()
        self.assertIn('@MAKE_SLIDES.md', root_instructions)
        self.assertIn('@.setup/ENVIRONMENT.md', root_instructions)
        self.assertIn('@talk-brief.md', (ROOT / 'project-template/CLAUDE.md').read_text())
        self.assertNotIn('SLIDES_WORKSPACE', (ROOT / 'MAKE_SLIDES.md').read_text())
        self.assertNotIn('起動時に有効化済み', (ROOT / 'START_PROMPT.md').read_text())

    def test_setup_rejects_root(self):
        import os
        if os.geteuid() != 0:
            self.skipTest('root guard is exercised only when tests run as root')
        p = subprocess.run(['bash', str(ROOT / 'setup.sh')], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('sudoを付けず', p.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
