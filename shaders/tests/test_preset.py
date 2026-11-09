"""Dependency/integrity checks only; no GPU or emulator is launched."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream"
PRESET = ROOT / "soulgold-vivid-relief.slangp"


def read_preset(path):
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in values:
            raise ValueError(f"Duplicate key: {key}")
        values[key] = value.strip().strip('"')
    return values


class ShaderFilesTest(unittest.TestCase):
    def test_upstream_manifest(self):
        manifest = json.loads((ROOT / "upstream-manifest.json").read_text())
        actual = {p.relative_to(UPSTREAM).as_posix()
                  for p in UPSTREAM.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(manifest["files"]))
        self.assertEqual(len(actual), 12)
        for name, expected in manifest["files"].items():
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((UPSTREAM / name).read_bytes()).hexdigest(), expected)

    def test_preset_dependencies(self):
        for path in [PRESET, *UPSTREAM.rglob("*.slangp")]:
            values = read_preset(path)
            count = int(values["shaders"])
            keys = {k for k in values if re.fullmatch(r"shader\d+", k)}
            self.assertEqual(keys, {f"shader{i}" for i in range(count)})
            for i in range(count):
                target = (path.parent / values[f"shader{i}"]).resolve()
                self.assertTrue(target.is_relative_to(UPSTREAM.resolve()))
                self.assertTrue(target.is_file(), str(target))

    def test_include_dependencies(self):
        for path in UPSTREAM.rglob("*"):
            if path.suffix not in {".slang", ".h"}:
                continue
            for include in re.findall(r'^\s*#include\s+"([^"]+)"', path.read_text(), re.M):
                target = (path.parent / include).resolve()
                self.assertTrue(target.is_relative_to(UPSTREAM.resolve()))
                self.assertTrue(target.is_file(), str(target))

    def test_scalefx_chain_preserved(self):
        original_path = UPSTREAM / "edge-smoothing/scalefx/scalefx.slangp"
        original = read_preset(original_path)
        combined = read_preset(PRESET)
        self.assertEqual(combined["shaders"], "8")
        for key, value in original.items():
            if key == "shaders":
                continue
            if re.fullmatch(r"shader\d+", key):
                self.assertEqual((original_path.parent / value).resolve(),
                                 (ROOT / combined[key]).resolve())
            else:
                self.assertEqual(combined[key], value, key)
        self.assertEqual(combined["shader6"], "upstream/handheld/shaders/bevel.slang")
        self.assertEqual(combined["shader7"], "upstream/misc/shaders/image-adjustment.slang")
        self.assertEqual(combined["scale_type6"], "viewport")
        self.assertEqual(combined["scale6"], "1.0")
        self.assertEqual(combined["scale_type7"], "source")
        self.assertEqual(combined["scale7"], "1.0")

    def test_parameters_exist_and_are_in_range(self):
        values = read_preset(PRESET)
        declarations = {}
        for path in UPSTREAM.rglob("*.slang"):
            for name, default, lower, upper in re.findall(
                r'#pragma parameter (\w+) "[^"]+" ([\d.]+) ([\d.]+) ([\d.]+)',
                path.read_text()
            ):
                declarations[name] = (float(lower), float(upper))
        self.assertEqual(values["parameters"].split(";"), ["BEVEL_LEVEL", "ia_saturation"])
        for name in values["parameters"].split(";"):
            lower, upper = declarations[name]
            self.assertGreaterEqual(float(values[name]), lower)
            self.assertLessEqual(float(values[name]), upper)


if __name__ == "__main__":
    unittest.main()
