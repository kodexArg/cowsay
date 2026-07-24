#!/usr/bin/env python3
"""Goldens / regression suite for bin/cowsay (stdlib only)."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin" / "cowsay"


def run(
    args: list[str],
    stdin: bytes | str = b"",
    *,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    data = stdin.encode("utf-8") if isinstance(stdin, str) else stdin
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(
        [str(BIN), *args],
        input=data,
        capture_output=True,
        env=full_env,
        check=False,
    )


class CowsayTests(unittest.TestCase):
    def test_moo_width_40(self) -> None:
        r = run(["-W", "40"], "moo")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("< moo >", out)
        self.assertIn("(oo)", out)
        self.assertTrue(out.endswith("\n"))

    def test_wrap_width_3(self) -> None:
        r = run(["-W", "3"], "a b c")
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.decode().splitlines()
        self.assertEqual(lines[1], "/ a b \\")
        self.assertEqual(lines[2], "\\ c   /")

    def test_deterministic(self) -> None:
        a = run(["-W", "40"], "x")
        b = run(["-W", "40"], "x")
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_think(self) -> None:
        r = run(["-W", "20", "--think"], "hmm")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("( hmm )", out)
        self.assertIn("\n        o   ", out)

    def test_dead_face(self) -> None:
        r = run(["-W", "20", "-d"], "x")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("(xx)", out)
        self.assertIn("U ", out)

    def test_moose_eyes_substituted(self) -> None:
        r = run(["-W", "20", "-f", "moose", "-e", "XX"], "x")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("(XX)", out)
        self.assertNotIn("(oo)", out)

    def test_moose_dead_eyes(self) -> None:
        r = run(["-W", "20", "-f", "moose", "-d"], "x")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("(xx)", r.stdout.decode())

    def test_missing_cow(self) -> None:
        r = run(["-f", "no-such-cow", "-W", "20"], "x")
        self.assertEqual(r.returncode, 2)
        self.assertIn(b"cowfile not found", r.stderr)

    def test_refuse_non_cow_path(self) -> None:
        r = run(["-f", "/etc/passwd", "-W", "20"], "x")
        self.assertEqual(r.returncode, 2)
        self.assertIn(b"refusing non-.cow path", r.stderr)
        self.assertNotIn(b"root:", r.stdout)

    def test_explicit_cow_path_ok(self) -> None:
        cow = ROOT / "cows" / "tux.cow"
        r = run(["-f", str(cow), "-W", "20"], "hi")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(b"o_o", r.stdout)

    def test_invalid_utf8_stdin(self) -> None:
        r = run(["-W", "20"], b"\xff\xfe")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stderr, b"cowsay: invalid UTF-8 on stdin\n")
        self.assertEqual(r.stdout, b"")

    def test_list_cows(self) -> None:
        r = run(["-l"])
        self.assertEqual(r.returncode, 0, r.stderr)
        names = r.stdout.decode().strip().split()
        self.assertEqual(names, ["default", "moose", "tux"])

    def test_cowpath_keeps_bundled_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            custom = Path(tmp) / "x.cow"
            custom.write_text("  $thoughts X\n  ($eyes)\n  $tongue\n", encoding="utf-8")
            r = run(["-W", "10"], "z", env={"COWPATH": tmp})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn(b"(oo)", r.stdout)  # bundled default still resolves
            r2 = run(["-f", "x", "-W", "10"], "z", env={"COWPATH": tmp})
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn(b"X", r2.stdout)

    def test_version(self) -> None:
        r = run(["-V"])
        self.assertEqual(r.returncode, 0)
        self.assertIn(b"0.2.2", r.stdout)
        self.assertIn(b"kodexArg", r.stdout)

    def test_hard_wrap_n(self) -> None:
        r = run(["-n", "-W", "5"], "no wrap please\nsecond")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("no wrap please", out)
        self.assertIn("second", out)

    def test_empty_stdin(self) -> None:
        r = run(["-W", "40"], "")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout.decode()
        self.assertIn("<  >", out)
        self.assertIn("(oo)", out)
        self.assertTrue(out.endswith("\n"))

    def test_moo_default_golden(self) -> None:
        r = run(["-W", "40"], "moo")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            r.stdout.decode(),
            " _____\n"
            "< moo >\n"
            " -----\n"
            "        \\   ^__^\n"
            "         \\  (oo)\\_______\n"
            "            (__)\\       )\\/\\\n"
            "                ||----w |\n"
            "                ||     ||\n",
        )

    def test_symlink_cow_escape_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            evil = Path(tmp) / "evil.cow"
            evil.symlink_to("/etc/passwd")
            r = run(["-f", str(evil), "-W", "10"], "x")
            self.assertEqual(r.returncode, 2)
            self.assertIn(b"refusing cowfile outside COWPATH", r.stderr)
            self.assertNotIn(b"root:", r.stdout)
            r2 = run(["-f", "evil", "-W", "10"], "x", env={"COWPATH": tmp})
            self.assertEqual(r2.returncode, 2)
            self.assertNotIn(b"root:", r2.stdout)
            # Must not appear in -l either
            r3 = run(["-l"], env={"COWPATH": tmp})
            self.assertEqual(r3.returncode, 0, r3.stderr)
            self.assertNotIn("evil", r3.stdout.decode().split())

    def test_cow_outside_cowpath_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "lone.cow"
            outside.write_text("  $thoughts X\n  ($eyes)\n", encoding="utf-8")
            r = run(["-f", str(outside), "-W", "10"], "x")
            self.assertEqual(r.returncode, 2)
            self.assertIn(b"refusing cowfile outside COWPATH", r.stderr)
            # Allowed once its directory is on COWPATH
            r2 = run(["-f", str(outside), "-W", "10"], "x", env={"COWPATH": tmp})
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn(b"X", r2.stdout)

    def test_symlink_into_bundled_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "alias.cow"
            link.symlink_to(ROOT / "cows" / "default.cow")
            r = run(["-f", str(link), "-W", "10"], "z", env={"COWPATH": tmp})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn(b"(oo)", r.stdout)


if __name__ == "__main__":
    if not BIN.is_file():
        sys.stderr.write(f"missing binary: {BIN}\n")
        raise SystemExit(2)
    raise SystemExit(unittest.main(verbosity=2))
