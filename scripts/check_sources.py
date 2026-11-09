#!/usr/bin/env python3
"""Syntax, map integrity and explicit upstream-debt checks; not a ROM test."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def source_names(root):
    # Include new worktree files too: the previous scanner silently missed its
    # own untracked scripts and new contributions until git add was run.
    data = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root)
    return sorted(set(filter(None, data.decode().split("\0"))))


def local_file(root, name):
    target = (root / name).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes source root: {name}")
    if not target.is_file():
        raise ValueError(f"Missing source file: {name}")
    return target


def duplicates(values):
    return sorted(key for key, count in Counter(values).items() if count > 1)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def check_maps(game, known):
    groups = load_json(game / "data/maps/map_groups.json")
    order = groups["group_order"]
    if duplicates(order):
        raise ValueError(f"Duplicate map groups: {duplicates(order)}")
    names = [name for group in order for name in groups[group]]
    if duplicates(names):
        raise ValueError(f"Duplicate maps: {duplicates(names)}")
    maps = [load_json(local_file(game, f"data/maps/{name}/map.json")) for name in names]
    if duplicates([entry["id"] for entry in maps]):
        raise ValueError("Duplicate map IDs")
    layouts = load_json(game / "data/layouts/layouts.json")["layouts"]
    ids = [entry["id"] for entry in layouts]
    if duplicates(ids):
        raise ValueError("Duplicate layout IDs")
    allowed_layouts = set(ids) | {"LAYOUT_NONE"}
    for entry in maps:
        if entry.get("layout") not in allowed_layouts:
            raise ValueError(f"Unknown layout in {entry['id']}: {entry.get('layout')}")
    excluded_groups = set(groups.get("rom_excluded_groups", []))
    if excluded_groups - set(order):
        raise ValueError("Unknown ROM-excluded map group")
    excluded_names = {name for group in excluded_groups for name in groups[group]}
    excluded_ids = {entry["layout"] for name, entry in zip(names, maps) if name in excluded_names}
    retained_ids = {entry["layout"] for name, entry in zip(names, maps) if name not in excluded_names}
    excluded_ids -= retained_ids  # Shared layouts must remain available.
    observed = {}
    for entry in layouts:
        for field in ("border_filepath", "blockdata_filepath"):
            local_file(game, entry[field])
        width, height = entry["width"], entry["height"]
        if type(width) is not int or type(height) is not int or width <= 0 or height <= 0:
            raise ValueError(f"Invalid dimensions in {entry['id']}")
        path = local_file(game, entry["blockdata_filepath"])
        actual, expected = path.stat().st_size, width * height * 2
        excluded = entry["id"] in excluded_ids or entry.get("layout_version", "emerald") != "emerald"
        if not excluded and (actual < expected or actual % 2):
            raise ValueError(f"Short or non-u16 ROM layout: {entry['id']}")
        if actual != expected:
            observed[entry["id"]] = {
                "classification": "excluded-from-emerald" if excluded else "emitted-surplus-cells",
                "path": entry["blockdata_filepath"], "width": width, "height": height,
                "actual_bytes": actual, "expected_bytes": expected,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
    # Do not silently accept new issues, changes to bad data or stale waivers.
    if set(observed) != set(known):
        raise ValueError(f"Layout debt changed: new={sorted(set(observed) - set(known))}, "
                         f"resolved/stale={sorted(set(known) - set(observed))}. "
                         "Review data and docs/known-layout-issues.json; do not blindly rebaseline.")
    for name, values in observed.items():
        if any(known[name].get(key) != value for key, value in values.items()):
            raise ValueError(f"Known layout issue changed: {name}; requires review")
    return len(maps), len(layouts), len(observed)


def main():
    counts = {"json": 0, "python": 0}
    errors = []
    for name in source_names(ROOT):
        path = ROOT / name
        try:
            if path.suffix == ".json":
                load_json(path)
                counts["json"] += 1
            elif path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=name)
                counts["python"] += 1
        except (OSError, ValueError, SyntaxError) as error:
            errors.append(f"{name}: {error}")
    if errors:
        raise SystemExit("\n".join(errors))
    known = load_json(ROOT / "docs/known-layout-issues.json")["issues"]
    maps, layouts, debt = check_maps(ROOT / "soulgold", known)
    print(f"Syntax: {counts['json']} JSON, {counts['python']} Python OK. "
          f"References: {maps} maps, {layouts} layouts checked.")
    print(f"Reviewed legacy differences: {debt}, unchanged; no short emitted Emerald layout. "
          "This is a data-bound check, not a playthrough or release approval.")


if __name__ == "__main__":
    main()
