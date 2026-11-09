import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.check_sources import check_maps, local_file, source_names, load_json


class SourceChecksTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.groups = {"group_order": ["Group"], "Group": ["Town"]}
        self.map = {"id": "MAP_TOWN", "layout": "LAYOUT_TOWN"}
        self.layout = {"id": "LAYOUT_TOWN", "width": 2, "height": 2,
                       "border_filepath": "border.bin", "blockdata_filepath": "map.bin"}
        self.write("data/maps/map_groups.json", self.groups)
        self.write("data/maps/Town/map.json", self.map)
        self.write("data/layouts/layouts.json", {"layouts": [self.layout]})
        (self.root / "map.bin").write_bytes(bytes(8))
        (self.root / "border.bin").write_bytes(bytes(8))

    def write(self, name, obj):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj))

    def test_valid_sources(self):
        self.assertEqual(check_maps(self.root, {}), (1, 1, 0))

    def test_duplicate_json_keys_are_rejected(self):
        path = self.root / "duplicate.json"
        path.write_text('{"dimensions": {"width": 2, "width": 3}}')
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key: width"):
            load_json(path)

    def test_duplicate_map_ids_are_rejected(self):
        self.groups["Group"].append("OtherTown")
        self.write("data/maps/map_groups.json", self.groups)
        self.write("data/maps/OtherTown/map.json", self.map)
        with self.assertRaisesRegex(ValueError, "Duplicate map IDs"):
            check_maps(self.root, {})

    def test_untracked_sources_are_included_and_deduplicated(self):
        with patch("scripts.check_sources.subprocess.check_output", return_value=b"old.py\0new.py\0old.py\0") as call:
            self.assertEqual(source_names(self.root), ["new.py", "old.py"])
            self.assertIn("--others", call.call_args.args[0])

    def test_escape_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            local_file(self.root, "../outside")

    def test_missing_map_is_rejected(self):
        (self.root / "data/maps/Town/map.json").unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            check_maps(self.root, {})

    def test_duplicate_map_is_rejected(self):
        self.groups["Group"].append("Town")
        self.write("data/maps/map_groups.json", self.groups)
        with self.assertRaisesRegex(ValueError, "Duplicate maps"):
            check_maps(self.root, {})

    def test_duplicate_group_is_rejected(self):
        self.groups["group_order"].append("Group")
        self.write("data/maps/map_groups.json", self.groups)
        with self.assertRaisesRegex(ValueError, "Duplicate map groups"):
            check_maps(self.root, {})

    def test_unknown_layout_is_rejected(self):
        self.map["layout"] = "LAYOUT_UNKNOWN"
        self.write("data/maps/Town/map.json", self.map)
        with self.assertRaisesRegex(ValueError, "Unknown layout"):
            check_maps(self.root, {})

    def test_duplicate_layout_is_rejected(self):
        self.write("data/layouts/layouts.json", {"layouts": [self.layout, self.layout]})
        with self.assertRaisesRegex(ValueError, "Duplicate layout IDs"):
            check_maps(self.root, {})

    def test_invalid_dimensions_are_rejected(self):
        self.layout["width"] = 0
        self.write("data/layouts/layouts.json", {"layouts": [self.layout]})
        with self.assertRaisesRegex(ValueError, "Invalid dimensions"):
            check_maps(self.root, {})

    def test_new_size_mismatch_is_rejected(self):
        (self.root / "map.bin").write_bytes(bytes(2))
        with self.assertRaisesRegex(ValueError, "Short or non-u16 ROM layout"):
            check_maps(self.root, {})

    def test_known_debt_is_exact_not_blanket_permission(self):
        (self.root / "map.bin").write_bytes(bytes(10))
        known = {"LAYOUT_TOWN": {"path": "map.bin", "width": 2, "height": 2,
                                "actual_bytes": 10, "expected_bytes": 8,
                                "classification": "emitted-surplus-cells",
                                "sha256": hashlib.sha256(bytes(10)).hexdigest()}}
        self.assertEqual(check_maps(self.root, known), (1, 1, 1))
        (self.root / "map.bin").write_bytes(b"X" * 10)
        with self.assertRaisesRegex(ValueError, "Known layout issue changed"):
            check_maps(self.root, known)

    def test_stale_debt_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "resolved/stale"):
            check_maps(self.root, {"LAYOUT_TOWN": {}})
