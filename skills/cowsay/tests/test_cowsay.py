import subprocess, sys, unittest
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin" / "cowsay"

def run(*args, stdin=None):
    return subprocess.run([sys.executable, BIN, *args], input=stdin, capture_output=True, text=True, check=True).stdout

class Cowsay(unittest.TestCase):
    def test_box_is_aligned_with_emoji(self):
        lines = run("-W", "30", "hola 🚀 acá ñandú").splitlines()
        box = lines[: next(i for i, l in enumerate(lines) if l.startswith("╰")) + 1]
        widths = {sum(2 if ord(c) >= 0x1F300 else 1 for c in l) for l in box}
        self.assertEqual(len(widths), 1)

    def test_moods(self):
        self.assertIn("✔ ÉXITO", run("--ok", "x"))
        self.assertIn("(xx)", run("--fail", "x"))
        self.assertIn("o", run("--think", "x").splitlines()[3])

    def test_urls_are_not_split(self):
        url = "https://github.com/kodexArg/cowsay/pull/123456789"
        self.assertIn(url, run("-W", "20", url))

    def test_stdin_and_list(self):
        self.assertIn("moo", run(stdin="moo"))
        self.assertEqual(run("-l").split(), ["default", "tux", "moose", "cat", "koala"])

if __name__ == "__main__":
    unittest.main()
