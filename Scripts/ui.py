"""
ui.py — shared CLI presentation kit for the configure wizard
==============================================================

Colours, box-drawing, and prompt primitives shared by retarget-paths.py,
library.py, and custom_layout.py.  Every interactive prompt in the wizard
goes through this module so navigation (Back / Help / Quit) behaves the
same everywhere.

Navigation
----------

Any prompt built on `ask()`, `select()`, or `confirm()` recognises three
reserved tokens shown in the footer of every step:

    b, back     -> raises WizardBack    (caller re-runs the previous step)
    ?, help     -> prints step-specific help, then re-prompts
    q, quit     -> raises WizardQuit    (caller exits cleanly)
"""

from __future__ import annotations

import os
import re
import sys
import textwrap


class WizardBack(Exception):
    """Raised when the user asks to return to the previous step."""


class WizardQuit(Exception):
    """Raised when the user asks to exit the wizard."""


# =====================================================================
# Sample values used for every layout preview so users can compare
# presets against a single consistent reference release.
# =====================================================================

SAMPLE = {
    "artist":     "Iron Maiden",
    "album":      "Powerslave",
    "year":       "1984",
    "decade":     "1980s",
    "genre":      "Heavy Metal",
    "first_letter": "I",
    "track":      "02",
    "title":      "Aces High",
    "ext":        "flac",
    "disc":       "1",
    "disc_track": "05",
    "disc_title": "The Number of the Beast",
}


# =====================================================================
# ANSI styling
# =====================================================================

class Style:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDERLN = "\033[4m"

    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    BRED    = "\033[91m"
    BGREEN  = "\033[92m"
    BYELLOW = "\033[93m"
    BBLUE   = "\033[94m"
    BMAGENTA= "\033[95m"
    BCYAN   = "\033[96m"

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
    BOX     = "□"
    BOXCHK  = "☑"
    HEAVY   = "━"

    enabled = True


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "") == "dumb":
        return False
    return sys.stdout.isatty() and sys.stderr.isatty()


def set_color(enabled: bool) -> None:
    Style.enabled = enabled


Style.enabled = _color_enabled()


def c(code: str, text: str) -> str:
    if not getattr(Style, "enabled", True):
        return text
    return f"{code}{text}{Style.RESET}"


def strip_ansi(s: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", s)


def visible_len(s: str) -> int:
    return len(strip_ansi(s))


# Convenience helpers for common styling roles.
def path(text: str)    -> str: return c(Style.YELLOW, text)
def file(text: str)    -> str: return c(Style.BCYAN, text)
def heading(text: str) -> str: return c(Style.BOLD + Style.BCYAN, text)
def subhead(text: str) -> str: return c(Style.BOLD, text)
def prompt_chr()       -> str: return c(Style.BOLD + Style.BGREEN, "›")
def success(text: str) -> str: return c(Style.BGREEN, text)
def warn(text: str)    -> str: return c(Style.BYELLOW, text)
def error(text: str)   -> str: return c(Style.BRED, text)
def dim(text: str)     -> str: return c(Style.DIM, text)
def key(text: str)     -> str: return c(Style.BMAGENTA, text)
def val(text: str)     -> str: return c(Style.BCYAN, text)
def arrow()            -> str: return c(Style.DIM, Style.ARROW)
def badge(text: str)   -> str: return c(Style.BGREEN, text)
def muted(text: str)   -> str: return c(Style.DIM, text)


def hr(width: int = 70, char: str = Style.HLINE) -> str:
    return c(Style.DIM, char * width)


def heavy_rule(width: int = 56) -> str:
    return c(Style.DIM, Style.HEAVY * width)


# =====================================================================
# Structural helpers
# =====================================================================

def banner(title: str, subtitle: str, repo_root: str) -> None:
    print()
    w = 70
    print(f"  {c(Style.DIM, Style.HEAVY * w)}")
    print()
    print(f"  {heading(title)}")
    print(f"  {dim(subtitle)}")
    print()
    print(f"  {dim('Repo')}  {path(repo_root)}")
    print()
    print(f"  {c(Style.DIM, Style.HEAVY * w)}")
    print()


def section(n: int, total: int, title: str) -> None:
    """Step header with progress indicator."""
    progress = _progress_bar(n, total, width=20)
    label = f"Step {n} of {total}"
    print()
    print(f"  {c(Style.DIM, Style.HEAVY * 56)}")
    print(f"  {dim(label)}  {progress}")
    print(f"  {heading(title)}")
    print(f"  {c(Style.DIM, Style.HEAVY * 56)}")
    print()


def _progress_bar(n: int, total: int, width: int = 20) -> str:
    filled = round(width * n / total)
    bar = "█" * filled + "░" * (width - filled)
    pct = f"{round(100 * n / total)}%"
    return c(Style.DIM, f"[") + c(Style.BCYAN, bar) + c(Style.DIM, f"] {pct}")


def info(*lines: str) -> None:
    for line in lines:
        print(f"  {dim(line)}" if line else "")


def footer_hint() -> None:
    b = key("B") + dim("ack")
    h = key("?") + dim(" Help")
    q = key("Q") + dim("uit")
    print(f"  {dim('[')}{b}{dim(']')}  {dim('[')}{h}{dim(']')}  {dim('[')}{q}{dim(']')}")


def checklist(items: list[tuple[bool, str]]) -> None:
    """Print a list of (ok, label) as a validation checklist."""
    for ok, label in items:
        mark = success(Style.CHECK) if ok else error(Style.CROSS)
        print(f"  {mark}  {label}")


def divider(char: str = "─", width: int = 56) -> str:
    return c(Style.DIM, char * width)


def wrap_lines(text: str, width: int = 56) -> list[str]:
    if not text:
        return []
    return textwrap.wrap(text, width=width, replace_whitespace=True)


def print_wrapped(text: str, indent: int = 4, width: int = 54,
                  style=dim) -> None:
    pad = " " * indent
    for line in wrap_lines(text, width):
        print(f"{pad}{style(line)}")


def preview_block(title: str, preview: str, indent: int = 4) -> None:
    pad = " " * indent
    print(f"{pad}{subhead(title)}")
    print()
    for line in preview.splitlines():
        print(f"{pad}{dim(line)}")


def key_value(label: str, value: str, *, muted_val: bool = False) -> None:
    rendered = dim(value) if muted_val else val(value)
    print(f"  {dim(label):<24} {rendered}")


def current_value_block(label: str, value: str) -> None:
    """The 'Current  <value>  Press Enter to keep this option.' pattern."""
    print(f"  {dim(label)}")
    print(f"  {val(value)}")
    print(f"  {dim('Press Enter to keep this option.')}")
    print()


# =====================================================================
# Layout card  (used by the layout browser)
# =====================================================================

def layout_card(number: str | int, preset_name: str, structure: str,
                description: str, preview: str,
                *, selected: bool = False,
                preset_id: str = "", card_width: int = 64) -> None:
    """Render a single layout as a visually separated card block.

    Format::

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [1] Standard Hierarchy                           ✓ Current

             Artist / Album / Track

             Traditional music library structure.

             Preview

             Music/
             └── Iron Maiden/
                 └── Powerslave/
                     └── 02 Aces High.flac
    """
    rule = c(Style.DIM, Style.HEAVY * card_width)
    print(f"  {rule}")
    print()
    # Header line: [N] Name   [badge]
    num_str = key(f"[{number}]")
    name_str = subhead(preset_name)
    selected_badge = f"  {success('✓ Current')}" if selected else ""
    id_hint = f"  {dim('id:')} {dim(preset_id)}" if preset_id and not selected else ""
    print(f"  {num_str}  {name_str}{selected_badge}{id_hint}")
    print()
    # Structure
    print(f"       {dim(structure)}")
    print()
    # Description (wrapped)
    for line in wrap_lines(description, width=card_width - 10):
        print(f"       {dim(line)}")
    print()
    # Preview tree
    print(f"       {subhead('Preview')}")
    print()
    for line in preview.splitlines():
        print(f"       {dim(line)}")
    print()


# =====================================================================
# Option block  (used by file scope / output mode etc.)
# =====================================================================

def option_block(number: str | int, title: str,
                 description: str | list[str] = "",
                 *, badge: str = "", selected: bool = False,
                 block_width: int = 60) -> None:
    """Render one selectable option as a short block.

    Example::

        [1] Update this repository                  Recommended

             Updates the existing files in-place.

        ──────────────────────────────────────
    """
    mark = success(Style.CHECK + " ") if selected else "  "
    badge_str = f"  {success(badge)}" if badge else ""
    num_str = key(f"[{number}]")
    print(f"  {mark}{num_str}  {subhead(title)}{badge_str}")
    print()
    lines: list[str]
    if isinstance(description, str):
        lines = wrap_lines(description, width=block_width - 8)
    else:
        lines = list(description)
    for line in lines:
        print(f"       {dim(line)}")
    print()


def option_separator(width: int = 56) -> None:
    print(f"  {hr(width)}")
    print()


# =====================================================================
# Summary row (used by the config summary panel)
# =====================================================================

def summary_row(label: str, value: str, note: str = "") -> None:
    note_str = f"  {dim(note)}" if note else ""
    print(f"  {dim(f'{label:<18}')}  {val(value)}{note_str}")


# =====================================================================
# Input primitives
# =====================================================================

_RESERVED_BACK = {"b", "back"}
_RESERVED_HELP = {"?", "help"}
_RESERVED_QUIT = {"q", "quit"}


def _check_reserved(raw: str) -> None:
    token = raw.strip().lower()
    if token in _RESERVED_BACK:
        raise WizardBack()
    if token in _RESERVED_QUIT:
        raise WizardQuit()


def ask(label: str, default: str = "", allow_empty: bool = False,
        help_text: str = "", nav: bool = True) -> str:
    """Prompt for a single-line answer, honouring Back/Help/Quit tokens."""
    suffix = f" {dim('[' + default + ']')}" if default else ""
    while True:
        try:
            raw = input(f"  {prompt_chr()} {label}{suffix}: ")
        except EOFError:
            print()
            return default
        stripped = raw.strip()
        if nav:
            low = stripped.lower()
            if low in _RESERVED_BACK:
                raise WizardBack()
            if low in _RESERVED_QUIT:
                raise WizardQuit()
            if low in _RESERVED_HELP:
                print()
                print(f"  {subhead('Help')}")
                for line in wrap_lines(help_text or
                        "No additional help is available for this step.", 64):
                    print(f"  {dim(line)}")
                print()
                continue
        ans = stripped or default
        if ans or allow_empty:
            return ans
        print(f"  {warn('!')} Please enter a value, or type {key('b')} to go back.")


def confirm(msg: str, default_no: bool = True, help_text: str = "",
            nav: bool = True) -> bool:
    hint = dim("[y/N]") if default_no else dim("[Y/n]")
    while True:
        try:
            raw = input(f"  {prompt_chr()} {msg} {hint}: ")
        except EOFError:
            return False
        stripped = raw.strip().lower()
        if nav:
            if stripped in _RESERVED_BACK:
                raise WizardBack()
            if stripped in _RESERVED_QUIT:
                raise WizardQuit()
            if stripped in _RESERVED_HELP:
                print()
                print(f"  {subhead('Help')}")
                for line in wrap_lines(help_text or
                        "No additional help is available for this step.", 64):
                    print(f"  {dim(line)}")
                print()
                continue
        if not stripped:
            return not default_no
        return stripped in ("y", "yes")


def select(options: list[str], title: str | None = None,
           default_index: int = 0, help_text: str = "",
           nav: bool = True) -> int:
    """Numbered single-choice menu. Returns the 0-based index chosen."""
    if title:
        print(f"  {subhead(title)}")
        print()
    for i, opt in enumerate(options, 1):
        marker = success("›") if i == default_index + 1 else dim(" ")
        print(f"    {marker} {key(str(i) + '.')} {opt}")
    print()
    default_label = str(default_index + 1)
    while True:
        raw = ask(f"Choose (1–{len(options)})", default_label,
                  help_text=help_text, nav=nav)
        try:
            idx = int(raw) - 1
        except ValueError:
            print(f"  {warn('!')} Enter a number between {key('1')} "
                  f"and {key(str(len(options)))}")
            continue
        if 0 <= idx < len(options):
            return idx
        print(f"  {warn('!')} Enter a number between {key('1')} "
              f"and {key(str(len(options)))}")


# Backwards-compat alias kept so existing callers don't break.
def option_card(number: str, title: str, description: str | list[str] = "",
                *, badge: str = "", selected: bool = False,
                width: int = 62) -> None:
    option_block(number, title, description, badge=badge, selected=selected,
                 block_width=width)


def option_separator_old(width: int = 56) -> None:  # pragma: no cover
    option_separator(width)
