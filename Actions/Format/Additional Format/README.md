# Additional Format

Extended library of one-off formatting actions. Each action is a short script that fixes or reformats a specific tag pattern. They do not move files or change filenames.

## Actions

| File | What it does |
| --- | --- |
| `F - Album Artist from Artist.mta` | Builds `ALBUMARTIST` from `ARTIST`, then trims/normalizes artist tag values across the selected files. |
| `F - Artist Clean.mta` | Cleans up the `ARTIST` field: collapses whitespace, fixes common separators, and normalizes casing. |
| `F - Artist to Album Artist.mta` | Copies `ARTIST` into `ALBUMARTIST` for save actions that rely on album artist paths. |
| `F - BPM Format.mta` | Reformats the `BPM` field (e.g. pads, normalizes fractional values, removes non-numeric junk). |
| `F - Case Conversion.mta` | Applies case conversion to selected tags. |
| `F - Clean Comments.mta` | Trims and normalizes the `COMMENT` field (collapses whitespace, strips redundant info). |
| `F - Combo - Accents.mta` | Broad cleanup pipeline: case normalization, text cleanup, accent stripping, year cleanup, and genre deduping. |
| `F - Combo.mta` | Standard cleanup combo: case normalization, spacing cleanup, year cleanup, replacements, and genre deduping. |
| `F - Compilation Tag.mta` | Sets the `COMPILATION` tag to `1` (or clears it, depending on direction). |
| `F - Date Format.mta` | Reformats the `DATE` / `YEAR` field into a consistent 4-digit year. |
| `F - Disc Number Format.mta` | Normalizes `DISCNUMBER` (pads, removes total-disc suffix, collapses ranges). |
| `F - Feat Standardize.mta` | Standardizes `feat.` / `ft.` / `featuring` mentions: moves guest artists from `ARTIST` to `TITLE` and lowercases `feat`. |
| `F - Fix.mta` | Lighter fix pipeline: punctuation, year cleanup, genre deduping, case normalization. |
| `F - Genre Clean.mta` | Normalizes separators in `GENRE` (`/` / `&` / `,` / `-` → `;`) then merges duplicates. |
| `F - Mixed Case.mta` | Applies mixed-case conversion to selected tags. |
| `F - Remove Brackets.mta` | Strips `(...)` and `[...]` content (and surrounding whitespace) from `TITLE`, `ARTIST`, `ALBUM`. |
| `F - Remove Compilation Tag.mta` | Clears the `COMPILATION` tag from the selected files. |
| `F - Remove Duplicates.mta` | Merges duplicate multi-value entries in `ARTIST`, `GENRE`, `COMMENT`, and `ALBUMARTIST`. |
| `F - Remove Extra Info.mta` | Strips trailing `(Live)`, `(Remix)`, `[...]`, `(feat. ...)` and similar clutter from `TITLE`. |
| `F - Standard.mta` | Base text cleanup rules used before more opinionated formatting passes. |
| `F - Style to Genre.mta` | Copies `STYLE` into `GENRE` and normalizes the genre field casing. |
| `F - Title Case Advanced.mta` | Smart title-casing with article handling (`a`, `the`, `of`, `and` lowercased unless first/last), preserves acronyms. |
| `F - Track Number Format.mta` | Pads and normalizes `TRACK` / `TRACKNUMBER` (e.g. `1/12` → `01`). |
| `F - URL Clean.mta` | Normalizes URLs in `WWW` / `COMMENT` (strips tracking params, lowercases host, removes trailing slashes). |
| `F - Year.mta` | Extracts the four-digit year from `YEAR` or a `DATE`-style value. |

## Files

- `Additional Format.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each action.
