"""
The Ferryman Project — Local Storage Engine
Encapsulates private, local-first reflection logging with atomic writes,
strict file permissions (0600), and corruption recovery.
Zero network calls, zero telemetry.
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime
from contextlib import contextmanager
from typing import List, Optional, Iterator
from ferryman.types import LogEntry


DEFAULT_LOG_PATH = os.path.expanduser("~/.ferryman_log.json")


def get_log_path() -> str:
    """Returns the configured log file path, expanding user and respecting FERRYMAN_DATA_FILE."""
    path = os.environ.get("FERRYMAN_DATA_FILE", DEFAULT_LOG_PATH)
    return os.path.abspath(os.path.expanduser(path))


@contextmanager
def file_lock(lock_path: str) -> Iterator[None]:
    """
    Acquires an exclusive advisory lock on lock_path with 0600 permissions.
    Serializes concurrent writes to prevent data loss.
    """
    parent_dir = os.path.dirname(os.path.abspath(lock_path))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o700, exist_ok=True)

    try:
        import fcntl
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            os.chmod(lock_path, 0o600)
        except OSError:
            pass
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(fd)
    except ImportError:
        # Fallback for Windows or non-fcntl systems
        yield


def load_log() -> List[LogEntry]:
    """
    Loads all log entries from the local storage file.
    If the file does not exist or is 0 bytes, returns an empty list.
    If the file is corrupted, backs it up and returns an empty list without crashing.
    """
    path = get_log_path()
    real_path = os.path.realpath(path)
    if not os.path.exists(real_path):
        return []

    # 0-byte file check: treat as clean empty log without raising JSONDecodeError
    try:
        if os.path.getsize(real_path) == 0:
            return []
    except OSError:
        return []

    try:
        with open(real_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # Validate items roughly conform to LogEntry
                valid_entries: List[LogEntry] = []
                for item in data:
                    if isinstance(item, dict) and "timestamp" in item and "type" in item and "content" in item:
                        valid_entries.append({
                            "timestamp": str(item["timestamp"]),
                            "type": str(item["type"]),
                            "content": str(item["content"])
                        })
                return valid_entries
            return []
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as err:
        # Corrupt file recovery: safely isolate corrupted file and reset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        corrupt_path = f"{real_path}.corrupt.{timestamp}"
        try:
            shutil.move(real_path, corrupt_path)
            sys.stderr.write(f"[Ferryman] Warning: Log file was unreadable. Preserved at {corrupt_path}\n")
        except OSError:
            pass
        return []


def save_entry(session_type: str, text: str) -> None:
    """
    Appends a new crossing reflection to the local log.
    Uses an exclusive lock, atomic temporary file swap, and ensures 0600 file permissions.
    Preserves symlink integrity if the log path is a symlink.
    """
    path = get_log_path()
    real_path = os.path.realpath(path)
    parent_dir = os.path.dirname(real_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o700, exist_ok=True)

    lock_file = f"{real_path}.lock"
    with file_lock(lock_file):
        log = load_log()
        new_entry: LogEntry = {
            "timestamp": datetime.now().isoformat(),
            "type": session_type,
            "content": text.strip()
        }
        log.append(new_entry)

        # Atomic write pattern in the same directory to avoid cross-device rename errors
        fd, tmp_path = tempfile.mkstemp(prefix="ferryman_", suffix=".tmp", dir=parent_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Enforce strict private permissions (0600: read/write by owner only)
            os.chmod(tmp_path, 0o600)
            os.replace(tmp_path, real_path)
        except Exception:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise


def clear_log() -> int:
    """
    Safely wipes the local log file, honoring user sovereignty over their data.
    Returns the count of deleted entries.
    """
    path = get_log_path()
    real_path = os.path.realpath(path)
    if not os.path.exists(real_path):
        return 0

    lock_file = f"{real_path}.lock"
    with file_lock(lock_file):
        log = load_log()
        count = len(log)
        try:
            os.remove(real_path)
        except OSError:
            # If removal fails, try truncating with empty list
            with open(real_path, "w", encoding="utf-8") as f:
                f.write("[]\n")
            os.chmod(real_path, 0o600)
        return count
