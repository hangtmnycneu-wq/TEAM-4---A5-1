import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos_bap" / "demo_tinya51.py"

class TestTinyDemo(unittest.TestCase):
    def test_demo_runs_and_prints_trace(self):
        result = subprocess.run(
            [sys.executable, str(DEMO)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(
            result.returncode, 0,
            msg=f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )
        self.assertIn("Keystream", result.stdout)
        self.assertIn("Bản mã", result.stdout)
        self.assertIn("BƯỚC", result.stdout)

if __name__ == "__main__":
    unittest.main()
