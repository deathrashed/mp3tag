"""
library.py — music library / save-location selection
=======================================================

Presents common library locations as visually separated groups with
clear descriptions so the user can pick without having to interpret a
bare numbered list.  Detected items are shown with short contextual
notes; recommended locations are highlighted clearly.

In this codebase the "library location" the user picks *is* the save
mount the Eksternal actions write to (what the rest of the script calls
`new_mount`), so `choose_library_path()` returns a normalised path
string suitable for that purpose.
"""

from __future__ import annotations

import os
from pathlib import Path

import ui
from ui import (
    Style, ask, confirm, dim, error, heading, key, muted,
    path as pcolor, subhead, success, val, warn,
)

COMMON_LIBRARY_PATHS = [
    "~/Music",
    "~/Music/Music",
    "~/Music/Library",
    "~/Documents/Music",
]

# Volume names that are never a real music library — skip when
# scanning /Volumes so the "External drives" list stays useful.
_IGNORED_VOLUME_NAMES = {
    "Macintosh HD", "Macintosh HD - Data", "Recovery", "VM", "Preboot",
    "Update", "com.apple.TimeMachine.localsnapshots",
}


def expand(p: str) -> str:
    return os.path.expanduser(p)


def normalize(p: str) -> str:
    p = expand(p).strip()
    if not p:
        return ""
    return p.rstrip("/") + "/"


def _display(p: str) -> str:
    """Collapse the home directory back to ~ for display."""
    home = os.path.expanduser("~")
    expanded = expand(p)
    if expanded.startswith(home):
        return "~" + expanded[len(home):]
    return p


def detect_common_paths() -> list[str]:
    """Common library locations that actually exist on disk, in priority order."""
    found = []
    for candidate in COMMON_LIBRARY_PATHS:
        if os.path.isdir(expand(candidate)):
            found.append(candidate)
    return found


def detect_external_volumes() -> list[str]:
    """Mounted external volumes under /Volumes, excluding the boot volume."""
    volumes_root = "/Volumes"
    if not os.path.isdir(volumes_root):
        return []
    found = []
    for name in sorted(os.listdir(volumes_root)):
        if name.startswith("."):
            continue
        if name in _IGNORED_VOLUME_NAMES:
            continue
        full = os.path.join(volumes_root, name)
        if os.path.isdir(full) and not os.path.islink(full):
            found.append(full)
        # Real external drives are not symlinks; skip links (boot volume alias).
    return found


def validate_path(raw: str) -> tuple[bool, str]:
    """Return (ok, message).  A path is valid if it is absolute and exists,
    or absolute and its parent exists (so new sub-folders are still allowed)."""
    full = expand(raw).rstrip("/")
    if not full:
        return False, "path cannot be empty"
    if not os.path.isabs(full):
        return False, f"{full!r} is not absolute — use a leading / or ~/"
    if os.path.isdir(full):
        return True, "exists"
    parent = os.path.dirname(full) or "/"
    if os.path.isdir(parent):
        return True, "does not exist yet, but the parent folder does"
    return False, f"{full!r} does not exist, and neither does its parent"


LIBRARY_HELP = (
    "This is the folder Mp3tag will save your organised music into once "
    "the Eksternal actions run — usually the root of your existing library, "
    "or a new folder you want to build one in. "
    "Recommended entries are common library locations that already exist on "
    "this Mac. External drives are non-system volumes currently mounted "
    "under /Volumes. You can also enter any custom path."
)


# ─────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────

def choose_library_path(current: str | None = None,
                        remembered: str | None = None) -> str:
    """Interactive picker.  Returns a normalised (trailing-slash) path.

    Raises ui.WizardBack / ui.WizardQuit on navigation.
    """
    common   = detect_common_paths()
    external = detect_external_volumes()

    print(f"  {subhead('Where should Mp3tag save your music?')}")
    print()
    print(f"  {dim('Choose an existing location or enter a custom path.')}")
    print()

    options: list[tuple[str, str]] = []  # (display_label, raw_path)
    item_n = 0  # running counter for display numbers

    # ── Remembered (last-used) ──────────────────────────────────────
    if remembered:
        item_n += 1
        _section_header("Last used")
        _location_item(item_n, _display(remembered), remembered,
                       note="Used last time")
        options.append((_display(remembered), remembered))
        print()

    # ── Recommended (local paths that exist) ───────────────────────
    if common:
        _section_header("Recommended")
        for p in common:
            item_n += 1
            note = "Exists on this Mac"
            if p == "~/Music":
                note += "  ·  Default iTunes / Music app location"
            _location_item(item_n, p, p, note=note,
                           recommended=(item_n == (2 if remembered else 1)))
            options.append((p, p))
        print()

    # ── External drives ────────────────────────────────────────────
    if external:
        _section_header("External drives")
        for p in external:
            item_n += 1
            _location_item(item_n, p, p, note="Mounted external volume")
            options.append((p, p))
        print()

    # ── Custom entry ───────────────────────────────────────────────
    _section_header("Other")
    print(f"       {key('[0]')}  Enter a custom path")
    print()

    default_opt = "1" if options else "0"
    while True:
        raw = ask(
            f"Choose (0–{len(options)})",
            default_opt,
            help_text=LIBRARY_HELP,
        )
        if raw == "0":
            chosen = _prompt_custom_path(current)
            break
        try:
            idx = int(raw) - 1
        except ValueError:
            print(f"  {warn('!')} Enter a number between {key('0')} "
                  f"and {key(str(len(options)))}")
            continue
        if 0 <= idx < len(options):
            chosen = expand(options[idx][1])
            ok, msg = validate_path(chosen)
            if not ok:
                print(f"  {error('!')} {msg}")
                continue
            break
        print(f"  {warn('!')} Enter a number between {key('0')} "
              f"and {key(str(len(options)))}")

    normalised = normalize(chosen)
    print()
    print(f"  {success(Style.CHECK)}  Library set to {pcolor(normalised)}")
    print()
    return normalised


# ─────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────

def _section_header(title: str) -> None:
    print(f"  {dim('──')}  {subhead(title)}")
    print()


def _location_item(n: int, display: str, raw_path: str, *,
                   note: str = "", recommended: bool = False) -> None:
    badge_str = f"  {success('Recommended')}" if recommended else ""
    print(f"       {key(f'[{n}]')}  {val(display)}{badge_str}")
    if note:
        print(f"             {dim(note)}")
    print()


def _prompt_custom_path(current: str | None) -> str:
    print(f"  {dim('Enter the full path to your music folder.')}")
    print(f"  {dim('Tilde (~) is expanded automatically.')}")
    print()
    while True:
        raw = ask("Custom path", current or "", help_text=LIBRARY_HELP)
        candidate = expand(raw)
        ok, msg = validate_path(candidate)
        if ok:
            return candidate
        print(f"  {warn('!')} {msg}")
        if not confirm("Use this path anyway?", default_no=True):
            continue
        return candidate
