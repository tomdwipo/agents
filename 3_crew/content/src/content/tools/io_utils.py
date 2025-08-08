from __future__ import annotations

import json
import os
from typing import Any, Dict

from slugify import slugify


def ensure_dirs(*paths: str) -> None:
    """Ensure directories exist for each given path (file or folder path)."""
    for p in paths:
        base = p if os.path.isdir(p) or p.endswith(os.sep) else os.path.dirname(p)
        if base:
            os.makedirs(base, exist_ok=True)


def slugify_topic(topic: str) -> str:
    """Convert a topic string to a filesystem-friendly slug."""
    return slugify(topic)


def write_json(path: str, data: Dict[str, Any]) -> None:
    """Write a JSON file with UTF-8 encoding and pretty formatting."""
    ensure_dirs(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_text(path: str, text: str) -> None:
    """Write a UTF-8 text file."""
    ensure_dirs(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)