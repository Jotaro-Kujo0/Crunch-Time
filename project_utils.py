"""
project_utils.py

Utility helpers for safe JSON persistence and simple logging.
"""
import json
import os
import tempfile
from typing import Any, Optional

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")


def safe_load_json(path: str) -> Optional[dict]:
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        _log(f"safe_load_json error reading {path}: {e}")
        return None


def atomic_write_json(path: str, data: Any) -> bool:
    try:
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=dirpath, prefix='.tmp_', text=True)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, path)
            return True
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
    except Exception as e:
        _log(f"atomic_write_json error writing {path}: {e}")
        return False


def _log(msg: str) -> None:
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass
