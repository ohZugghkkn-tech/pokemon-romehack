#!/usr/bin/env python3
"""Run reproducible host checks. No ROM, GPU, browser, downloads or publication."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "soulgold"


def run(*args, cwd=ROOT):
    print(f"\n[{cwd.relative_to(ROOT) or '.'}] {' '.join(map(str, args))}", flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def main():
    for tool in ("git", "make", "g++", "gcc", "node"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Missing host dependency: {tool}. See TESTING.md.")
    try:
        import PIL  # noqa: F401 - check before generating files
    except ImportError:
        raise SystemExit("Missing Pillow. Install requirements-dev.txt in a virtual environment.")

    run(sys.executable, "scripts/check_sources.py")
    run(sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-v")
    run(sys.executable, "-m", "unittest", "discover", "-s", "shaders/tests", "-v")
    # global.h includes this generated header even when only preprocessing docs.
    # Build the host generator directly: no ARM toolchain or ROM build needed.
    run("make", "-C", "tools/jsonproc", cwd=GAME)
    run("tools/jsonproc/jsonproc", "src/data/region_map/region_map_sections.json",
        "src/data/region_map/region_map_sections.constants.json.txt",
        "include/constants/region_map_sections.h", cwd=GAME)
    for directory in ("tools/soulgold_docs/tests", "tools/learnset_helpers/tests", "tools/docs_qr"):
        run(sys.executable, "-m", "unittest", "discover", "-s", directory, "-v", cwd=GAME)
    # The frontier browser test requires Playwright plus a running HTTP server;
    # it is deliberately separate, not silently skipped as a passed test.
    run("node", "--test", "tools/soulgold_docs/tests/party-export.test.mjs",
        "tools/soulgold_docs/tests/version-check.test.mjs", cwd=GAME)
    run(sys.executable, "tools/check_song_config.py", cwd=GAME)


if __name__ == "__main__":
    main()
