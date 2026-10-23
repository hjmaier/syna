#!/usr/bin/env python3
"""Synthetic Hugo regression tests; uses Python's standard library only."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("--hugo", required=True, help="Path to a Hugo binary")
PARSER.add_argument("--theme-root", type=Path, default=Path(__file__).resolve().parents[2])
PARSER.add_argument("--artifacts", type=Path)

OPTIONS = None


class HugoCase(unittest.TestCase):
    def setUp(self):
        if OPTIONS.artifacts:
            self.root = OPTIONS.artifacts.resolve() / self.id().split(".")[-1]
            self.root.mkdir(parents=True, exist_ok=False)
        else:
            temp = tempfile.TemporaryDirectory(prefix="syna-hugo-")
            self.addCleanup(temp.cleanup)
            self.root = Path(temp.name)
        self.theme = OPTIONS.theme_root.resolve()

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def partial(self, path):
        target = self.root / "layouts/partials" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.theme / "layouts/partials" / path, target)

    def build(self, *args):
        command = [str(Path(OPTIONS.hugo).resolve()), "--source", str(self.root),
                   "--destination", str(self.root / "public"),
                   "--cacheDir", str(self.root / "cache"), "--ignoreCache", *args]
        env = {key: value for key, value in os.environ.items() if not key.startswith("HUGO_")}
        env.update(GOMAXPROCS="2", HUGO_RESOURCEDIR=str(self.root / "resources"))
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30)
        (self.root / "command.json").write_text(json.dumps(command, indent=2))
        (self.root / "build.log").write_text(result.stdout + result.stderr)
        (self.root / "build-result.json").write_text(json.dumps({
            "exit_code": result.returncode,
            "environment": {"GOMAXPROCS": "2", "HUGO_RESOURCEDIR": str(self.root / "resources")}
        }, indent=2))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result


class FragmentLanguageTests(HugoCase):
    def language_fixture(self):
        self.write("config.toml", '''baseURL = "https://example.invalid/"
defaultContentLanguage = "de"
defaultContentLanguageInSubdir = true
disableKinds = ["RSS", "sitemap", "taxonomy", "term", "taxonomyTerm"]
[languages.de]
weight = 1
[languages.en]
weight = 2
[params]
defaultContentLanguage = "de"
''')
        self.partial("helpers/fragments.html")
        self.partial("helpers/deprecation-warning.html")
        self.write("layouts/index.html", "Synthetic home.\n")
        self.write("layouts/_default/single.html", '''{{- .Scratch.Set "layout_info" (dict "root" . "real_page" . "page" .) -}}
{{- partial "helpers/fragments.html" (dict "page_scratch" .Scratch) -}}
{{- $markers := slice -}}
{{- range .Scratch.Get "page_fragments" -}}
  {{- $markers = $markers | append .Params.marker -}}
{{- end -}}
{{- $markers | jsonify -}}
''')
        for path, title in [("_index.md", "Deutsch"), ("_index.en.md", "English")]:
            self.write("content/" + path, '+++\ntitle = "' + title + '"\n+++\n')
        for suffix in ["", ".en"]:
            self.write(f"content/page/index{suffix}.md", '+++\ntitle = "Synthetic page"\n+++\n')
        fragments = [
            ("page/localized.md", "local-de"),
            ("page/localized.en.md", "local-en"),
        ]
        for path, marker in fragments:
            self.write("content/" + path,
                       f'+++\nfragment = "content"\nmarker = "{marker}"\n+++\nSynthetic fragment.\n')

    def test_language_selection(self):
        self.language_fixture()
        self.build()
        de = json.loads((self.root / "public/de/page/index.html").read_text())
        en = json.loads((self.root / "public/en/page/index.html").read_text())
        self.assertEqual(de, ["local-de"])
        self.assertEqual(en, ["local-en"])


if __name__ == "__main__":
    OPTIONS = PARSER.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FragmentLanguageTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
