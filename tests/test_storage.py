"""
Unit tests for ferryman/storage.py
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from ferryman.storage import (
    load_log,
    save_entry,
    clear_log,
    get_log_path,
    DEFAULT_LOG_PATH
)


class TestStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log_file = os.path.join(self.temp_dir.name, "test_log.json")
        os.environ["FERRYMAN_DATA_FILE"] = self.test_log_file

    def tearDown(self) -> None:
        if "FERRYMAN_DATA_FILE" in os.environ:
            del os.environ["FERRYMAN_DATA_FILE"]
        self.temp_dir.cleanup()

    def test_load_log_empty_when_nonexistent(self) -> None:
        entries = load_log()
        self.assertEqual(entries, [])

    def test_save_and_load_entry(self) -> None:
        save_entry("dawn", "Present breath")
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "dawn")
        self.assertEqual(entries[0]["content"], "Present breath")
        self.assertTrue("timestamp" in entries[0])

    def test_unicode_and_emojis(self) -> None:
        save_entry("dusk", "Laying down: 🌊 meditation and tranquil thoughts 🧘")
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["content"], "Laying down: 🌊 meditation and tranquil thoughts 🧘")

    def test_permissions_are_0600(self) -> None:
        save_entry("pause", "Feet on ground")
        mode = os.stat(self.test_log_file).st_mode & 0o777
        self.assertEqual(mode, 0o600)

    def test_clear_log(self) -> None:
        save_entry("dawn", "Morning walk")
        save_entry("dusk", "Laying down tasks")
        self.assertEqual(len(load_log()), 2)

        count = clear_log()
        self.assertEqual(count, 2)
        self.assertEqual(len(load_log()), 0)

    def test_clear_log_when_nonexistent(self) -> None:
        count = clear_log()
        self.assertEqual(count, 0)

    def test_corrupt_file_recovery(self) -> None:
        with open(self.test_log_file, "w") as f:
            f.write("{ invalid json corrupted content ")

        entries = load_log()
        self.assertEqual(entries, [])

        # Check that corrupted file was moved to .corrupt.<timestamp>
        files = os.listdir(self.temp_dir.name)
        corrupt_files = [f for f in files if ".corrupt." in f]
        self.assertTrue(len(corrupt_files) >= 1)

    def test_non_list_json_returns_empty(self) -> None:
        with open(self.test_log_file, "w") as f:
            f.write('{"timestamp": "2026-09-19", "content": "not a list"}')

        entries = load_log()
        self.assertEqual(entries, [])

    def test_malformed_entries_filtered(self) -> None:
        # Write list with some malformed items
        import json
        data = [
            {"timestamp": "2026-09-19", "type": "dawn", "content": "valid"},
            "invalid string",
            {"missing": "keys"},
            42,
            {"timestamp": "2026-09-19", "type": "dusk", "content": "also valid"}
        ]
        with open(self.test_log_file, "w") as f:
            json.dump(data, f)

        entries = load_log()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["content"], "valid")
        self.assertEqual(entries[1]["content"], "also valid")

    def test_directory_auto_creation(self) -> None:
        nested_file = os.path.join(self.temp_dir.name, "nested", "sub", "log.json")
        os.environ["FERRYMAN_DATA_FILE"] = nested_file

        save_entry("dawn", "Nested test")
        self.assertTrue(os.path.exists(nested_file))
        self.assertEqual(len(load_log()), 1)

    def test_expanduser_in_get_log_path(self) -> None:
        os.environ["FERRYMAN_DATA_FILE"] = "~/test_ferryman_path.json"
        path = get_log_path()
        self.assertFalse(path.startswith("~"))
        self.assertTrue(os.path.isabs(path))

    def test_zero_byte_file_handling(self) -> None:
        with open(self.test_log_file, "w") as f:
            pass  # 0 bytes
        entries = load_log()
        self.assertEqual(entries, [])
        # File should remain 0-byte without creating a .corrupt file
        files = os.listdir(self.temp_dir.name)
        corrupt_files = [f for f in files if ".corrupt." in f]
        self.assertEqual(len(corrupt_files), 0)

    def test_symlink_preservation(self) -> None:
        real_target = os.path.join(self.temp_dir.name, "real_target.json")
        with open(real_target, "w") as f:
            f.write("[]")
        symlink_path = os.path.join(self.temp_dir.name, "symlink.json")
        os.symlink(real_target, symlink_path)
        os.environ["FERRYMAN_DATA_FILE"] = symlink_path

        save_entry("dawn", "symlink check")
        self.assertTrue(os.path.islink(symlink_path))
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["content"], "symlink check")

    def test_concurrent_writes(self) -> None:
        import threading
        def worker(w_id: int) -> None:
            for i in range(5):
                save_entry("dawn", f"worker_{w_id}_{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        entries = load_log()
        self.assertEqual(len(entries), 20)


if __name__ == "__main__":
    unittest.main()
