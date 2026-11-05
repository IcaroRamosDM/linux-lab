import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("linux_lab", ROOT / "app.py")
app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(app)


class EnvironmentReportTests(unittest.TestCase):
    def test_report_contains_process_and_filesystem_information(self):
        with tempfile.TemporaryDirectory() as temporary:
            report = app.collect_report(Path(temporary))
            self.assertEqual(report["directory"], str(Path(temporary).resolve()))
            self.assertIsInstance(report["uid"], int)
            self.assertGreater(report["disk"]["total_bytes"], 0)
            self.assertGreaterEqual(report["disk"]["free_bytes"], 0)
            self.assertLessEqual(
                report["disk"]["free_bytes"], report["disk"]["total_bytes"]
            )

    def test_json_cli_handles_spaces_and_unicode(self):
        with tempfile.TemporaryDirectory(prefix="linux lab ação ") as temporary:
            process = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "app.py"),
                    "--json",
                    "--directory",
                    temporary,
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads(process.stdout)
            self.assertEqual(report["directory"], str(Path(temporary).resolve()))

    def test_missing_directory_is_a_cli_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "app.py"),
                    "--directory",
                    str(Path(temporary) / "missing"),
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(process.returncode, 1)
            self.assertIn("linux-lab:", process.stderr)
            self.assertNotIn("Traceback", process.stderr)

    def test_file_cannot_be_used_as_directory(self):
        with tempfile.NamedTemporaryFile() as temporary:
            with self.assertRaises(NotADirectoryError):
                app.collect_report(Path(temporary.name))


if __name__ == "__main__":
    unittest.main()
