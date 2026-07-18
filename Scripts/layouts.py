"""
Layouts — preset folder and file naming structures for the Eksternal save
actions. Each layout defines up to five format-string templates, one per
action type (E, D, C, DC, S), that replace the post-genre portion of every
bundled .mta and .json file.

The genre *bucket* folder (e.g. `<mount>/Electronic/`) is always preserved
— the bundled actions are split per-genre-bucket, so a layout only
controls what comes *after* that root. A few presets additionally nest a
folder named after the Mp3tag `%genre%` tag itself (a finer-grained value
than the bucket, e.g. "Thrash Metal" inside the "Metal" bucket) — those
are noted in their description.

Templates are written in Mp3tag scripting — see
https://docs.mp3tag.de/scripting/functions/ for the full reference.

Adding a new preset requires only adding a new `LayoutPreset` to
`_RAW_PRESETS` below — nothing else in this file or in retarget-paths.py
needs to change.

How the action type is detected
--------------------------------

From the filename:
  `E - <Genre>.mta`               -> E   (standard album, no disc)
  `D - <Genre>.mta`               -> D   (with Disc N/ subfolder)
  `C - <Genre> - Compilation.mta` -> C   (under -Compilations-)
  `S - <Genre> - Split.mta`       -> S   (under -Splits-)
  `DC - <Genre> Compilation.mta`  -> DC  (compilation + disc subfolder)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ui import SAMPLE

# =====================================================================
# Action detection (unchanged wire format — consumed by retarget-paths.py)
# =====================================================================

ACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^E - (.+)\.mta$"),                "E"),
    (re.compile(r"^D - (.+)\.mta$"),                "D"),
    (re.compile(r"^C - (.+) - Compilation\.mta$"),  "C"),
    (re.compile(r"^S - (.+) - Split\.mta$"),        "S"),
    (re.compile(r"^DC - (.+) Compilation\.mta$"),   "DC"),
]


def detect_action(filename: str) -> tuple[str | None, str | None]:
    """Return (action_type, genre) for a given .mta filename, or (None, None)."""
    base = Path(filename).name
    for pat, kind in ACTION_PATTERNS:
        m = pat.match(base)
        if m:
            return kind, m.group(1)
    return None, None


COMPILATION_MARKER = "-Compilations-"
SPLIT_MARKER       = "-Splits-"


# =====================================================================
# Reusable Mp3tag scripting fragments
# =====================================================================

FIRST_LETTER = (
    "$if($eql($left(%albumartist%,4),The ),"
    "$left($right(%albumartist%,$sub($len(%albumartist%),4)),1),"
    "$left(%albumartist%,1))"
)
YEAR_PREFIX       = "$if(%year%,$left(%year%,4) - ,)"
YEAR_FOLDER       = "$if(%year%,$left(%year%,4),Unknown Year)"
YEAR_SUFFIX       = "%album% ($if(%year%,$left(%year%,4),Unknown))"
YEAR_PAREN_PREFIX = "$if(%year%,($left(%year%,4)) ,)%album%"
DECADE            = "$left(%year%,3)0s"
GENRE_TAG         = "$if(%genre%,%genre%,Unknown Genre)"
RELEASE_TYPE      = "$if(%releasetype%,%releasetype%,Albums)"
DISC_SUBFOLDER    = "$if(%discnumber%,Disc $num(%discnumber%,1)/,)"
TRACK_TITLE       = "$num(%track%,2). %title%"
TRACK_ARTIST      = "$num(%track%,2). %artist% - %title%"


def _variants(folder_e: str, folder_c: str,
              track_title: str = TRACK_TITLE, track_artist: str = TRACK_ARTIST,
              disc: str = DISC_SUBFOLDER) -> dict[str, str]:
    """Build the standard E/D/C/DC/S template set from a folder path.

    `folder_e` is the path used for normal albums (may reference
    %albumartist%). `folder_c` is the path used for compilations (should
    not reference %albumartist%, since compilations don't have one).
    """
    return {
        "E":  f"{folder_e}/{track_title}",
        "D":  f"{folder_e}/{disc}{track_title}",
        "C":  f"{folder_c}/{track_artist}",
        "DC": f"{folder_c}/{disc}{track_artist}",
        "S":  f"{folder_e}/{track_artist}",
    }


# =====================================================================
# Preset data model
# =====================================================================

@dataclass(frozen=True)
class LayoutPreset:
    id: str
    name: str
    description: str
    structure: str                 # human-readable, e.g. "Artist / Album / Track"
    templates: dict[str, str]      # E, D, C, DC, S -> Mp3tag format string
    category: str = "Common"
    preview: str = field(default="")
    note: str = ""

    def __getitem__(self, key: str) -> str:
        return self.templates[key]

    def get(self, key: str, default: str | None = None) -> str | None:
        return self.templates.get(key, default)


def _tree(folders: list[str], filename: str, root: str = "/Music/") -> str:
    """Render an ASCII folder tree preview using the shared sample values."""
    lines = [root]
    indent = "    "
    for depth, folder in enumerate(folders):
        lines.append(f"{indent * depth}└── {folder}/")
    lines.append(f"{indent * len(folders)}└── {filename}")
    return "\n".join(lines)


_S = SAMPLE  # shorthand
_FILE = f"{_S['track']} {_S['title']}.{_S['ext']}"
_FILE_ARTIST = f"{_S['track']} {_S['artist']} - {_S['title']}.{_S['ext']}"


# =====================================================================
# Presets
# =====================================================================
# Each entry mirrors one preset from Scripts/layout-presets.txt. A few
# genre/time-based presets from that reference document were merged with
# "standard" because this repo's action files are already split per
# genre bucket one level above every layout (see module docstring) —
# adding an identical folder there would be redundant. Where merging
# happened the description says so.

_RAW_PRESETS: list[LayoutPreset] = [

    LayoutPreset(
        id="standard",
        name="Standard Hierarchy",
        description="The classic music library structure used by most collectors.",
        structure="Artist / Album / TrackNo - Title",
        category="Common",
        templates=_variants("%albumartist%/%album%", "%album%"),
        preview=_tree([_S["artist"], _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="artist_year_album",
        name="Artist by Year",
        description="Groups albums chronologically beneath each artist.",
        structure="Artist / Year - Album / TrackNo - Title",
        category="Common",
        templates=_variants(
            "%albumartist%/" + YEAR_PREFIX + "%album%",
            YEAR_PREFIX + "%album%",
        ),
        preview=_tree([_S["artist"], f"{_S['year']} - {_S['album']}"], _FILE),
    ),

    LayoutPreset(
        id="artist_year_folder",
        name="Artist → Year → Album",
        description="Places the year in its own folder instead of the album name.",
        structure="Artist / Year / Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants(
            "%albumartist%/" + YEAR_FOLDER + "/%album%",
            YEAR_FOLDER + "/%album%",
        ),
        preview=_tree([_S["artist"], _S["year"], _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="album_year_suffix",
        name="Album (Year)",
        description="Displays the release year after the album title.",
        structure="Artist / Album (Year) / TrackNo - Title",
        category="Time & Genre",
        templates=_variants("%albumartist%/" + YEAR_SUFFIX, YEAR_SUFFIX),
        preview=_tree([_S["artist"], f"{_S['album']} ({_S['year']})"], _FILE),
    ),

    LayoutPreset(
        id="year_album_prefix",
        name="(Year) Album",
        description="Displays the release year before the album title.",
        structure="Artist / (Year) Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants("%albumartist%/" + YEAR_PAREN_PREFIX, YEAR_PAREN_PREFIX),
        preview=_tree([_S["artist"], f"({_S['year']}) {_S['album']}"], _FILE),
    ),

    LayoutPreset(
        id="alphabetical",
        name="Alphabetical Artist",
        description="Organises artists into alphabetical folders. Good for very large "
                     "libraries — avoids scrolling through hundreds of root-level folders.",
        structure="FirstLetter / Artist / Album / TrackNo - Title",
        category="Common",
        templates=_variants(
            FIRST_LETTER + "/%albumartist%/%album%",
            FIRST_LETTER + "/%album%",
        ),
        preview=_tree([_S["first_letter"], _S["artist"], _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="genre_artist_album",
        name="Genre → Artist → Album",
        description="Nests a folder named after the %genre% tag inside the genre bucket "
                     "— useful if you tag specific subgenres (e.g. 'Thrash Metal') "
                     "separately from the coarse bucket ('Metal').",
        structure="Genre / Artist / Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants(
            GENRE_TAG + "/%albumartist%/%album%",
            GENRE_TAG + "/%album%",
        ),
        preview=_tree([_S["genre"], _S["artist"], _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="genre_decade_artist",
        name="Genre → Decade → Artist",
        description="Ideal for large genre-tagged collections spanning many decades.",
        structure="Genre / Decade / Artist / Year - Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants(
            GENRE_TAG + "/" + DECADE + "/%albumartist%/" + YEAR_PREFIX + "%album%",
            GENRE_TAG + "/" + DECADE + "/" + YEAR_PREFIX + "%album%",
        ),
        preview=_tree(
            [_S["genre"], _S["decade"], _S["artist"], f"{_S['year']} - {_S['album']}"],
            _FILE,
        ),
    ),

    LayoutPreset(
        id="decade",
        name="Decade Grouping",
        description="Groups music globally by decade, independent of genre.",
        structure="Decade / Artist / Year - Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants(
            DECADE + "/%albumartist%/" + YEAR_PREFIX + "%album%",
            DECADE + "/" + YEAR_PREFIX + "%album%",
        ),
        preview=_tree([_S["decade"], _S["artist"], f"{_S['year']} - {_S['album']}"], _FILE),
    ),

    LayoutPreset(
        id="year_first",
        name="Year First",
        description="Organises the entire library by release year.",
        structure="Year / Artist / Album / TrackNo - Title",
        category="Time & Genre",
        templates=_variants(
            YEAR_FOLDER + "/%albumartist%/%album%",
            YEAR_FOLDER + "/%album%",
        ),
        preview=_tree([_S["year"], _S["artist"], _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="release_type",
        name="Release Type Library",
        description="Separates albums, EPs, singles, and live releases. Relies on a "
                     "%releasetype% tag (defaults to 'Albums' if untagged).",
        structure="Artist / Albums|EPs|Singles|Live / Album / TrackNo - Title",
        category="Special Purpose",
        templates=_variants(
            "%albumartist%/" + RELEASE_TYPE + "/%album%",
            "Compilations/%album%",
        ),
        preview=_tree([_S["artist"], "Albums", _S["album"]], _FILE),
    ),

    LayoutPreset(
        id="flat",
        name="Flat Directory",
        description="Stores every file directly within the genre folder. Relies entirely "
                     "on ID3 tags rather than folder structure for browsing.",
        structure="Artist - Year - Album - TrackNo - Title (no subfolders)",
        category="Special Purpose",
        templates={
            "E":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - %title%",
            "D":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - "
                  + DISC_SUBFOLDER.replace("/", " - ") + "%title%",
            "C":  "$num(%track%,2) - %album% - %artist% - %title%",
            "DC": "$num(%track%,2) - %album% - " + DISC_SUBFOLDER.replace("/", " - ")
                  + "%artist% - %title%",
            "S":  "$num(%track%,2) - %albumartist% - " + YEAR_PREFIX + "%album% - %artist% - %title%",
        },
        preview=_tree([], f"{_S['artist']} - {_S['year']} - {_S['album']} - {_FILE}"),
    ),

    LayoutPreset(
        id="metadata_filename",
        name="Metadata Filename",
        description="Includes most metadata directly in the filename, all in one folder.",
        structure="TrackNo - Title - Artist - Album (Year) (no subfolders)",
        category="Special Purpose",
        templates={
            "E":  "$num(%track%,2) - %title% - %artist% - " + YEAR_SUFFIX,
            "D":  "$num(%track%,2) - %title% - %artist% - " + YEAR_SUFFIX
                  + " - " + DISC_SUBFOLDER.replace("/", ""),
            "C":  "$num(%track%,2) - %title% - %artist% - " + YEAR_SUFFIX,
            "DC": "$num(%track%,2) - %title% - %artist% - " + YEAR_SUFFIX
                  + " - " + DISC_SUBFOLDER.replace("/", ""),
            "S":  "$num(%track%,2) - %title% - %artist% - " + YEAR_SUFFIX,
        },
        preview=_tree([], f"{_S['track']} - {_S['title']} - {_S['artist']} - "
                          f"{_S['album']} ({_S['year']}).{_S['ext']}"),
    ),

    LayoutPreset(
        id="compilation",
        name="Compilation Library",
        description="Routes every release (not only tagged compilations) under a single "
                     "'Compilations' root, credited per-track.",
        structure="Compilations / Album / TrackNo - Artist - Title",
        category="Special Purpose",
        templates=_variants("Compilations/%album%", "Compilations/%album%",
                             track_title=TRACK_ARTIST),
        preview=_tree(["Compilations", "Now That's What I Call Music 12"],
                      "01 Queen - Radio Ga Ga.flac"),
    ),

    LayoutPreset(
        id="soundtrack",
        name="Soundtrack Library",
        description="Stores soundtrack albums separately, grouped by composer/artist.",
        structure="Soundtracks / Title / Artist / TrackNo - Title",
        category="Special Purpose",
        templates=_variants(
            "Soundtracks/%album%/%artist%",
            "Soundtracks/%album%",
            track_title=TRACK_TITLE,
        ),
        preview=_tree(["Soundtracks", "Doom Eternal", "Mick Gordon"],
                      "01 At Doom's Gate.flac"),
    ),
]

# Public aliases — custom_layout.py builds presets on the fly using the
# same tree-rendering and template-variant helpers used above.
render_tree = _tree
build_variants = _variants

LAYOUTS: dict[str, LayoutPreset] = {p.id: p for p in _RAW_PRESETS}
PRESET_ORDER: list[str] = [p.id for p in _RAW_PRESETS]

CATEGORY_ORDER = ["Common", "Time & Genre", "Special Purpose"]

# Backwards-compatible aliases for the original four preset names, so
# existing `--layout <name>` invocations keep working.
_LEGACY_ALIASES = {
    "standard": "standard",
    "chronological": "artist_year_album",
    "alphabetical": "alphabetical",
    "flat": "flat",
}


def get(name: str) -> LayoutPreset:
    """Return a layout by id (or legacy alias), or raise KeyError."""
    resolved = _LEGACY_ALIASES.get(name, name)
    if resolved not in LAYOUTS:
        raise KeyError(
            f"Unknown layout {name!r}. Available: {', '.join(PRESET_ORDER)}"
        )
    return LAYOUTS[resolved]


def list_layouts() -> list[str]:
    """Ids in display order (not alphabetical — see PRESET_ORDER)."""
    return list(PRESET_ORDER)


def by_category() -> list[tuple[str, list[LayoutPreset]]]:
    """Presets grouped by category, in CATEGORY_ORDER."""
    groups: dict[str, list[LayoutPreset]] = {c: [] for c in CATEGORY_ORDER}
    for pid in PRESET_ORDER:
        preset = LAYOUTS[pid]
        groups.setdefault(preset.category, []).append(preset)
    return [(c, groups[c]) for c in CATEGORY_ORDER if groups.get(c)]


def build_format_string(layout: LayoutPreset, action: str, mount: str, genre: str) -> str:
    """Return the full /<mount>/<genre>/<...> format string for an action."""
    template = layout[action]
    if action in ("C", "DC"):
        return f"{mount}{genre}/{COMPILATION_MARKER}/{template}"
    if action == "S":
        return f"{mount}{genre}/{SPLIT_MARKER}/{template}"
    return f"{mount}{genre}/{template}"
