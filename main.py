#!/usr/bin/env python3
"""Brushing the Sea — coolest-art-01 entry.

Reads entry.png (bundled next to this script), verifies it, and writes it
to the grader's output directory. Stdlib only.
"""

import hashlib
import os
import sys

EXPECTED_SHA256 = "26e92cc7dff9bf49fe64333bfe21d251a64b313c091db887311a5906994b62ed"


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()

    # Verify: JPEG magic bytes.
    if not data.startswith(b"\xff\xd8\xff"):
        print("error: entry.png is not a JPEG", file=sys.stderr)
        return 1

    # Verify: dimensions <= 1024x1024 (read from the JPEG SOF marker).
    width, height = jpeg_dimensions(data)
    if width > 1024 or height > 1024:
        print(f"error: dimensions {width}x{height} exceed 1024x1024",
              file=sys.stderr)
        return 1

    # Verify: content matches the bundled image.
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        print("error: entry.png sha256 mismatch", file=sys.stderr)
        return 1

    print(f"source verified: {len(data)} bytes, JPEG magic OK, "
          f"dimensions {width}x{height} (uncropped landscape)")

    # The docker grader does NOT set MAKEFUN_OUTPUT_DIR; /output is a real
    # writable mount there, so fall back to it. (The local process driver
    # sets the variable, so either path works.)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)

    print(f"wrote {out_path} ({len(data)} bytes, sha256 {sha[:16]}...)")
    return 0


def jpeg_dimensions(data: bytes):
    """Parse width/height from a JPEG's Start-Of-Frame marker."""
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        i += 2 + seg_len
    raise ValueError("no SOF marker found in JPEG")


if __name__ == "__main__":
    sys.exit(main())
