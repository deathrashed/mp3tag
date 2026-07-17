"""
Layouts — preset folder and file naming structures for the Eksternal save
actions. Each layout defines four format-string templates, one per action
type (E, D, C, S), that replace the post-genre portion of every bundled
.mta and .json file.

The genre folder (e.g. `<mount>/Electronic/`) is always preserved — the
bundled actions are split per-genre, so the layout only controls what comes
*after* the genre root.

Templates are written in Mp3tag scripting — see
https://docs.mp3tag.de/scripting/functions/ for the full reference.

How the action type is detected
------------------------------

From the filename:
  `E - <Genre>.mta`              → E  (standard album, no disc)
  `D - <Genre>.mta`              → D  (with Disc N/ subfolder)
  `C - <Genre> - Compilation.mta`→ C  (under -Compilations-)
  `S - <Genre> - Split.mta`      → S  (under -Splits-)
"""

from __future__ import annotations

import re
from pathlib import Path

# Action types derived from filename patterns.
ACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^E - (.+)\.mta$"),                                          "E"),
    (re.compile(r"^D - (.+)\.mta$"),                                          "D"),
    (re.compile(r"^C - (.+) - Compilation\.mta$"),                            "C"),
    (re.compile(r"^S - (.+) - Split\.mta$"),                                  "S"),
    (re.compile(r"^DC - (.+) Compilation\.mta$"),                             "DC"),
]


def detect_action(filename: str) -> tuple[str | None, str | None]:
    """Return (action_type, genre) for a given .mta filename, or (None, None)."""
    base = Path(filename).name
    for pat, kind in ACTION_PATTERNS:
        m = pat.match(base)
        if m:
            return kind, m.group(1)
    return None, None


# Special marker subfolders used by the bundled templates.
COMPILATION_MARKER = "-Compilations-"
SPLIT_MARKER       = "-Splits-"


# The shared "first letter" snippet used by the alphabetical layout.
# Strips a leading "The " from the album artist and returns the first
# character of the result, so "The Beatles" → "B".
FIRST_LETTER = (
    "$if($eql($left(%albumartist%,4),The ),"
    "$left($right(%albumartist%,$sub($len(%albumartist%),4)),1),"
    "$left(%albumartist%,1))"
)

# Reusable fragments.
YEAR_PREFIX   = "$if(%year%,$left(%year%,4) - ,)"
DISC_SUBFOLDER = "$if(%discnumber%,Disc $num(%discnumber%,1)/,)"
TRACK_TITLE   = "$num(%track%,2). %title%"
TRACK_ARTIST  = "$num(%track%,2). %artist% - %title%"


LAYOUTS: dict[str, dict] = {

    # 1. Standard Hierarchy
    # Artist / Album / TrackNo - Title.ext
    "standard": {
        "name": "Standard Hierarchy",
        "description": "Artist / Album / TrackNo - Title",
        "use_case": "Standard organisation. Suitable for most media players and general listening.",
        "example": "Daft Punk / Discovery / 01 - One More Time.mp3",
        "E":  "%albumartist%/%album%/" + TRACK_TITLE,
        "D":  "%albumartist%/%album%/" + DISC_SUBFOLDER + TRACK_TITLE,
        "C":  "%album%/" + TRACK_ARTIST,
        "DC": "%album%/" + DISC_SUBFOLDER + TRACK_ARTIST,
        "S":  "%albumartist%/%album%/" + TRACK_ARTIST,
    },

    # 2. Chronological by Artist
    # Artist / Year - Album / TrackNo - Title.ext
    "chronological": {
        "name": "Chronological by Artist",
        "description": "Artist / Year - Album / TrackNo - Title",
        "use_case": "Tracking artist evolution over time. Keeps albums sorted by release date rather than alphabetically.",
        "example": "The Beatles / 1969 - Abbey Road / 01 - Come Together.flac",
        "E":  "%albumartist%/" + YEAR_PREFIX + "%album%/" + TRACK_TITLE,
        "D":  "%albumartist%/" + YEAR_PREFIX + "%album%/" + DISC_SUBFOLDER + TRACK_TITLE,
        "C":  YEAR_PREFIX + "%album%/" + TRACK_ARTIST,
        "DC": YEAR_PREFIX + "%album%/" + DISC_SUBFOLDER + TRACK_ARTIST,
        "S":  "%albumartist%/" + YEAR_PREFIX + "%album%/" + TRACK_ARTIST,
    },

    # 4. Alphabetical Grouping (the maintainer's current layout)
    # FirstLetter / Artist / Album / TrackNo - Title.ext
    "alphabetical": {
        "name": "Alphabetical Grouping",
        "description": "FirstLetter / Artist / Album / TrackNo - Title",
        "use_case": "Extremely large libraries. Prevents operating system strain and excessive scrolling when browsing root directories.",
        "example": "M-R / Nirvana / Nevermind / 01 - Smells Like Teen Spirit.mp3",
        "E":  FIRST_LETTER + "/%albumartist%/%album%/" + TRACK_TITLE,
        "D":  FIRST_LETTER + "/%albumartist%/%album%/" + DISC_SUBFOLDER + TRACK_TITLE,
        "C":  FIRST_LETTER + "/%album%/" + TRACK_ARTIST,
        "DC": FIRST_LETTER + "/%album%/" + DISC_SUBFOLDER + TRACK_ARTIST,
        "S":  FIRST_LETTER + "/%albumartist%/%album%/" + TRACK_ARTIST,
    },

    # 9. Flat Directory (Metadata Reliant)
    # Artist - Year - Album - TrackNo - Title.ext
    "flat": {
        "name": "Flat Directory",
        "description": "TrackNo - Artist - Year - Album - Title (all files in the genre root)",
        "use_case": "Dumping all files into a single genre folder. Relies entirely on the media player reading internal metadata (ID3 tags) rather than folder structure.",
        "example": "Pink Floyd - 1973 - The Dark Side of the Moon - 01 - Speak to Me.mp3",
        "E":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - %title%",
        "D":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - " + DISC_SUBFOLDER.replace("/", " - ") + "%title%",
        "C":  "$num(%track%,2) - %album% - %artist% - %title%",
        "DC": "$num(%track%,2) - %album% - " + DISC_SUBFOLDER.replace("/", " - ") + "%artist% - %title%",
        "S":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - %artist% - %title%",
    },
}


def get(name: str) -> dict:
    """Return a layout by name, or raise KeyError."""
    if name not in LAYOUTS:
        raise KeyError(
            f"Unknown layout {name!r}. Available: {', '.join(sorted(LAYOUTS))}"
        )
    return LAYOUTS[name]


def list_layouts() -> list[str]:
    return sorted(LAYOUTS.keys())


def build_format_string(layout: dict, action: str, mount: str, genre: str) -> str:
    """Return the full /<mount>/<genre>/<...> format string for an action."""
    template = layout[action]
    if action in ("C", "DC"):
        return f"{mount}{genre}/{COMPILATION_MARKER}/{template}"
    if action == "S":
        return f"{mount}{genre}/{SPLIT_MARKER}/{template}"
    return f"{mount}{genre}/{template}"
