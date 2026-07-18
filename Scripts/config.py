"""
config.py — persisted wizard settings
======================================

Saves the choices made in the interactive wizard to `configure.json` in
the repo root, and offers to reuse them on the next run. This is separate
from the Eksternal action files themselves — it only remembers wizard
*input*, never modifies your library.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_FILENAME = "configure.json"
CONFIG_VERSION = 1


def config_path(repo_root: Path) -> Path:
    return repo_root / CONFIG_FILENAME


def load(repo_root: Path) -> dict[str, Any] | None:
    """Return the saved config dict, or None if absent / unreadable."""
    p = config_path(repo_root)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict) or data.get("version") != CONFIG_VERSION:
        return None
    return data


def save(repo_root: Path, *, library_path: str, old_mount: str, new_mount: str,
          layout_id: str | None, layout_name: str | None, genre_rewrite: bool,
          json_only: bool, custom_layout: dict[str, Any] | None = None) -> Path:
    """Write the current wizard selections to configure.json. Returns the path written."""
    data: dict[str, Any] = {
        "version": CONFIG_VERSION,
        "library_path": library_path,
        "old_mount": old_mount,
        "new_mount": new_mount,
        "layout_id": layout_id,
        "layout_name": layout_name,
        "genre_rewrite": genre_rewrite,
        "json_only": json_only,
    }
    if custom_layout is not None:
        data["custom_layout"] = custom_layout
    p = config_path(repo_root)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return p


def summary_lines(data: dict[str, Any]) -> list[str]:
    """Human-readable summary of a saved config, for the 'reuse?' prompt."""
    lines = []
    if data.get("library_path"):
        lines.append(f"Library:  {data['library_path']}")
    if data.get("layout_name"):
        lines.append(f"Layout:   {data['layout_name']}")
    elif data.get("layout_id") == "custom":
        lines.append("Layout:   Custom")
    if data.get("json_only"):
        lines.append("Scope:    JSON only")
    return lines
