#!/usr/bin/env python3
"""
retarget-paths.py — rewrite personal file paths and folder layout
================================================================

A guided, interactive tool that rewrites the hard-coded paths in the
Eksternal action groups so the bundled templates point at your own
library layout instead of the maintainer's `/Volumes/Eksternal/Audio/`
mount and `FirstLetter/Artist/Album/TrackNo - Title` structure.

WHAT IT DOES
------------

The Eksternal action groups ship with two pieces of personal information
hard-coded into every format string:

  1. The **mount path** — where Mp3tag will save files
     (e.g. `/Volumes/Eksternal/Audio/`).
  2. The **folder layout** — how files are organised inside that mount
     (e.g. `FirstLetter/Artist/Album/TrackNo - Title`).

This script handles both, plus the optional `/Audio/<Genre>/` →
`/Music/<Genre>/` rename, in one pass. The same path string lives in
three places in the repo and the script rewrites all of them:

  - Individual `*.mta` action scripts in `Actions/Eksternal/...`
  - Per-category JSON action groups
    (`Actions/Eksternal/Eksternal.json`, etc.)
  - The master importable bundle `Actions/Action Groups.json`

Both unescaped and JSON-escaped (`\\/`) forms are handled.

USAGE
-----

Interactive (recommended)::

    python3 Scripts/retarget-paths.py

Non-interactive (for scripting / CI)::

    # Mount retarget only.
    python3 Scripts/retarget-paths.py \\
        --new /Volumes/MyExternal/Music/ --yes

    # Apply a layout only (keep current mount).
    python3 Scripts/retarget-paths.py \\
        --layout standard --yes

    # Mount retarget + layout.
    python3 Scripts/retarget-paths.py \\
        --new /Volumes/MyExternal/Music/ \\
        --layout artist_year_album --yes

    # Write a retargeted copy to a directory (originals untouched).
    python3 Scripts/retarget-paths.py \\
        --new /Volumes/MyExternal/Music/ \\
        --layout alphabetical \\
        --out /tmp/retargeted/ --yes

    # Print the retargeted master JSON to stdout for piping.
    python3 Scripts/retarget-paths.py \\
        --new /Volumes/MyExternal/Music/ \\
        --layout flat \\
        --stdout --yes > "Action Groups.retargeted.json"

    # Inspect available layouts.
    python3 Scripts/retarget-paths.py --list-layouts
    python3 Scripts/retarget-paths.py --show-layout standard

OPTIONS
-------

Mount retargeting
  --old PATH        Old mount path to replace (default:
                    `/Volumes/Eksternal/Audio/`). Pass empty string to
                    skip the mount swap.
  --new PATH        New mount path (e.g. `/Volumes/MyExternal/Music/`
                    or `~/Music/Audio/`). Leave blank in interactive
                    mode to keep the current mount.
  --include-genre-rewrites
                    Also rewrite `/Audio/<Genre>/` → `/Music/<Genre>/`
                    in one pass. Off by default.

Layout application
  --layout NAME     Apply a folder-structure preset. See
                    `--list-layouts` for the bundled options. Add a
                    new preset to `Scripts/layouts.py` for anything else.

Output mode (mutually exclusive)
  --out DIR         Write a retargeted copy under DIR, preserving the
                    directory layout. Originals are untouched.
  --stdout          Write the retargeted `Actions/Action Groups.json`
                    to stdout. Originals are untouched.

Control
  --yes, -y         Apply changes without prompting.
  --dry-run, -n     Print what would change but do not write.
  --no-interactive  Disable the interactive wizard. Errors out if
                    neither `--new` nor `--layout` is given.
  --no-color        Disable ANSI color output (also auto-disabled
                    when stdout is not a TTY).
  --json-only       Process only JSON files (skip the per-action
                    `.mta` scripts). Useful for bulk retargeting
                    when the `.mta` files would be regenerated from
                    the JSON anyway, or when you only need the master
                    `Action Groups.json` as the importable bundle.
  --reset           Forget the saved configuration (configure.json)
                    and exit.

AFTER RUNNING
-------------

- In-place: re-import `Actions/Action Groups.json` into Mp3tag (or
  refresh the already-imported groups) so the new paths take effect.
  Commit the rewritten files if you forked the repo.
- `--out DIR`: import `<DIR>/Actions/Action Groups.json` into Mp3tag.
- `--stdout`: paste into Mp3tag via **Actions → File → Import Action
  Groups…** or pipe to a file with `> "Action Groups.retargeted.json"`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import config as configmod
import library
import ui
from ui import (
    Style,
    arrow, ask, banner, checklist, confirm, dim, error, file as fcolor,
    footer_hint, heading, heavy_rule, hr, info, key, path as pcolor,
    prompt_chr, section, select, subhead, success, val, warn,
    WizardBack, WizardQuit,
)
from custom_layout import build_custom_layout
from layouts import (
    COMPILATION_MARKER,
    SPLIT_MARKER,
    LayoutPreset,
    build_format_string,
    by_category,
    detect_action,
    get as get_layout,
    list_layouts,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_SEARCH_DIRS = [
    REPO_ROOT / "Actions",
    REPO_ROOT / "Sources",
]
FILE_GLOBS    = ("*.mta", "*.json")
DEFAULT_OLD   = "/Volumes/Eksternal/Audio/"
MASTER_JSON   = REPO_ROOT / "Actions" / "Action Groups.json"

EKSTERNAL_DIRS = (
    REPO_ROOT / "Actions" / "Eksternal",
    REPO_ROOT / "Sources",
)

DEFAULT_GENRE_REWRITES = [
    ("/Audio/Metal/",          "/Music/Metal/"),
    ("/Audio/Electronic/",     "/Music/Electronic/"),
    ("/Audio/Hip-Hop/",        "/Music/Hip-Hop/"),
    ("/Audio/Punk & Hardcore/","/Music/Punk & Hardcore/"),
    ("/Audio/Rock & Grunge/",  "/Music/Rock & Grunge/"),
    ("/Audio/Miscellaneous/",  "/Music/Miscellaneous/"),
]


# =====================================================================
# General utilities
# =====================================================================

def expand(p: str) -> str:
    return os.path.expanduser(p)


def normalize(p: str) -> str:
    p = expand(p).strip()
    if not p:
        return ""
    return p.rstrip("/") + "/"


def find_files(roots: list[Path], json_only: bool = False) -> list[Path]:
    globs = ("*.json",) if json_only else FILE_GLOBS
    out: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for pattern in globs:
            out.extend(root.rglob(pattern))
    if MASTER_JSON.exists() and MASTER_JSON not in out:
        out.append(MASTER_JSON)
    return sorted(set(out))


# =====================================================================
# Mount rewrite
# =====================================================================

def rewrite_mount(text: str, old: str, new: str,
                  extra: list[tuple[str, str]]) -> tuple[str, int]:
    r"""Mount retargeting. Handles unescaped and JSON-escaped `\/` forms."""
    count = 0
    pairs: list[tuple[str, str]] = []
    if old and old != new:
        pairs.append((old, new))
    for src, dst in extra:
        if src and dst and src != dst:
            pairs.append((src, dst))

    for src, dst in pairs:
        if src in text:
            count += text.count(src)
            text = text.replace(src, dst)
        escaped_src = src.replace("/", "\\/")
        escaped_dst = dst.replace("/", "\\/")
        if escaped_src in text and escaped_src != escaped_dst:
            count += text.count(escaped_src)
            text = text.replace(escaped_src, escaped_dst)
    return text, count


def detect_current_state() -> str:
    files = find_files(DEFAULT_SEARCH_DIRS)
    counts: dict[str, int] = {}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for known in ["/Volumes/Eksternal/Audio/", "/Audio/", "/Music/"]:
            if known in text:
                counts[known] = counts.get(known, 0) + text.count(known)
    return max(counts, key=counts.get) if counts else ""


def sample_change(text: str, old: str, extra: list[tuple[str, str]]) -> str:
    candidates = ([old] if old else []) + [s for s, _ in extra]
    for prefix in candidates:
        if prefix and prefix in text:
            idx = text.find(prefix)
            end = text.find("$", idx)
            if end == -1:
                end = idx + 80
            return text[idx:end][:80] + ("…" if end - idx > 80 else "")
    return ""


# =====================================================================
# Layout rewrite
# =====================================================================

_JSON_STR = r'"((?:[^"\\]|\\.)*)"'


def replace_format_in_mta(text: str, action: str, genre: str,
                           new_format: str) -> tuple[str, int]:
    """Replace the `1=<format>` line under `F=_FILENAME` in a .mta file."""
    new_text, n = re.subn(
        r'(F=_FILENAME[ \t]*\n)1=[^\n]+',
        lambda m: m.group(1) + "1=" + new_format,
        text, count=1,
    )
    return new_text, 1 if n else 0


def replace_format_in_json_line(line: str, action: str, genre: str,
                                new_format: str,
                                new_format_escaped: str) -> tuple[str, int]:
    """Replace the `format` value in one JSON line, if it contains this genre."""
    if action == "C":
        marker         = f"/{genre}/{COMPILATION_MARKER}"
        marker_escaped = marker.replace("/", "\\/")
    elif action == "S":
        marker         = f"/{genre}/{SPLIT_MARKER}"
        marker_escaped = marker.replace("/", "\\/")
    else:
        marker         = f"/{genre}/"
        marker_escaped = marker.replace("/", "\\/")

    if marker not in line and marker_escaped not in line:
        return line, 0

    new_text, n = re.subn(
        r'("format"\s*:\s*)' + _JSON_STR,
        lambda m: m.group(1) + '"' + new_format_escaped + '"',
        line, count=1,
    )
    return new_text, 1 if n else 0


def replace_layout_in_json(text: str, layout: LayoutPreset,
                            new_mount: str) -> tuple[str, int]:
    """Replace every `format` value in the Eksternal action groups of a JSON file."""
    lines = text.split("\n")

    actions: list[tuple[str, str]] = []
    title_re = re.compile(r'"title"\s*:\s*' + _JSON_STR)
    for line in lines:
        m = title_re.search(line)
        if m:
            kind, genre = _title_to_action(m.group(1))
            if kind:
                actions.append((kind, genre))

    format_re = re.compile(r'"format"\s*:\s*' + _JSON_STR)
    idx = 0
    total = 0
    out_lines: list[str] = []
    for line in lines:
        if format_re.search(line) and idx < len(actions):
            kind, genre = actions[idx]
            idx += 1
            new_format = build_format_string(layout, kind, new_mount, genre)
            new_format_escaped = new_format.replace("/", "\\/")
            line, n = replace_format_in_json_line(
                line, kind, genre, new_format, new_format_escaped)
            total += n
        out_lines.append(line)

    return "\n".join(out_lines), total


def _title_to_action(title: str) -> tuple[str | None, str | None]:
    """Map an action title to (action_type, genre)."""
    if title.startswith("E - "):
        return "E", title[len("E - "):]
    if title.startswith("DC - "):
        return "DC", title[len("DC - "):].replace(" Compilation", "")
    if title.startswith("D - "):
        return "D", title[len("D - "):]
    if title.startswith("C - "):
        return "C", title[len("C - "):].replace(" - Compilation", "")
    if title.startswith("S - "):
        return "S", title[len("S - "):].replace(" - Split", "")
    return None, None


# =====================================================================
# Combined rewrite
# =====================================================================

def rewrite_file(fpath: Path, old_mount: str, new_mount: str,
                 extra: list[tuple[str, str]],
                 layout: LayoutPreset | None) -> tuple[str, int, str]:
    """Apply mount retargeting and/or layout application to a file.

    Returns (new_text, total_change_count, first_sample_line).
    """
    text     = fpath.read_text(encoding="utf-8")
    new_text = text
    total    = 0
    sample   = ""

    if (old_mount and new_mount and old_mount != new_mount) or extra:
        new_text, n = rewrite_mount(new_text, old_mount, new_mount, extra)
        total += n
        if n and not sample:
            sample = sample_change(new_text, old_mount, extra)

    if layout is not None:
        mount = new_mount or old_mount
        if fpath.suffix == ".mta":
            action, genre = detect_action(fpath.name)
            if action and genre:
                new_format = build_format_string(layout, action, mount, genre)
                new_text, n = replace_format_in_mta(new_text, action, genre, new_format)
                total += n
                if n and not sample:
                    sample = f"{action} {genre}: {new_format[:60]}…"
        elif fpath.suffix == ".json":
            new_text, n = replace_layout_in_json(new_text, layout, mount)
            total += n
            if n and not sample:
                sample = f"layout '{layout.name}' applied to {n} format string(s)"

    return new_text, total, sample


# =====================================================================
# Repo validation
# =====================================================================

def validate_repo() -> tuple[bool, list[tuple[bool, str]]]:
    """Sanity-check the repo before touching any files."""
    results: list[tuple[bool, str]] = []

    sources_dir = REPO_ROOT / "Sources"
    results.append((sources_dir.is_dir(),
                    f"Sources directory  {dim(str(sources_dir))}"))

    actions_dir = REPO_ROOT / "Actions"
    results.append((actions_dir.is_dir(),
                    f"Actions directory  {dim(str(actions_dir))}"))

    json_ok = True
    json_checked = 0
    for jf in find_files(DEFAULT_SEARCH_DIRS, json_only=True):
        json_checked += 1
        try:
            json.loads(jf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_ok = False
    results.append((json_ok,
                    f"JSON files valid  {dim(f'({json_checked} checked)')}"))

    writable = os.access(REPO_ROOT, os.W_OK)
    results.append((writable,
                    f"Destination writable  {dim(str(REPO_ROOT))}"))

    required    = [MASTER_JSON, REPO_ROOT / "Scripts" / "layouts.py"]
    required_ok = all(p.exists() for p in required)
    results.append((required_ok, "Required files present"))

    return all(ok for ok, _ in results), results


# =====================================================================
# Pre-scan  (for the rich summary panel — requirement #6)
# =====================================================================

def pre_scan(old: str, new: str, extra: list[tuple[str, str]],
             layout: LayoutPreset | None,
             json_only: bool) -> tuple[list[Path], int, int, int]:
    """Return (changed_files, mta_count, json_count, total_replacements)."""
    files   = find_files(DEFAULT_SEARCH_DIRS, json_only=json_only)
    mta_n   = 0
    json_n  = 0
    total_r = 0
    changed: list[Path] = []
    for f in files:
        try:
            _, n, _ = rewrite_file(f, old, new, extra, layout)
        except UnicodeDecodeError:
            continue
        if n:
            changed.append(f)
            total_r += n
            if f.suffix == ".mta":
                mta_n += 1
            elif f.suffix == ".json":
                json_n += 1
    return changed, mta_n, json_n, total_r


# =====================================================================
# CLI — layout list / detail  (also used by --list-layouts)
# =====================================================================

def print_layout_list() -> None:
    print(heading("Available layouts"))
    print(hr(60))
    for category, presets in by_category():
        print()
        print(f"  {subhead(category)}")
        for preset in presets:
            print(f"    {key(preset.id):<22} {val(preset.name)}")
            print(f"    {'':22} {dim(preset.description)}")
    print()


def print_layout_detail(name: str) -> None:
    L = get_layout(name)
    print(heading(f"Layout: {L.name}  ({key(repr(L.id))})"))
    print(hr(60))
    print(f"  {dim('Description:')}  {L.description}")
    print(f"  {dim('Structure:  ')}  {L.structure}")
    print()
    print(f"  {subhead('Preview')}")
    for line in L.preview.splitlines():
        print(f"    {line}")
    print()
    print(f"  {subhead('Format-string templates (run after the genre folder):')}")
    print()
    kind_labels = {
        "E":  "E  (standard album)",
        "D":  "D  (with Disc N/)",
        "C":  "C  (compilation)",
        "DC": "DC (compilation + disc)",
        "S":  "S  (split)",
    }
    for kind in ("E", "D", "C", "DC", "S"):
        print(f"    {key(f'{kind:<2}')}  {dim(kind_labels[kind] + ':'):<28}  {val(L[kind])}")
    print()


# =====================================================================
# Layout browser  (requirement #1: card-based display)
# =====================================================================

def print_layout_browser(selected_id: str | None) -> None:
    """Render layouts as visually separated cards."""
    counter = 1
    for category, presets in by_category():
        print(f"  {heading(category)}")
        print()
        for preset in presets:
            ui.layout_card(
                counter,
                preset.name,
                preset.structure,
                preset.description,
                preset.preview,
                selected=preset.id == selected_id,
                preset_id=preset.id,
            )
            counter += 1
        # Category gap
        print()

    # Separator before the extra options
    print(f"  {ui.heavy_rule(56)}")
    print()


# =====================================================================
# Wizard steps
# =====================================================================

STEP_TITLES = [
    "Where should Mp3tag save your files?",
    "How should your files be organised?",
    "Which files should be updated?",
    "Where should the updated files be written?",
]
TOTAL_STEPS = len(STEP_TITLES)

LIBRARY_STEP_HELP = (
    "Pick where Mp3tag should save your organised music. Recommended "
    "entries are common library locations that already exist on this Mac; "
    "detected external drives are non-system volumes currently under /Volumes."
)

LAYOUT_STEP_HELP = (
    "Pick a folder-structure preset, or build your own. Every preset shows "
    "an ASCII preview using the sample album Iron Maiden – Powerslave. "
    "Type the preset number, the preset id (e.g. 'standard'), "
    "'0' to build a custom layout, or '-' to keep the current layout."
)


# ─────────────────────────────────────────────────────────────────────
# Step 1 — Save location
# ─────────────────────────────────────────────────────────────────────

def step_save_location(saved: dict | None) -> tuple[str, str]:
    """Returns (old_mount, new_mount), both normalised with a trailing slash."""
    section(1, TOTAL_STEPS, STEP_TITLES[0])
    info(
        "The bundled actions contain a hard-coded mount path.",
        "Tell the wizard which path to replace, then where your files will go.",
        "",
    )
    footer_hint()
    print()

    current       = detect_current_state()
    suggested_old = current or DEFAULT_OLD
    if current and current != DEFAULT_OLD:
        info(f"Currently detected in repo: {current}")
        print()

    raw = ask(
        "Old path to replace",
        suggested_old,
        allow_empty=True,
        help_text=(
            "This is the placeholder path baked into the bundled action files. "
            "Leave it as-is unless you have already run this wizard before."
        ),
    )
    old = normalize(raw)

    print()
    remembered = saved.get("new_mount") if saved else None
    new = library.choose_library_path(current=old, remembered=remembered)

    if old and new and old == new:
        old = new

    return old, new


# ─────────────────────────────────────────────────────────────────────
# Step 2 — Layout / filename structure
# ─────────────────────────────────────────────────────────────────────

def step_filename_structure(saved: dict | None) -> tuple[LayoutPreset | None, list[tuple[str, str]]]:
    """Returns (layout_or_None, genre_rewrite_pairs)."""
    section(2, TOTAL_STEPS, STEP_TITLES[1])
    info(
        "Pick a layout preset for the folder hierarchy inside your save location,",
        "or build a custom one. Every card below shows an ASCII folder preview.",
        "",
    )
    footer_hint()
    print()

    print_layout_browser(saved.get("layout_id") if saved else None)

    ids = list_layouts()
    total_presets = len(ids)

    # Extra options after the cards
    print(f"  {key('[0]')}  {subhead('Design a custom layout')}")
    print(f"       {dim('Build the folder hierarchy and filename format step by step.')}")
    print()
    print(f"  {key('[–]')}  {subhead('Keep the current layout')}")
    print(f"       {dim('Only update mount paths and other options below.')}")
    print()
    print(f"  {ui.heavy_rule(56)}")
    print()

    default_choice = (saved or {}).get("layout_id") or "standard"
    while True:
        raw = ask(
            f"Choose a layout number, preset id, 0 for custom, or – to skip",
            default_choice,
            help_text=LAYOUT_STEP_HELP,
        )
        if raw in ("-", "–", "--"):
            layout = None
            break
        if raw == "0":
            print()
            layout = build_custom_layout()
            break
        if raw.isdigit() and 1 <= int(raw) <= total_presets:
            layout = get_layout(ids[int(raw) - 1])
            break
        if raw in ids:
            layout = get_layout(raw)
            break
        print(f"  {warn('!')} Unrecognised choice {raw!r} — see the cards above.")

    print()
    if layout is not None:
        _show_selected_layout(layout)

    # Genre sub-folder rename (optional, off by default)
    print()
    print(f"  {subhead('Genre folder name')}")
    print()
    print(f"  {dim('Some repositories use /Audio/<Genre>/ as the genre bucket path.')}")
    print(f"  {dim('You can rename it to /Music/<Genre>/ in the same pass.')}")
    print()
    if confirm(
        f"Rename  {pcolor('/Audio/<Genre>/')}  →  {pcolor('/Music/<Genre>/')} ?",
        default_no=True,
        help_text=(
            "Rewrites the coarse genre-bucket parent folder name from 'Audio' "
            "to 'Music' across all files. Off by default."
        ),
    ):
        extra = DEFAULT_GENRE_REWRITES
    else:
        extra = []

    return layout, extra


def _show_selected_layout(layout: LayoutPreset) -> None:
    print(f"  {success(Style.CHECK)}  Layout set to  {val(layout.name)}")
    print()
    print(f"  {dim('Structure:')}  {dim(layout.structure)}")
    print()
    print(f"  {subhead('Preview')}")
    print()
    for line in layout.preview.splitlines():
        print(f"    {dim(line)}")
    print()


# ─────────────────────────────────────────────────────────────────────
# Step 3 — File scope
# ─────────────────────────────────────────────────────────────────────

def step_file_scope() -> bool:
    """Returns json_only."""
    section(3, TOTAL_STEPS, STEP_TITLES[2])
    info(
        "The wizard updates two types of files inside this repository:",
        "  • Per-action scripts  (.mta)  — the individual save action templates",
        "  • JSON action groups  (.json) — the importable bundles for Mp3tag",
        "",
        "Updating both is recommended.  If the .mta files will be regenerated",
        "from the JSON anyway, choose 'JSON files only' to save time.",
        "",
    )
    footer_hint()
    print()

    ui.option_block(
        "1", "Both script and JSON files",
        "Updates every .mta script and every JSON action group.  "
        "Recommended for a complete retarget.",
        badge="Recommended",
    )
    ui.option_separator()

    ui.option_block(
        "2", "JSON files only",
        "Skips the per-action .mta scripts. "
        "Useful when you only need the importable Action Groups.json bundle.",
    )

    idx = select(
        ["Both .mta and JSON", "JSON only"],
        default_index=0,
        help_text="Choose 'JSON only' if you just need the importable Action Groups.json bundle.",
    )
    return idx == 1


# ─────────────────────────────────────────────────────────────────────
# Step 4 — Output mode
# ─────────────────────────────────────────────────────────────────────

def step_output_mode() -> tuple[str | None, bool]:
    """Returns (out_dir_or_None, use_stdout)."""
    section(4, TOTAL_STEPS, STEP_TITLES[3])
    info(
        "Choose where the updated files should be written.",
        "",
    )
    footer_hint()
    print()

    ui.option_block(
        "1", "Update this repository",
        "Rewrites the existing files in-place.  "
        "Re-import Action Groups.json into Mp3tag afterwards.",
        badge="Recommended",
    )
    ui.option_separator()

    ui.option_block(
        "2", "Write to a separate folder",
        "Leaves the originals untouched and writes a retargeted copy "
        "to a folder you specify.  Import from there.",
    )
    ui.option_separator()

    ui.option_block(
        "3", "Print to stdout",
        "Writes Action Groups.json to stdout.  "
        "Useful for piping or clipboard import into Mp3tag.",
    )

    idx = select(
        ["Update this repository", "Write to a separate folder", "Print to stdout"],
        default_index=0,
        help_text=(
            "'Update this repository' is what most people want. "
            "Use 'Write to a separate folder' to keep the originals untouched."
        ),
    )
    if idx == 1:
        print()
        while True:
            entered = ask("Output folder path")
            if not entered:
                print(f"  {warn('!')} A path is required.")
                continue
            return str(Path(expand(entered)).resolve()), False
    if idx == 2:
        return None, True
    return None, False


# ─────────────────────────────────────────────────────────────────────
# Step 5 — Rich confirmation summary  (requirement #6)
# ─────────────────────────────────────────────────────────────────────

def step_summary(old: str, new: str, layout: LayoutPreset | None,
                 extra: list[tuple[str, str]], json_only: bool,
                 out_dir: str | None, use_stdout: bool,
                 changed_files: list[Path], mta_n: int, json_n: int,
                 total_r: int) -> bool:
    """Prints the final confirmation summary.  Returns True if the user confirms."""
    w = 56

    print(f"  {ui.heavy_rule(w)}")
    print(f"  {heading('  Ready to apply')}")
    print(f"  {ui.heavy_rule(w)}")
    print()

    # Mount
    if old and new and old != new:
        ui.summary_row("Mount path", f"{pcolor(old)}  →  {pcolor(new)}")
    else:
        ui.summary_row("Mount path", "No change", note="")

    # Layout
    if layout:
        ui.summary_row("Layout", layout.name, note=dim(layout.structure))
    else:
        ui.summary_row("Layout", "Keep current")

    # Genre rename
    if extra:
        ui.summary_row("Genre folders",
                       "/Audio/ → /Music/",
                       note=f"{len(extra)} rules")
    else:
        ui.summary_row("Genre folders", "No change")

    # File scope
    scope_label = "JSON files only" if json_only else ".mta + JSON files"
    ui.summary_row("Files updated", scope_label)

    # Output
    if use_stdout:
        ui.summary_row("Output", "stdout")
    elif out_dir:
        ui.summary_row("Output", pcolor(out_dir + "/"),
                       note="originals untouched")
    else:
        ui.summary_row("Output", "In-place")

    print()
    print(f"  {ui.heavy_rule(w)}")
    print(f"  {subhead('  Estimated work')}")
    print(f"  {ui.heavy_rule(w)}")
    print()

    if changed_files:
        if not json_only:
            ui.summary_row("Action scripts", f"{mta_n} .mta files")
        ui.summary_row("JSON bundles", f"{json_n} .json files")
        ui.summary_row("Total replacements", str(total_r))
    else:
        print(f"  {warn('  No changes would be made')} — files may already be up to date.")

    print()
    print(f"  {ui.heavy_rule(w)}")
    print()

    if not changed_files:
        print(f"  {warn('Nothing to do.')}  "
              f"The files already contain the requested paths and layout.")
        return False

    return confirm("Apply these changes?", default_no=True)


# ─────────────────────────────────────────────────────────────────────
# Completion screen
# ─────────────────────────────────────────────────────────────────────

def print_completion(written: int, out_dir: str | None) -> None:
    w = 56
    print()
    print(f"  {ui.heavy_rule(w)}")
    print()
    print(f"  {heading('  Done!')}")
    print()
    print(f"  {success(Style.CHECK)}  Updated {val(str(written))} file(s)")
    print()
    print(f"  {subhead('Next steps')}")
    print()
    if out_dir:
        print(f"    1.  Import  {fcolor(out_dir + '/Actions/Action Groups.json')}")
        print(f"        into Mp3tag")
    else:
        print(f"    1.  Re-import  {fcolor('Actions/Action Groups.json')}  into Mp3tag")
        print(f"        (or refresh the already-imported groups)")
    print(f"    2.  Restart Mp3tag if it was open during the update")
    print()
    print(f"  Happy tagging.")
    print()
    print(f"  {ui.heavy_rule(w)}")
    print()


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Rewrite the hard-coded library mount and/or folder layout in "
            "the Eksternal action templates. Run with no arguments for an "
            "interactive wizard, or pass --new / --layout for non-interactive use."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 Scripts/retarget-paths.py\n"
            "  python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --yes\n"
            "  python3 Scripts/retarget-paths.py --layout standard --yes\n"
            "  python3 Scripts/retarget-paths.py --list-layouts\n"
        ),
    )
    ap.add_argument("--old", default=None,
                    help=f"Old mount path to replace (default: {DEFAULT_OLD!r}). "
                         f"Pass empty string to skip the mount swap.")
    ap.add_argument("--new", default=None,
                    help="New mount path (e.g. /Volumes/MyExternal/Music/ or ~/Music/Audio/).")
    ap.add_argument("--layout", default=None, metavar="NAME",
                    help="Apply a folder-structure layout. See --list-layouts.")
    ap.add_argument("--list-layouts", action="store_true",
                    help="List available layouts and exit.")
    ap.add_argument("--show-layout", default=None, metavar="NAME",
                    help="Show the format-string templates for a layout and exit.")
    ap.add_argument("--yes", "-y", action="store_true",
                    help="Apply changes without prompting.")
    ap.add_argument("--dry-run", "-n", action="store_true",
                    help="Print what would change but do not write.")
    ap.add_argument("--include-genre-rewrites", action="store_true",
                    help="Also rewrite /Audio/<Genre>/ → /Music/<Genre>/. Off by default.")
    ap.add_argument("--out", default=None, metavar="DIR",
                    help="Write a retargeted copy under DIR. Mutually exclusive with --stdout.")
    ap.add_argument("--stdout", action="store_true",
                    help="Write Actions/Action Groups.json to stdout. Mutually exclusive with --out.")
    ap.add_argument("--no-interactive", action="store_true",
                    help="Disable interactive mode. Errors out if --new and --layout are both missing.")
    ap.add_argument("--no-color", action="store_true",
                    help="Disable ANSI color output (also auto-disabled when stdout is not a TTY).")
    ap.add_argument("--json-only", action="store_true",
                    help="Process only JSON files (skip the per-action .mta scripts).")
    ap.add_argument("--reset", action="store_true",
                    help="Forget the saved configuration (configure.json) and exit.")
    args = ap.parse_args()

    if args.no_color:
        ui.set_color(False)

    if args.list_layouts:
        print_layout_list()
        return 0
    if args.show_layout:
        try:
            print_layout_detail(args.show_layout)
        except KeyError as e:
            print(f"  {error(str(e))}", file=sys.stderr)
            return 2
        return 0
    if args.reset:
        p = configmod.config_path(REPO_ROOT)
        if p.exists():
            p.unlink()
            print(f"  {success('Done.')} Removed {fcolor(str(p))}")
        else:
            print(f"  {dim('Nothing to reset.')}")
        return 0

    if args.out and args.stdout:
        print(f"  {error('--out and --stdout are mutually exclusive')}", file=sys.stderr)
        return 2

    interactive = not args.no_interactive and sys.stdin.isatty()

    saved       = configmod.load(REPO_ROOT) if interactive else None
    reuse_saved = False

    if interactive:
        banner(
            "Eksternal Configure",
            "Set up library paths and folder layout for your Mp3tag actions",
            str(REPO_ROOT),
        )

        print(f"  {dim('This wizard rewrites the Eksternal action groups so the bundled')}")
        print(f"  {dim('templates point at')} {key('your')} {dim('library mount and folder layout.')}")
        print()
        print(f"  {dim('Flow:')}  "
              f"{key('Save location')}  {arrow()}  {key('Layout')}  {arrow()}  "
              f"{key('File scope')}  {arrow()}  {key('Output mode')}")
        print()
        print(f"  {dim('Press')} {key('Enter')} {dim('to accept a default.')}  "
              f"{dim('Type')} {key('?')} {dim('for help at any prompt.')}  "
              f"{dim('Type')} {key('b')} {dim('to go back.')}")
        print()

        # Repo validation
        print(f"  {subhead('Checking repository…')}")
        print()
        all_ok, results = validate_repo()
        checklist(results)
        print()
        if not all_ok:
            print(f"  {error('Repository check failed.')} "
                  f"Fix the issues above and re-run.")
            return 1
        print(f"  {success('Ready.')}")
        print()

        if saved:
            print(f"  {subhead('Previous configuration found')}")
            print()
            for line in configmod.summary_lines(saved):
                print(f"    {dim(line)}")
            print()
            reuse_saved = confirm("Use previous settings?", default_no=False)
            print()

    # ─────────────────────────────────────────────────────────────────
    # Wizard step runner
    # ─────────────────────────────────────────────────────────────────
    old: str = ""
    new: str = ""
    layout: LayoutPreset | None = None
    extra: list[tuple[str, str]] = []
    json_only  = args.json_only
    out_dir:  str | None = args.out
    use_stdout = args.stdout

    if interactive and reuse_saved and saved:
        old        = saved.get("old_mount", "") or ""
        new        = saved.get("new_mount", "") or ""
        layout_id  = saved.get("layout_id")
        if layout_id == "custom" and saved.get("custom_layout"):
            cl     = saved["custom_layout"]
            layout = LayoutPreset(**cl)
        elif layout_id:
            try:
                layout = get_layout(layout_id)
            except KeyError:
                layout = None
        extra     = DEFAULT_GENRE_REWRITES if saved.get("genre_rewrite") else []
        json_only = saved.get("json_only", json_only)

        # Still ask for output mode even on reuse.
        section(4, TOTAL_STEPS, STEP_TITLES[3])
        footer_hint()
        print()
        idx = select(
            ["Update this repository", "Write to a separate folder", "Print to stdout"],
            default_index=0,
        )
        if idx == 1:
            out_dir = str(Path(expand(ask("Output folder path"))).resolve())
        elif idx == 2:
            use_stdout = True

    elif interactive:
        wizard_steps = [
            "save_location",
            "filename_structure",
            "file_scope",
            "output_mode",
        ]
        step_idx = 0
        step_results: dict[str, object] = {}

        while step_idx < len(wizard_steps):
            step_name = wizard_steps[step_idx]
            try:
                if step_name == "save_location":
                    step_results["save_location"] = step_save_location(saved)
                elif step_name == "filename_structure":
                    step_results["filename_structure"] = step_filename_structure(saved)
                elif step_name == "file_scope":
                    step_results["file_scope"] = step_file_scope()
                elif step_name == "output_mode":
                    step_results["output_mode"] = step_output_mode()
            except WizardBack:
                if step_idx == 0:
                    print(f"  {dim('Already at the first step.')}")
                    continue
                step_idx -= 1
                print()
                continue
            except WizardQuit:
                print(f"\n  {warn('Cancelled.')}")
                return 130
            print()
            step_idx += 1

        old, new = step_results["save_location"]
        layout, extra = step_results["filename_structure"]
        json_only = step_results["file_scope"]
        out_dir, use_stdout = step_results["output_mode"]

    else:
        # Non-interactive: pure flag-driven path, unchanged behaviour.
        if args.old is not None:
            old = normalize(args.old)
        else:
            old = normalize(DEFAULT_OLD) if (args.new or args.layout) else ""
        new = normalize(args.new) if args.new is not None else old

        if args.layout is not None:
            try:
                layout = get_layout(args.layout)
            except KeyError as e:
                print(f"  {error(str(e))}", file=sys.stderr)
                return 2
        else:
            layout = None

        extra = DEFAULT_GENRE_REWRITES if args.include_genre_rewrites else []

        if not args.new and layout is None and not extra:
            print(f"  {error('error:')} pass {key('--new')}, {key('--layout')}, or both "
                  f"(or run without {key('--no-interactive')})", file=sys.stderr)
            return 2

    if old and new and old == new:
        old = new

    # ─────────────────────────────────────────────────────────────────
    # Pre-scan + rich summary (interactive, non-reuse)
    # ─────────────────────────────────────────────────────────────────
    if interactive and not args.yes:
        changed_files, mta_n, json_n, total_r = pre_scan(
            old, new, extra, layout, json_only)

        if not step_summary(old, new, layout, extra, json_only, out_dir,
                            use_stdout, changed_files, mta_n, json_n, total_r):
            print(f"  {warn('Cancelled.')}")
            return 1
        print()
        # Use the pre-scan results so we don't scan twice in the apply phase.
        plan = [(f, *_n_sample(f, old, new, extra, layout))
                for f in changed_files]
    else:
        # Non-interactive path: scan now.
        files = find_files(DEFAULT_SEARCH_DIRS, json_only=json_only)
        if not files:
            kind = "JSON" if json_only else ".mta or .json"
            print(f"  {error(f'No {kind} files found.')}", file=sys.stderr)
            return 1

        plan_raw: list[tuple[Path, int, str]] = []
        for f in files:
            try:
                _, n, sample = rewrite_file(f, old, new, extra, layout)
            except UnicodeDecodeError:
                continue
            if n:
                plan_raw.append((f, n, sample))
        plan = plan_raw  # type: ignore[assignment]

        if not plan:
            print(f"  {warn('No changes would be made')} "
                  f"(searched {len(files)} files).")
            return 0

    total = sum(n for _, n, *_ in plan)
    out_stream = sys.stderr if use_stdout else sys.stdout

    print(hr(70), file=out_stream)
    print(f"  {subhead('Plan')}  {dim('—')}  "
          f"{total} change(s) across {len(plan)} file(s)", file=out_stream)
    print(hr(70), file=out_stream)
    for row in plan:
        f, n = row[0], row[1]
        sample = row[2] if len(row) > 2 else ""
        try:
            rel = f.relative_to(REPO_ROOT)
        except ValueError:
            rel = f
        line = f"  {val(str(n).rjust(3))}  {fcolor(str(rel))}"
        if sample:
            line += f"  {dim('  e.g.')}  {pcolor(sample)}"
        print(line, file=out_stream)
    print(hr(70), file=out_stream)
    print(file=out_stream)

    if args.dry_run:
        print(f"  {warn('Dry run — no files written.')}")
        return 0

    if not args.yes and not (interactive and not args.yes):
        # Non-interactive, --yes not given: ask once more.
        if interactive:
            ans = confirm(f"Apply these {total} change(s)?", default_no=True)
        else:
            raw_ans = input(
                f"  {prompt_chr()} Apply these {total} change(s)? [y/N]: "
            ).strip().lower()
            ans = raw_ans in ("y", "yes")
        if not ans:
            print(f"  {warn('Cancelled.')}")
            return 1

    # ─────────────────────────────────────────────────────────────────
    # Apply
    # ─────────────────────────────────────────────────────────────────
    written = 0

    if use_stdout:
        if not MASTER_JSON.exists():
            print(f"  {error(str(MASTER_JSON) + ' not found')}", file=sys.stderr)
            return 1
        new_text, _, _ = rewrite_file(MASTER_JSON, old, new, extra, layout)
        sys.stdout.write(new_text)
        if not new_text.endswith("\n"):
            sys.stdout.write("\n")
        print(
            f"\n  {success('Done.')} Wrote {total} change(s) to stdout. "
            f"Pipe or paste into Mp3tag via "
            f"{key('Actions → File → Import Action Groups…')}",
            file=sys.stderr,
        )
        return 0

    if out_dir:
        out_root = Path(expand(out_dir)).resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        for row in plan:
            f = row[0]
            try:
                rel = f.relative_to(REPO_ROOT)
            except ValueError:
                rel = Path(f.name)
            new_text, _, _ = rewrite_file(f, old, new, extra, layout)
            if new_text == f.read_text(encoding="utf-8"):
                continue
            dest = out_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(new_text, encoding="utf-8")
            written += 1
        if interactive:
            _save_config(old, new, layout, extra, json_only)
            print_completion(written, str(out_root))
        else:
            print(f"  {success('Done.')} Wrote {val(str(written))} file(s) under "
                  f"{pcolor(str(out_root) + '/')}  {dim('(originals untouched)')}")
            print(f"  Import {fcolor(str(out_root / 'Actions' / 'Action Groups.json'))} "
                  f"into Mp3tag to load the rewritten actions.")
        return 0

    # In-place.
    for row in plan:
        f = row[0]
        new_text, _, _ = rewrite_file(f, old, new, extra, layout)
        if new_text != f.read_text(encoding="utf-8"):
            f.write_text(new_text, encoding="utf-8")
            written += 1

    if interactive:
        _save_config(old, new, layout, extra, json_only)
        print_completion(written, None)
    else:
        print(f"  {success('Done.')} Wrote {val(str(written))} file(s). "
              f"Re-import {fcolor('Actions/Action Groups.json')} into Mp3tag "
              f"{dim('(or refresh the existing imported groups)')} to pick up the changes.")
    return 0


def _n_sample(fpath: Path, old: str, new: str,
              extra: list[tuple[str, str]],
              layout: LayoutPreset | None) -> tuple[int, str]:
    """Return (n_changes, sample) for a file that we know changed."""
    _, n, sample = rewrite_file(fpath, old, new, extra, layout)
    return n, sample


def _save_config(old: str, new: str, layout: LayoutPreset | None,
                 extra: list[tuple[str, str]], json_only: bool) -> None:
    custom_layout_data = None
    if layout is not None and layout.id == "custom":
        custom_layout_data = {
            "id":          layout.id,
            "name":        layout.name,
            "description": layout.description,
            "structure":   layout.structure,
            "templates":   layout.templates,
            "category":    layout.category,
            "preview":     layout.preview,
            "note":        layout.note,
        }
    configmod.save(
        REPO_ROOT,
        library_path=new,
        old_mount=old,
        new_mount=new,
        layout_id=layout.id if layout else None,
        layout_name=layout.name if layout else None,
        genre_rewrite=bool(extra),
        json_only=json_only,
        custom_layout=custom_layout_data,
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print(f"\n  {warn('Cancelled.')}")
        raise SystemExit(130)
