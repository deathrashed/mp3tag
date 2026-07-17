# Format

Tag-formatting actions. These run on the selected files to clean up, normalize, and reorganize tag values before saving. They do not move files or change filenames.

## Top-level actions

| File | What it does |
| --- | --- |
| `F - Artist to Album Artist.mta` | Copies `ARTIST` into `ALBUMARTIST` for save actions that rely on album artist paths. |
| `F - Case Conversion.mta` | Applies case conversion to selected tags. |
| `F - Combo - Accents.mta` | Runs the broad cleanup pipeline: case normalization, text cleanup, accent stripping, year cleanup, and genre deduping. |
| `F - Combo.mta` | Runs the standard cleanup combo: case normalization, spacing cleanup, year cleanup, replacements, and genre deduping. |
| `F - Fix.mta` | Runs the lighter fix pipeline for common cleanup issues like punctuation, year cleanup, genre deduping, and case normalization. |
| `F - Mixed Case.mta` | Applies mixed-case conversion to selected tags. |
| `F - Move Feat to Title.mta` | Moves `feat.` / `ft.` / `featuring` guest-artist credits out of `ARTIST` and into `TITLE` as `(feat. ...)`. |
| `F - Standard.mta` | Applies the base text cleanup rules used before more opinionated formatting passes. |
| `F - Strip Remaster.mta` | Removes remaster/version clutter from `TITLE` and `ALBUM` (e.g. `(Remastered 2011)`), then tidies whitespace. |
| `F - Style to Genre.mta` | Copies `STYLE` into `GENRE` and normalizes the genre field casing. |
| `F - Year.mta` | Extracts the four-digit year from `YEAR` or a `DATE`-style value. |

## Subfolders

| Folder | What it does |
| --- | --- |
| `Additional Format/` | Extended library of one-off formatting actions (BPM, Date, Track, Disc, Compilation tag, Genre cleanup, Remove Brackets, Remove Extra Info, URL Clean, Title Case Advanced, Remove Duplicates, etc.). See `Additional Format/Additional Format.json` for the full list. |

## Files

- `Format.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each top-level action.
