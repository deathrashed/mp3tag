"""
custom_layout.py — interactive custom layout builder
=======================================================

Walks the user through building a folder hierarchy and filename format
in a multi-step guided wizard.  Each sub-step shows a live preview that
updates immediately after every choice — the user sees the result of
each decision before moving on to the next.

Returns a `layouts.LayoutPreset` built from their choices — same shape
as every bundled preset, so the rest of the wizard (preview, summary,
rewrite engine) doesn't need to know it's custom.
"""

from __future__ import annotations

import ui
from ui import (
    SAMPLE, Style, ask, confirm, dim, key, select, subhead, success, val,
    wrap_lines,
)
from layouts import (
    DECADE,
    DISC_SUBFOLDER,
    FIRST_LETTER,
    GENRE_TAG,
    LayoutPreset,
    TRACK_ARTIST,
    TRACK_TITLE,
    YEAR_FOLDER,
    YEAR_PAREN_PREFIX,
    YEAR_PREFIX,
    YEAR_SUFFIX,
    build_variants as _variants,
    render_tree as _tree,
)

_S = SAMPLE

# ─────────────────────────────────────────────────────────────────────
# Lookup tables
# ─────────────────────────────────────────────────────────────────────

YEAR_STYLES = [
    ("prefix",       "Year – Album",           YEAR_PREFIX + "%album%",   f"{_S['year']} - {_S['album']}"),
    ("suffix",       "Album (Year)",            YEAR_SUFFIX,               f"{_S['album']} ({_S['year']})"),
    ("paren_prefix", "(Year) Album",            YEAR_PAREN_PREFIX,         f"({_S['year']}) {_S['album']}"),
    ("folder",       "Separate Year/ folder",   None,                      None),
]

SEPARATORS = {
    "Dash  (02 - Aces High)":       " - ",
    "Dot   (02. Aces High)":        ". ",
    "Space (02 Aces High)":         " ",
    "Underscore (02_Aces_High)":    "_",
}

FILENAME_FIELDS = {
    "Track Number": "$num(%track%,2)",
    "Artist":       "%artist%",
    "Album":        "%album%",
    "Title":        "%title%",
    "Year":         "$left(%year%,4)",
}


# ─────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────

def build_custom_layout() -> LayoutPreset:
    """Run the interactive builder.  Raises ui.WizardBack / ui.WizardQuit."""
    _header()

    folders:       list[str] = []   # Mp3tag folder fragments (artist path)
    folders_c:     list[str] = []   # same, for the compilation variant
    label_folders: list[str] = []   # human-readable sample values, for the preview tree

    # ── Step A: First-letter grouping ─────────────────────────────────
    _substep("A", "Alphabetical grouping",
             "Add a top-level A–Z folder (e.g. 'I/') before the artist folder. "
             "Useful for very large libraries.")
    if confirm("Group artists into A–Z folders?", default_no=True):
        folders.append(FIRST_LETTER)
        label_folders.append(_S["first_letter"])
    _inline_preview(label_folders, _S["album"], _default_filename())
    print()

    # ── Step B: Genre sub-folder ──────────────────────────────────────
    _substep("B", "Genre sub-folder",
             "Nest a folder named after the %genre% tag value "
             "(e.g. 'Thrash Metal') inside the existing genre bucket.")
    if confirm("Add a folder for the specific genre tag?", default_no=True):
        folders.append(GENRE_TAG)
        folders_c.append(GENRE_TAG)
        label_folders.append(_S["genre"])
    _inline_preview(label_folders, _S["album"], _default_filename())
    print()

    # ── Step C: Decade folder ─────────────────────────────────────────
    _substep("C", "Decade folder",
             "Add a decade folder (e.g. '1980s/') above the artist folder.")
    if confirm("Group by decade?", default_no=True):
        folders.append(DECADE)
        folders_c.append(DECADE)
        label_folders.append(_S["decade"])
    _inline_preview(label_folders, _S["album"], _default_filename())
    print()

    # Artist folder is always present.
    folders.append("%albumartist%")
    label_folders.append(_S["artist"])

    # ── Step D: Year handling ─────────────────────────────────────────
    _substep("D", "Year placement",
             "Choose how the release year appears in the album folder name.")
    year_labels = [s[1] for s in YEAR_STYLES] + ["No year in folder names"]
    year_idx = select(year_labels, default_index=len(YEAR_STYLES))

    album_folder = "%album%"
    album_label  = _S["album"]

    if year_idx < len(YEAR_STYLES):
        style_id, _, fragment, sample = YEAR_STYLES[year_idx]
        if style_id == "folder":
            folders.append(YEAR_FOLDER)
            folders_c.append(YEAR_FOLDER)
            label_folders.append(_S["year"])
        else:
            album_folder = fragment
            album_label  = sample

    folders.append(album_folder)
    folders_c.append(album_folder)
    label_folders.append(album_label)
    _inline_preview(label_folders, album_label, _default_filename())
    print()

    folder_e = "/".join(folders)
    folder_c = "/".join(folders_c) if folders_c else "%album%"

    # ── Step E: Disc sub-folders ──────────────────────────────────────
    _substep("E", "Multi-disc albums",
             "Add a 'Disc 1/', 'Disc 2/' sub-folder when a release "
             "has more than one disc.  Recommended.")
    include_disc = confirm("Separate multi-disc albums into Disc N/ folders?",
                           default_no=False)
    _inline_preview(label_folders, album_label,
                    f"Disc 1/{_default_filename()}" if include_disc else _default_filename())
    print()

    # ── Step F: Filename format ────────────────────────────────────────
    _substep("F", "Track filename format",
             "Choose how each individual track file is named inside the album folder.")
    fn_options = [
        f"TrackNo. Title        e.g. {dim(_S['track'])}. {dim(_S['title'])}.{dim(_S['ext'])}",
        f"TrackNo. Artist – Title  e.g. {dim(_S['track'])}. {dim(_S['artist'])} – {dim(_S['title'])}.{dim(_S['ext'])}",
        "Custom  (choose fields and separator)",
    ]
    fn_idx = select(fn_options, default_index=0)

    if fn_idx == 0:
        track_title    = TRACK_TITLE
        track_artist   = TRACK_ARTIST
        filename_label = f"{_S['track']}. {_S['title']}.{_S['ext']}"
    elif fn_idx == 1:
        track_title    = TRACK_ARTIST
        track_artist   = TRACK_ARTIST
        filename_label = f"{_S['track']}. {_S['artist']} - {_S['title']}.{_S['ext']}"
    else:
        track_title, track_artist, filename_label = _build_custom_filename()

    _inline_preview(label_folders, album_label, filename_label)
    print()

    templates = _variants(
        folder_e, folder_c,
        track_title=track_title,
        track_artist=track_artist,
        disc=(DISC_SUBFOLDER if include_disc else ""),
    )

    structure = " / ".join(label_folders) + " / TrackNo - Title"
    preview   = _tree(label_folders, filename_label)

    # ── Final: name the layout ────────────────────────────────────────
    print(f"  {subhead('Name your layout')}")
    print(f"  {dim('Give this configuration a short name for the summary screen.')}")
    print()
    name = ask("Layout name", "My Layout")

    return LayoutPreset(
        id="custom",
        name=name,
        description="A custom layout configured in the setup wizard.",
        structure=structure,
        category="Custom",
        templates=templates,
        preview=preview,
    )


# ─────────────────────────────────────────────────────────────────────
# Custom filename sub-wizard
# ─────────────────────────────────────────────────────────────────────

def _build_custom_filename() -> tuple[str, str, str]:
    """Ask for filename components + separator.

    Returns (track_title_template, track_artist_template, display_label).
    """
    print()
    print(f"  {subhead('Choose filename fields')}")
    print(f"  {dim('Enter the numbers of the fields you want, separated by commas.')}")
    print()
    names = list(FILENAME_FIELDS.keys())
    label_map = {
        "Track Number": _S["track"],
        "Artist":       _S["artist"],
        "Album":        _S["album"],
        "Title":        _S["title"],
        "Year":         _S["year"],
    }
    for i, n in enumerate(names, 1):
        print(f"    {key(str(i) + '.')}  {n}  {dim(f'e.g. {label_map[n]}')}")
    print()

    while True:
        raw = ask("Fields (e.g. 1,4 for Track + Title)", "1,4")
        try:
            picks = [names[int(x.strip()) - 1] for x in raw.split(",")
                     if x.strip()]
        except (ValueError, IndexError):
            print(f"  {dim('!')} Enter comma-separated numbers from the list above.")
            continue
        if picks:
            break
        print(f"  {dim('!')} Pick at least one field.")

    print()
    sep_names = list(SEPARATORS.keys())
    idx = select(sep_names, title="Separator between fields", default_index=0)
    sep = list(SEPARATORS.values())[idx]

    template = sep.join(FILENAME_FIELDS[p] for p in picks)
    label    = sep.join(label_map[p] for p in picks) + f".{_S['ext']}"

    # Use the same template for both variants — user chose what appears.
    return template, template, label


# ─────────────────────────────────────────────────────────────────────
# Internal rendering helpers
# ─────────────────────────────────────────────────────────────────────

def _header() -> None:
    print(f"  {ui.heading('Custom Layout Builder')}")
    print()
    print(f"  {ui.dim('Build a folder hierarchy and filename format step by step.')}")
    print(f"  {ui.dim('A preview updates after every choice.')}")
    print()


def _substep(letter: str, title: str, description: str) -> None:
    print(f"  {ui.dim('──')}  {ui.key(letter)}  {ui.subhead(title)}")
    print()
    for line in wrap_lines(description, 60):
        print(f"       {ui.dim(line)}")
    print()


def _default_filename() -> str:
    return f"{_S['track']}. {_S['title']}.{_S['ext']}"


def _inline_preview(folder_labels: list[str], album_label: str,
                    filename: str) -> None:
    """Print a compact live preview after each sub-step."""
    # Always show from the artist level so the preview is readable even at
    # the start when only a few levels have been chosen.
    tree = _tree(folder_labels, filename)
    print(f"  {ui.dim('─' * 48)}")
    print(f"  {ui.subhead('Preview')}")
    print()
    for line in tree.splitlines():
        print(f"  {ui.dim(line)}")
    print(f"  {ui.dim('─' * 48)}")
