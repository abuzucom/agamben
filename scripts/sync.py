#!/usr/bin/env python3
"""Sync AGENTS.md to tool-specific copies."""

import shutil
import sys
from pathlib import Path


SOURCE = "AGENTS.md"
COPIES = (
    "CLAUDE.md",
    "GEMINI.md",
    "CONVENTIONS.md",
    ".cursorrules",
    ".clinerules",
    ".windsurfrules",
    ".copilot-instructions",
    ".github/copilot-instructions.md",
)


def files_match(source: Path, target: Path) -> bool:
    """Return whether two text files match after line-ending normalization."""
    try:
        if not target.is_file():
            return False
        source_text = source.read_text(encoding="utf-8")
        target_text = target.read_text(encoding="utf-8")
        return source_text.replace("\r\n", "\n") == target_text.replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return False


def sync_copies(check_only: bool) -> int:
    """Sync copies or return 1 when check-only finds stale files."""
    root = Path(__file__).resolve().parent.parent
    source = root / SOURCE
    if not source.is_file():
        print(f"error: {SOURCE} not found at {root}", file=sys.stderr)
        return 1

    stale = [name for name in COPIES if not files_match(source, root / name)]
    if check_only:
        if stale:
            print(f"out of sync with {SOURCE}: {', '.join(stale)}", file=sys.stderr)
            return 1
        print("all copies in sync")
        return 0

    for name in stale:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        print(f"synced {name}")
    print("all copies already in sync" if not stale else "sync complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync_copies(check_only="--check" in sys.argv[1:]))
