# Actions

This folder holds every Mp3tag action group used by the library. Actions are organised into four top-level categories — one per workflow stage — each in its own subfolder with its own `README.md`, master `<Category>.json` file, and per-action `.mta` scripts.

## Files at this level

| File | What it is |
| --- | --- |
| `Action Groups.json` | The original master file imported into Mp3tag. It contains **all** action groups (Eksternal, Format, Genre, plus the top-level `F -` actions) in a single top-level array, in the exact shape Mp3tag expects. |
| `Main Actions.json` | A flat collection of the most-used `F -` formatting actions (Year, Artist to Album Artist, Fix Feat, Strip Remaster, Style to Genre, Trim Whitespace), kept at the top level for quick access. Mirrors `../Categories/Main.json`. |
| `MTA Guide.md` | Reference notes on the `.mta` file format. |

## Categories

### `Eksternal/`

Save actions for the external library at `/Volumes/Eksternal/Audio/`. Writes `_FILENAME` so the selected files land in the right genre folder and exports the embedded front cover to `cover.jpg`.

| Subfolder | What it does |
| --- | --- |
| `Eksternal/` (root) | Top-level `E - <Genre>` save actions for standard albums (no disc subfolders). |
| `Eksternal/Disc Numbers/` | `D - <Genre>` actions that add an optional `Disc N/` subfolder for multi-disc releases. |
| `Eksternal/Compilation/` | `C - <Genre> - Compilation` actions for compilations, stored under a `-Compilations-` root. |
| `Eksternal/Splits/` | `S - <Genre> - Split` actions for split releases, stored under a `-Splits-` root. |

### `Format/`

Tag-formatting actions. These run on the selected files to clean up, normalize, and reorganize tag values before saving. They do not move files or change filenames.

| Subfolder | What it does |
| --- | --- |
| `Format/` (root) | Curated top-level `F -` actions: Fix, Combo, Combo-Accents, Standard, Move Feat to Title, Strip Remaster, Style to Genre, Year, Mixed Case, Case Conversion, Artist to Album Artist. |
| `Format/Additional Format/` | Extended library of 25 one-off formatting actions (BPM, Date, Track, Disc, Compilation tag, Genre cleanup, Remove Brackets, Remove Extra Info, URL Clean, Title Case Advanced, Remove Duplicates, Feat Standardize, etc.). |

### `Genre/`

One-click `GENRE` tag setters. Each action rewrites the `GENRE` field on the selected files to a single, controlled value so the library stays consistent.

| Subfolder | What it does |
| --- | --- |
| `Genre/` (root) | Top-level `G -` genre presets: Black Metal, Blackened Death Metal, Crossover Thrash, Death Metal, Death Thrash, Hardcore, Heavy Metal, Hip-Hop, Thrash Metal. |
| `Genre/Additional Genres/` | Extended list of 60+ genre presets covering the rest of the library (Alternative, Atmospheric, Avantgarde, Beatdown, Brutal Death Metal, Crossover, Death, Deathgrind, Djent, Doom, Experimental, Folk, Funeral Doom, Grindcore, Groove Metal, Grunge, Hard Rock, Hardcore Punk, Hip-Hop; Trap, Horrorcore, Indie Rock, Industrial, Melodic Death Metal, Metal, Metallic Hardcore, New Wave, Nu Metal, Power Metal, Progressive, Psytance, Punk, Slamming Brutal Death Metal, Sludge Metal, Speed Metal, Stoner Metal, Symphonic Metal, Technical, etc.). |

### `Regex/`

Regex-driven text normalization and cleanup actions. Each action is a sequence of `replace` / `regexp` / `caseconv` steps that fix common tagging issues across `_TAG` (every tag), `_ALL` (every field), or specific fields like `TITLE`, `ARTIST`, `ALBUM`.

| Subfolder | What it does |
| --- | --- |
| `Regex/` (root) | Top-level `R -` regex actions: English Naming, Smart Title Case, Spacing Proper, Strip Accents, Trim Extra Space, Upper Case Feats. |
| `Regex/Additional Regex/` | Extended regex library: Clean Whitespace, Fix Common Typos, Fix Abbreviations, Fix Contractions, Fix Roman Numerals, Normalize Separators, Remove Parentheses, Remove Square Brackets, Remove Trailing Info, Add Apostrophes, plus the accent/case rules from the top level. |

## File layout inside each subfolder

Every category subfolder follows the same convention:

- `README.md` — what each action in that folder does.
- `<Category>.json` — the full action group as a single Mp3tag-compatible JSON array, in the same shape used by `Action Groups.json`.
- `*.mta` — individual Mp3tag action scripts. Each `.mta` is one importable action.

## Why the `S -` / `F -` / `D -` / `E -` prefixes?

When you assign a custom macOS keyboard shortcut via **System Settings → Keyboard → Keyboard Shortcuts → App Shortcuts**, the shortcut is matched to a menu item by its exact title — the first character of the title is what macOS uses as the trigger key. If six action groups all start with the same word (e.g. “Save Album”), they collide and the system shortcut is ambiguous.

The single-letter prefix (S - Search, F - Fix, D - Disc Number, E - Export, etc.) gives every action group a unique first letter, so you can assign a clean, distinct macOS shortcut to each one without collisions. The letter is also the mnemonic Mp3tag itself shows in its Actions menu accelerator, so the keyboard hint matches what you see in the menu bar.

In short: the prefixes exist so both macOS and Mp3tag can give every action a unique, predictable keyboard shortcut that matches the menubar text exactly.

## Prefix glossary

| Prefix | Meaning |
| --- | --- |
| `E -` | Eksternal save (standard album, no disc subfolders) |
| `D -` | Disc Number save (with `Disc N/` subfolders) |
| `C -` | Compilation save (under `-Compilations-`) |
| `S -` | Split save (under `-Splits-`) |
| `F -` | Format / Fix (tag normalization) |
| `G -` | Genre preset |
| `R -` | Regex (text-pattern cleanup) |
| `DC -` | Disc + Compilation (compilation with disc subfolders) |

## Personal file paths

The `Eksternal/` actions hard-code the maintainer's library mount (`/Volumes/Eksternal/Audio/<Genre>/...`) into every `1=...` line. **You will need to retarget these paths before running them on your own machine.** The `Format/`, `Genre/`, and `Regex/` actions are tag-only and don't have this issue — only `Eksternal/` does.

A helper script at the repo root rewrites every occurrence in one pass:

```bash
# Dry run — show what would change, write nothing.
python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --dry-run

# Apply.
python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --yes

# Tilde expansion is supported.
python3 Scripts/retarget-paths.py --new '~/Music/Audio/' --yes
```

See `Scripts/retarget-paths.py --help` for all options (custom `--old`, optional genre-rename, etc.). After the script runs, re-import `Actions/Action Groups.json` into Mp3tag (or refresh the already-imported groups) so the new paths take effect.
