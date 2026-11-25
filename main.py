#!/usr/bin/env python3
"""Duskline Visit My House — make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Copies the pre-rendered invitation-letter image (entry.png, held in this
repository) to the output directory as entry.png.

Deterministic: a byte-for-byte copy, no network, no randomness,
no clock, no environment-dependent behaviour. Two runs write the
same bytes. The program never writes into its own repository: when
the output directory is the repo itself (or inside it) it refuses
quietly and exits 0.
"""
import hashlib
import os
import shutil
import sys
import tempfile

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(directory):
    """True when directory is the repo dir or lives inside it."""
    try:
        target = os.path.realpath(directory)
        root = os.path.realpath(HERE)
    except Exception:
        return True
    return target == root or target.startswith(root + os.sep)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out_dir:
        try:
            out_dir = tempfile.mkdtemp(prefix="duskline-visit-my-house-")
        except Exception:
            return 0
    if _inside_repo(out_dir):
        return 0
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception:
        return 0
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if _inside_repo(dst):
        return 0
    try:
        with open(src, "rb") as handle:
            if handle.read(len(PNG_MAGIC)) != PNG_MAGIC:
                print("entry.png is not a PNG file", file=sys.stderr)
                return 1
        shutil.copyfile(src, dst)
        src_hash = sha256_of(src)
        if sha256_of(dst) != src_hash:
            print("copied entry.png does not match the source", file=sys.stderr)
            return 1
    except Exception as exc:
        print("failed to copy entry.png: %s" % exc, file=sys.stderr)
        return 1
    print(
        "wrote %s (%d bytes, sha256 %s)" % (dst, os.path.getsize(dst), src_hash),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
