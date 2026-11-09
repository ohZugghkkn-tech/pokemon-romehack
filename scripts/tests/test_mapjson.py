"""Exercise the real C++ map generator, not just its Python mirror."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "soulgold"
TOOL = GAME / "tools/mapjson/mapjson"


class MapGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["make", "-C", str(TOOL.parent)], check=True, capture_output=True)

    def fixture(self, size=8, excluded=False, shared=False):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for name in ("maps/Town", "asm", "include"):
            (root / name).mkdir(parents=True)
        (root / "map.bin").write_bytes(bytes(size))
        (root / "border.bin").write_bytes(bytes(8))
        layouts = {"layouts_table_label": "gMapLayouts", "layouts": [{
            "id": "LAYOUT_TEST_TOWN", "name": "TestTown_Layout", "width": 2, "height": 2,
            "border_filepath": str(root / "border.bin"), "blockdata_filepath": str(root / "map.bin"),
            "primary_tileset": "gTileset_General", "secondary_tileset": "gTileset_General"}]}
        groups = {"group_order": ["Group"], "Group": ["Town"],
                  "rom_excluded_groups": ["Group"] if excluded else []}
        (root / "maps/Town/map.json").write_text(json.dumps({"layout": "LAYOUT_TEST_TOWN"}))
        if shared:
            groups["group_order"].append("KeptGroup")
            groups["KeptGroup"] = ["KeptTown"]
            (root / "maps/KeptTown").mkdir()
            (root / "maps/KeptTown/map.json").write_text(json.dumps({"layout": "LAYOUT_TEST_TOWN"}))
        (root / "maps/groups.json").write_text(json.dumps(groups))
        (root / "layouts.json").write_text(json.dumps(layouts))
        return root

    def generate(self, root):
        return subprocess.run([str(TOOL), "layouts", "emerald", str(root / "layouts.json"),
                               str(root / "maps/groups.json"), str(root / "asm"), str(root / "include")],
                              cwd=GAME, capture_output=True, text=True)

    def test_short_emitted_buffer_is_rejected(self):
        result = self.generate(self.fixture(size=2))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires at least 8 bytes", result.stderr)

    def test_odd_buffer_is_rejected(self):
        self.assertNotEqual(self.generate(self.fixture(size=9)).returncode, 0)

    def test_surplus_is_safe_and_not_truncated(self):
        root = self.fixture(size=10)
        self.assertEqual(self.generate(root).returncode, 0)
        self.assertEqual((root / "map.bin").stat().st_size, 10)
        self.assertIn("TestTown_Layout::", (root / "asm/layouts.inc").read_text())

    def test_excluded_short_buffer_has_null_slot_but_same_id(self):
        root = self.fixture(size=2, excluded=True)
        self.assertEqual(self.generate(root).returncode, 0)
        self.assertNotIn("TestTown_Layout::", (root / "asm/layouts.inc").read_text())
        self.assertIn(".4byte NULL", (root / "asm/layouts_table.inc").read_text())
        self.assertRegex((root / "include/layouts.h").read_text(), r"#define LAYOUT_TEST_TOWN 1\b")

    def test_shared_layout_cannot_hide_behind_an_excluded_group(self):
        result = self.generate(self.fixture(size=2, excluded=True, shared=True))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires at least 8 bytes", result.stderr)

    def test_real_layouts_generate_with_stable_ids_and_reviewed_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "asm").mkdir()
            (root / "include").mkdir()
            result = subprocess.run([
                str(TOOL), "layouts", "emerald", "data/layouts/layouts.json", "data/maps/map_groups.json",
                str(root / "asm"), str(root / "include")], cwd=GAME, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            known = json.loads((ROOT / "docs/known-layout-issues.json").read_text())
            self.assertEqual(hashlib.sha256((root / "include/layouts.h").read_bytes()).hexdigest(),
                             known["generated_constants_sha256"])
            table = re.findall(r"\.4byte (\w+)", (root / "asm/layouts_table.inc").read_text())
            layouts = json.loads((GAME / "data/layouts/layouts.json").read_text())["layouts"]
            headers = (root / "asm/layouts.inc").read_text()
            for index, layout in enumerate(layouts):
                issue = known["issues"].get(layout["id"])
                if not issue:
                    continue
                if issue["classification"] == "excluded-from-emerald":
                    self.assertEqual(table[index], "NULL", layout["id"])
                    self.assertNotIn("\n" + layout["name"] + "::\n", headers)
                else:
                    self.assertGreaterEqual(issue["actual_bytes"], issue["expected_bytes"])
                    self.assertEqual(table[index], layout["name"])
