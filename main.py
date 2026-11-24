#!/usr/bin/env python3
"""The Funniest Toaster Error Message — entry program.

Writes a single original toaster error message (80 characters) to
/output/entry.txt: the message a kitchen toaster shows its owner when
the bread has asked to leave for the oven. The line is written from
scratch for this bounty; it copies no other entry and no existing text.

Why this line: it opens like a real appliance error ("Toasting
failed:"), then the surprise comes from somewhere the obvious toaster
puns never go — the bread has filed a bureaucratic transfer request,
and the toaster, deadpan and gracious, wishes it well. One voice, one
read, every word earning its place.
"""

import os
import sys
from pathlib import Path

# One original line (80 characters): a toaster error message in which
# the bread requests a transfer to the oven and the toaster wishes it
# well. No pun on toast, burnt, or crumbs — the joke is the toaster's
# deadpan, bureaucratic graciousness about losing its bread.
ENTRY = (
    "Toasting failed: the bread has requested a transfer to the oven. "
    "I wish it well."
)

# Output path: overridable for local testing via MAKEFUN_OUTPUT_PATH.
OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt"))

MIN_LENGTH = 1
MAX_LENGTH = 120


def validate_entry(text: str) -> str:
    """Check the text is one line the gate will accept."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(text)} chars, outside the 1-120 char range"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(entry: str, path: Path) -> None:
    """Write the entry directly to its destination, world-readable.

    Writes straight to the target file (no temp file is ever created in
    the output directory) and sets mode 0644 explicitly, so the grader
    can read the file whoever runs it.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(path, 0o644)


def main() -> int:
    try:
        entry = validate_entry(ENTRY)
    except ValueError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return 2
    try:
        write_entry(entry, OUTPUT_PATH)
        written = OUTPUT_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 3
    if written != entry:
        print(
            "error: round-trip check failed: file does not hold the entry",
            file=sys.stderr,
        )
        return 4
    print(f"wrote {len(written)}-char entry to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
