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

Both unescaped and JSON-escaped (``\\/``) forms are handled.

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
        --layout chronological --yes

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
                    `--list-layouts` for the bundled options
                    (`standard`, `chronological`, `alphabetical`,
                    `flat`). Add a custom entry to `Scripts/layouts.py`
                    for anything else.

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

from layouts import (
    COMPILATION_MARKER,
    SPLIT_MARKER,
    LAYOUTS,
    build_format_string,
    detect_action,
    get as get_layout,
    list_layouts,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_SEARCH_DIRS = [
    REPO_ROOT / "Actions",
    REPO_ROOT / "Sources",
]
FILE_GLOBS = ("*.mta", "*.json")
DEFAULT_OLD = "/Volumes/Eksternal/Audio/"
MASTER_JSON = REPO_ROOT / "Actions" / "Action Groups.json"

# Folders containing the hard-coded Eksternal action templates.
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
# ANSI styling
# =====================================================================
# Minimal, dependency-free color/format helpers. Auto-disabled when
# stdout isn't a TTY or TERM=dumb, or when --no-color is passed.

class Style:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDERLN = "\033[4m"

    # Foreground colors.
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    # Bright foreground colors.
    BRED    = "\033[91m"
    BGREEN  = "\033[92m"
    BYELLOW = "\033[93m"
    BBLUE   = "\033[94m"
    BMAGENTA= "\033[95m"
    BCYAN   = "\033[96m"

    # Box-drawing characters (Unicode).
    HLINE   = "─"
    VLINE   = "│"
    TLC     = "┌"
    TRC     = "┐"
    BLC     = "└"
    BRC     = "┘"
    LCROSS  = "├"
    RCROSS  = "┤"
    BULLET  = "•"
    ARROW   = "→"
    CHECK   = "✓"
    CROSS   = "✗"
    WARN    = "⚠"


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "") == "dumb":
        return False
    return sys.stdout.isatty() and sys.stderr.isatty()


def _set_color(enabled: bool) -> None:
    Style.enabled = enabled


# Default: enabled if TTY.
Style.enabled = _color_enabled()


def c(code: str, text: str) -> str:
    """Wrap text in an ANSI code, honouring the global enabled flag."""
    if not getattr(Style, "enabled", True):
        return text
    return f"{code}{text}{Style.RESET}"


def _strip(s: str) -> str:
    """Remove ANSI escape codes from a string (for width calculations)."""
    return re.sub(r"\033\[[0-9;]*m", "", s)


# Convenience helpers for common styling roles.
def path(text: str)   -> str: return c(Style.YELLOW, text)
def file(text: str)   -> str: return c(Style.BCYAN, text)
def heading(text: str) -> str: return c(Style.BOLD + Style.BCYAN, text)
def subhead(text: str) -> str: return c(Style.BOLD, text)
def prompt_chr()      -> str: return c(Style.BOLD + Style.BGREEN, "?")
def success(text: str) -> str: return c(Style.BGREEN, text)
def warn(text: str)    -> str: return c(Style.BYELLOW, text)
def error(text: str)   -> str: return c(Style.BRED, text)
def dim(text: str)     -> str: return c(Style.DIM, text)
def key(text: str)     -> str: return c(Style.BMAGENTA, text)
def val(text: str)     -> str: return c(Style.BCYAN, text)
def arrow()            -> str: return c(Style.DIM, Style.ARROW)


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


def prompt(label: str, default: str = "", allow_empty: bool = False) -> str:
    """Prompt the user for a single-line answer.

    `label` is the human-readable question; `default` is used when the
    user just presses Enter. If `allow_empty` is True, an empty answer
    is accepted even when no default is set.
    """
    suffix = f" {dim('[' + default + ']')}" if default else ""
    while True:
        try:
            ans = input(f"  {prompt_chr()} {label}{suffix}: ").strip()
        except EOFError:
            print()
            return default
        if not ans:
            ans = default
        if ans or allow_empty:
            return ans
        print(f"  {warn('!')} please enter a value, or Ctrl-C to abort")


def confirm(msg: str, default_no: bool = True) -> bool:
    suffix = f" {dim('[y/N]' if default_no else '[Y/n]')}"
    try:
        ans = input(f"  {prompt_chr()} {msg}{suffix}: ").strip().lower()
    except EOFError:
        return False
    if not ans:
        return not default_no
    return ans in ("y", "yes")


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

def rewrite_mount(text: str, old: str, new: str, extra: list[tuple[str, str]]) -> tuple[str, int]:
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
    files = find_files(DEFAULT_SEARCH_DIRS)  # both .mta and .json
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

# Pattern that captures a JSON string value (handles \" and \\ escapes).
_JSON_STR = r'"((?:[^"\\]|\\.)*)"'


def replace_format_in_mta(text: str, action: str, genre: str, new_format: str) -> tuple[str, int]:
    """Replace the `1=<format>` line under `F=_FILENAME` in a .mta file."""
    new_text, n = re.subn(
        r'(F=_FILENAME[ \t]*\n)1=[^\n]+',
        lambda m: m.group(1) + "1=" + new_format,
        text, count=1,
    )
    return new_text, 1 if n else 0


def replace_format_in_json_line(line: str, action: str, genre: str,
                                new_format: str, new_format_escaped: str) -> tuple[str, int]:
    """Replace the `format` value in one JSON line, if the line contains this genre.

    Handles both the unescaped form (as in `Eksternal.json`) and the JSON-escaped
    form (as in `Action Groups.json`).
    """
    if action == "C":
        marker        = f"/{genre}/{COMPILATION_MARKER}"
        marker_escaped = marker.replace("/", "\\/")
    elif action == "S":
        marker        = f"/{genre}/{SPLIT_MARKER}"
        marker_escaped = marker.replace("/", "\\/")
    else:
        marker        = f"/{genre}/"
        marker_escaped = marker.replace("/", "\\/")

    if marker not in line and marker_escaped not in line:
        return line, 0

    # Use the escaped form of the new format string to match the JSON style.
    new_text, n = re.subn(
        r'("format"\s*:\s*)' + _JSON_STR,
        lambda m: m.group(1) + '"' + new_format_escaped + '"',
        line, count=1,
    )
    return new_text, 1 if n else 0


def replace_layout_in_json(text: str, layout: dict, new_mount: str) -> tuple[str, int]:
    """Replace every `format` value in the Eksternal action groups of a JSON file.

    Two-pass approach: first find every action title (in order), then find
    every `format` line (in order) and apply the matching layout. Format
    lines and title lines appear in the same order in the JSON, so they
    can be paired by position.

    `new_mount` is the post-retarget mount (e.g. `/Volumes/MyExternal/Music/`).
    """
    lines = text.split("\n")

    # Pass 1: collect (action_type, genre) for every recognized title.
    actions: list[tuple[str, str]] = []
    title_re = re.compile(r'"title"\s*:\s*' + _JSON_STR)
    for line in lines:
        m = title_re.search(line)
        if m:
            kind, genre = _title_to_action(m.group(1))
            if kind:
                actions.append((kind, genre))

    # Pass 2: replace every format line, pairing it with the next action.
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
            line, n = replace_format_in_json_line(line, kind, genre, new_format, new_format_escaped)
            total += n
        out_lines.append(line)

    return "\n".join(out_lines), total


def _title_to_action(title: str) -> tuple[str | None, str | None]:
    """Map an action title to (action_type, genre).

    Recognised prefixes:
      E - <Genre>            -> E
      D - <Genre>            -> D
      C - <Genre> - Compilation  -> C
      S - <Genre> - Split        -> S
      DC - <Genre> Compilation   -> DC  (compilation + disc subfolder)
    """
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

def rewrite_file(path: Path, old_mount: str, new_mount: str,
                 extra: list[tuple[str, str]], layout: dict | None) -> tuple[str, int, str]:
    """Apply mount retargeting and/or layout application to a file.

    Returns (new_text, total_change_count, first_sample_line).
    """
    text = path.read_text(encoding="utf-8")
    new_text = text
    total = 0
    sample = ""

    # Mount retargeting.
    if old_mount and new_mount and old_mount != new_mount or extra:
        new_text, n = rewrite_mount(new_text, old_mount, new_mount, extra)
        total += n
        if n and not sample:
            sample = sample_change(new_text, old_mount, extra)

    # Layout application.
    if layout is not None:
        mount = new_mount or old_mount
        if path.suffix == ".mta":
            action, genre = detect_action(path.name)
            if action and genre:
                new_format = build_format_string(layout, action, mount, genre)
                new_text, n = replace_format_in_mta(new_text, action, genre, new_format)
                total += n
                if n and not sample:
                    sample = f"{action} {genre}: {new_format[:60]}…"
        elif path.suffix == ".json":
            new_text, n = replace_layout_in_json(new_text, layout, mount)
            total += n
            if n and not sample:
                sample = f"layout '{layout['name']}' applied to {n} format string(s)"

    return new_text, total, sample


# =====================================================================
# Interactive UI
# =====================================================================

BANNER_LINES = [
    "retarget-paths.py",
    "rewrite personal file paths and folder layout",
]


def _hr(width: int = 70, char: str = Style.HLINE) -> str:
    return char * width


def print_banner() -> None:
    bar = c(Style.DIM, _hr(70))
    title = heading("retarget-paths.py")
    subtitle = c(Style.DIM, "rewrite personal file paths and folder layout")
    print()
    print(f"  {title}")
    print(f"  {subtitle}")
    print(f"  {bar}")
    print(f"  {dim('Repo root:')} {path(str(REPO_ROOT))}")
    print(f"  {bar}")
    print()


def print_layout_list() -> None:
    print(heading("Available layouts"))
    print(dim(_hr(60)))
    name_w = max(len(n) for n in list_layouts())
    for name in list_layouts():
        L = get_layout(name)
        print()
        print(f"  {key(name):<{name_w+9}}  {val(L['description'])}")
        print(f"  {'':<{name_w+9}}  {dim('e.g.')}  {L['example']}")
        print(f"  {'':<{name_w+9}}  {dim('use:')}   {L['use_case']}")
    print()


def print_layout_detail(name: str) -> None:
    L = get_layout(name)
    print(heading(f"Layout: {L['name']}  ({key(repr(name))})"))
    print(dim(_hr(60)))
    print(f"  {dim('Description:')}  {L['description']}")
    print(f"  {dim('Example:    ')}  {L['example']}")
    print(f"  {dim('Use case:  ')}  {L['use_case']}")
    print()
    print(f"  {subhead('Format-string templates (run after the genre folder):')}")
    print()
    for kind in ("E", "D", "C", "DC", "S"):
        kind_lbl = {"E": "E (standard album)",     "D": "D (with Disc N/)",
                    "C": "C (compilation)",         "DC": "DC (compilation + disc)",
                    "S": "S (split)"}.get(kind, kind)
        print(f"    {key(f'{kind:<2}')}  {dim(kind_lbl + ':'):<28}  {val(L[kind])}")
    print()


def _section(n: int, total: int, title: str) -> None:
    """Print a numbered step header."""
    bar = c(Style.DIM, _hr(70, Style.HLINE))
    print(bar)
    print(f"  {subhead(f'Step {n} of {total}')}  {heading(title)}")
    print(bar)


def _info_block(lines: list[str]) -> None:
    for line in lines:
        print(f"  {line}")


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description=("Rewrite the hard-coded library mount and/or folder layout in the "
                     "Eksternal action templates. Run with no arguments for an interactive "
                     "wizard, or pass --new / --layout for non-interactive use."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Examples:\n"
                "  python3 Scripts/retarget-paths.py\n"
                "  python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --yes\n"
                "  python3 Scripts/retarget-paths.py --layout standard --yes\n"
                "  python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ \\\n"
                "                                       --layout chronological --yes\n"
                "  python3 Scripts/retarget-paths.py --list-layouts\n"),
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
                    help="Also rewrite /Audio/<Genre>/ → /Music/<Genre>/. Off by default; "
                         "enable this if your new root still uses an 'Audio' parent folder "
                         "and you want to rename it to 'Music' as well.")
    ap.add_argument("--out", default=None, metavar="DIR",
                    help="Write a retargeted copy under DIR. Mutually exclusive with --stdout.")
    ap.add_argument("--stdout", action="store_true",
                    help="Write Actions/Action Groups.json to stdout. Mutually exclusive with --out.")
    ap.add_argument("--no-interactive", action="store_true",
                    help="Disable interactive mode. Errors out if --new and --layout are both missing.")
    ap.add_argument("--no-color", action="store_true",
                    help="Disable ANSI color output (also auto-disabled when stdout is not a TTY).")
    ap.add_argument("--json-only", action="store_true",
                    help="Process only JSON files (skip the per-action .mta scripts). "
                         "Useful for bulk retargeting when the .mta files would be "
                         "regenerated from the JSON anyway, or when you only need the "
                         "master Action Groups.json as the importable bundle.")
    args = ap.parse_args()

    if args.no_color:
        _set_color(False)

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

    if args.out and args.stdout:
        print(f"  {error('--out and --stdout are mutually exclusive')}", file=sys.stderr)
        return 2

    interactive = not args.no_interactive and sys.stdin.isatty()

    if interactive:
        print_banner()
        print(f"  This wizard rewrites the {path('Eksternal')} action groups so the bundled")
        print(f"  templates point at {key('your')} library mount and folder layout. The")
        print(f"  flow is: {key('Save Location')} {arrow()} {key('Filename Structure')} {arrow()} "
              f"{key('File Scope')} {arrow()} {key('Output Mode')}. Each step has a sensible")
        print(f"  default — just press {key('Enter')} to accept it.")
        print()

    # =====================================================================
    # Step 1 of 4: Save Location
    # =====================================================================
    # The Save Location step is the foundation — it answers "where will
    # Mp3tag save files?". Subsequent steps (filename structure, etc.)
    # build on top of this.
    mount_change = bool(args.new) or (interactive and not args.layout)
    if args.old is not None:
        old = normalize(args.old)
    elif interactive and mount_change:
        current = detect_current_state()
        suggested_old = current or DEFAULT_OLD
        _section(1, 4, "Save Location — where will Mp3tag save your files?")
        _info_block([
            f"  {dim('The bundled actions ship with a hard-coded mount path. Tell the script which')}",
            f"  {dim('path to replace, then where your files should actually go.')}",
            f"  {''}",
            f"  {dim('Bundled default:')}  {path(DEFAULT_OLD)}",
            *([f"  {dim('Currently used: ')}  {path(current)}"] if current and current != DEFAULT_OLD else []),
        ])
        print()
        # 1a: old mount
        raw = prompt("Old mount path (which to replace)", suggested_old, allow_empty=True)
        old = normalize(raw)
        # 1b: new mount
        if old or mount_change:
            print()
            _info_block([
                f"  {dim('Now pick the save destination — this is the path Mp3tag will write to')}",
                f"  {dim('when the Eksternal actions run. Examples:')}",
                f"    {path('/Volumes/MyExternal/Music/')}",
                f"    {path('/Volumes/Backup/Audio/')}",
                f"    {path('~/Music/')}        {dim('(tilde is expanded to your home directory)')}",
                f"  {dim('Leave blank to keep the current mount.')}",
            ])
            print()
            while True:
                new = normalize(prompt("New mount path (save destination)", allow_empty=True))
                if not new:
                    new = old
                    break
                abs_new = expand(new).rstrip("/")
                if not os.path.isabs(abs_new):
                    print(f"  {warn('!')} {path(new)!r} is not an absolute path. Use a leading {key('/')} or {key('~/')}.")
                    continue
                if not os.path.exists(abs_new):
                    print(f"  {warn('!')} {path(abs_new)!r} does not currently exist on disk.")
                    if not confirm("Continue anyway?", default_no=True):
                        continue
                break
        else:
            new = old
    else:
        old = normalize(DEFAULT_OLD) if mount_change else ""
        if args.new is not None:
            new = normalize(args.new)
        else:
            new = old

    if old and new and old == new:
        if mount_change and not args.layout:
            print(f"  {dim('i')} old and new are the same ({path(old)!r}); nothing to do for the mount.")
            if not interactive:
                return 0
        old = new

    # =====================================================================
    # Step 2 of 4: Filename Structure
    # =====================================================================
    # Builds on the Save Location — same genre folders, but reorganised
    # according to a layout preset.
    if args.include_genre_rewrites:
        extra = DEFAULT_GENRE_REWRITES
    elif interactive and (mount_change or not old):
        _section(2, 4, "Filename Structure — how should files be organised?")
        _info_block([
            f"  {dim('Pick a layout preset for the folder hierarchy inside your save location.')}",
            f"  {dim('You can also optionally rename')} {path('/Audio/')} {dim('to')} {path('/Music/')} {dim('as the parent.')}",
        ])
        print()
        names = list_layouts()
        for i, n in enumerate(names, 1):
            L = get_layout(n)
            print(f"    {key(str(i) + '.')} {subhead(L['name']):<28}  {dim(L['description'])}")
        print(f"    {key(str(len(names)+1) + '.')} {subhead('(no layout change)'):<28}  {dim('keep the current folder structure')}")
        print()
        while True:
            choice = prompt(f"Layout (1-{len(names)+1})", str(len(names)+1))
            try:
                idx = int(choice) - 1
                if idx == len(names):
                    layout = None
                    break
                if 0 <= idx < len(names):
                    layout = get_layout(names[idx])
                    break
            except ValueError:
                pass
            print(f"  {warn('!')} please enter a number between {key('1')} and {key(str(len(names)+1))}.")
        print()
        if confirm(f"Rename the genre subfolders {path('/Audio/<Genre>/')} → {path('/Music/<Genre>/')}?", default_no=True):
            extra = DEFAULT_GENRE_REWRITES
        else:
            extra = []
    else:
        extra = []

    if args.layout is not None:
        try:
            layout = get_layout(args.layout)
        except KeyError as e:
            print(f"  {error(str(e))}", file=sys.stderr)
            return 2
    elif not interactive:
        layout = None
    # (When interactive and no --layout given, the user already chose
    # above in the combined Filename Structure step.)

    if not mount_change and layout is None and not extra:
        if args.new is None and args.old is None and args.layout is None:
            print(f"  {error('error:')} pass {key('--new')}, {key('--layout')}, or both "
                  f"(or run without {key('--no-interactive')})", file=sys.stderr)
            return 2
        print(f"  {dim('i')} nothing to do.")
        return 0

    # =====================================================================
    # Step 3 of 4: File Scope
    # =====================================================================
    if interactive and not args.json_only and not args.stdout:
        _section(3, 4, "File Scope — which files should be rewritten?")
        _info_block([
            f"  {dim('The script can write to both the per-action')} {file('.mta')} {dim('files and the')}",
            f"  {dim('JSON action groups, or just the JSONs. For bulk retargeting the JSONs are')}",
            f"  {dim('usually enough — the')} {file('.mta')} {dim('files can be regenerated from them.')}",
        ])
        print()
        print(f"    {key('1.')} {subhead('Both .mta and JSON'):<22}  rewrite the per-action scripts and the JSONs (default).")
        print(f"    {key('2.')} {subhead('JSON only'):<22}  skip the per-action .mta files; only rewrite the JSONs.")
        print(f"                           {dim('Useful for bulk retargeting when you just need the importable bundle.')}")
        print()
        choice = prompt("File scope (1/2)", "1").strip()
        if choice == "2":
            args.json_only = True

    # =====================================================================
    # Step 4 of 4: Output Mode
    # =====================================================================
    if interactive and not args.stdout and not args.out and not args.yes:
        _section(4, 4, "Output Mode — where should the rewritten files go?")
        print()
        print(f"    {key('1.')} {subhead('In-place'):<14}  rewrite the existing files in this repo.")
        print(f"                     {dim('(use this if you have forked the repo and want upstream to match)')}")
        print(f"    {key('2.')} {subhead('To a directory'):<14}  leave the originals untouched and")
        print(f"                     write a retargeted copy to {key('DIR')}.")
        print(f"    {key('3.')} {subhead('To stdout'):<14}  print {file('Actions/Action Groups.json')} to the")
        print(f"                     terminal for piping / clipboard import.")
        print()
        choice = prompt("Output mode (1/2/3)", "1").strip()
        if choice == "2":
            out_dir = None
            while not out_dir:
                entered = prompt("Output directory")
                if not entered:
                    print(f"  {warn('!')} a path is required.")
                    continue
                out_dir = Path(expand(entered)).resolve()
            args.out = str(out_dir)
        elif choice == "3":
            args.stdout = True
        # else: in-place (default)

    # =====================================================================
    # Review
    # =====================================================================
    if interactive and not args.yes:
        bar = c(Style.DIM, _hr(70))
        print(bar)
        print(f"  {subhead('Review')}  {dim('(confirm to apply)')}")
        print(bar)
        if old and new and old != new:
            print(f"  {dim('Save location:   ')}  {path(old)}  {arrow()}  {path(new)}")
        else:
            print(f"  {dim('Save location:   ')}  {dim('(no change)')}")
        if layout:
            print(f"  {dim('Filename struct: ')}  {val(layout['name'])} {dim('—')} {dim(layout['description'])}")
        else:
            print(f"  {dim('Filename struct: ')}  {dim('(keep current)')}")
        if extra:
            print(f"  {dim('Genre rename:    ')}  {len(extra)} rule(s) "
                  f"({path(extra[0][0])}  {arrow()}  {path(extra[0][1])}, {dim('…')})")
        else:
            print(f"  {dim('Genre rename:    ')}  {dim('none')}")
        if args.stdout:
            print(f"  {dim('File scope:      ')}  {dim('JSON only')} {dim('(stdout is always JSON)')}")
        elif args.json_only:
            print(f"  {dim('File scope:      ')}  {val('JSON only')} {dim('(skips per-action .mta scripts)')}")
        else:
            print(f"  {dim('File scope:      ')}  {val('.mta + JSON')} {dim('(both per-action scripts and JSONs)')}")
        if args.stdout:
            print(f"  {dim('Output:          ')}  {dim('stdout')} {dim('(')}{file('Actions/Action Groups.json')}{dim(')')}")
        elif args.out:
            print(f"  {dim('Output:          ')}  {path(args.out + '/')}  {dim('(rewritten copy, originals untouched)')}")
        else:
            print(f"  {dim('Output:          ')}  {dim('in-place')} {dim('(rewrites source files)')}")
        print(bar)
        print()
        if not confirm("Proceed?", default_no=True):
            print(f"  {warn('Aborted.')}")
            return 1
        print(bar)
        print()
        if not confirm("Proceed?", default_no=True):
            print(f"  {warn('Aborted.')}")
            return 1

    # =====================================================================
    # Scan
    # =====================================================================
    files = find_files(DEFAULT_SEARCH_DIRS, json_only=args.json_only)
    if not files:
        kind = "JSON" if args.json_only else ".mta or .json"
        print(f"  {error(f'No {kind} files found.')}", file=sys.stderr)
        return 1

    plan: list[tuple[Path, int, str]] = []
    for f in files:
        try:
            new_text, n, sample = rewrite_file(f, old, new, extra, layout)
        except UnicodeDecodeError:
            continue
        if n:
            plan.append((f, n, sample))

    if not plan:
        print(f"  {warn('No changes would be made')} (searched {len(files)} files).")
        return 0

    total = sum(n for _, n, _ in plan)
    out = sys.stderr if args.stdout else sys.stdout

    bar = c(Style.DIM, _hr(70))
    print(bar, file=out)
    print(f"  {subhead(f'Plan')}  {dim('—')} {total} change(s) across {len(plan)} file(s)", file=out)
    print(bar, file=out)
    for f, n, sample in plan:
        try:
            rel = f.relative_to(REPO_ROOT)
        except ValueError:
            rel = f
        line = f"  {val(str(n).rjust(3))}  {file(str(rel))}"
        if sample:
            line += f"  {dim('  e.g.')}  {path(sample)}"
        print(line, file=out)
    print(bar, file=out)
    print(file=out)

    if args.dry_run:
        print(f"  {warn('Dry run — no files written.')}")
        return 0

    if not args.yes:
        if interactive:
            ans = confirm(f"Apply these {total} change(s)?", default_no=True)
        else:
            ans = input(f"  {prompt_chr()} Apply these {total} change(s)? {dim('[y/N]')}: ").strip().lower() in ("y", "yes")
        if not ans:
            print(f"  {warn('Aborted.')}")
            return 1

    # =====================================================================
    # Apply
    # =====================================================================
    if args.stdout:
        if not MASTER_JSON.exists():
            print(f"  {error(str(MASTER_JSON) + ' not found')}", file=sys.stderr)
            return 1
        new_text, _, _ = rewrite_file(MASTER_JSON, old, new, extra, layout)
        sys.stdout.write(new_text)
        if not new_text.endswith("\n"):
            sys.stdout.write("\n")
        print(f"\n  {success('Done.')} Wrote {total} change(s) to stdout. "
              f"Pipe or paste into Mp3tag via {key('Actions → File → Import Action Groups…')}",
              file=sys.stderr)
        return 0

    if args.out:
        out_root = Path(expand(args.out)).resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        written = 0
        for f, _, _ in plan:
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
        print(f"  {success('Done.')} Wrote {val(str(written))} file(s) under "
              f"{path(str(out_root) + '/')}  {dim('(originals untouched)')}")
        print(f"  Import {file(str(out_root / 'Actions' / 'Action Groups.json'))} into Mp3tag "
              f"to load the rewritten actions.")
        return 0

    # In-place.
    written = 0
    for f, _, _ in plan:
        new_text, _, _ = rewrite_file(f, old, new, extra, layout)
        if new_text != f.read_text(encoding="utf-8"):
            f.write_text(new_text, encoding="utf-8")
            written += 1

    print(f"  {success('Done.')} Wrote {val(str(written))} file(s). Re-import "
          f"{file('Actions/Action Groups.json')} into Mp3tag "
          f"{dim('(or refresh the existing imported groups)')} to pick up the changes.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print(f"\n  {warn('Aborted.')}")
        raise SystemExit(130)
