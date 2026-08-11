from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CliTests(unittest.TestCase):
    def test_cli_returns_structured_json(self) -> None:
        payload = {
            "propositions": [
                {"id": "p1", "subject": "الف", "relation": "هست", "object": "ب", "polarity": "affirm", "context": "c", "time": "t", "source": "test"},
                {"id": "p2", "subject": "الف", "relation": "هست", "object": "ب", "polarity": "deny", "context": "c", "time": "t", "source": "test"},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "rational_core", str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("contradictory", json.loads(completed.stdout)["status"])

    def test_cli_rejects_invalid_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text("{}", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "rational_core", str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(2, completed.returncode)
        self.assertIn("error", json.loads(completed.stdout))


if __name__ == "__main__":
    unittest.main()

