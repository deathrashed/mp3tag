# Scripts

Helper scripts for working with this repo. None are required for day-to-day Mp3tag use — they exist to make one-off setup tasks easier when you fork the repo or sync it to a new machine.

## Available scripts

### Top-level wrapper: `./configure`

For convenience, the repo root has a small bash wrapper called `configure` that `exec`s into `Scripts/retarget-paths.py`. It forwards all arguments unchanged:

```bash
# Interactive wizard from the repo root.
./configure

# Non-interactive — same flags, just shorter to type.
./configure --new /Volumes/MyExternal/Music/ --layout standard --yes
./configure --list-layouts
./configure --show-layout standard
```

The wrapper has no other logic — it locates the script relative to itself and runs it through `python3`. Calling `python3 Scripts/retarget-paths.py` directly is equivalent.

### `retarget-paths.py`

An **interactive wizard** that rewrites the Eksternal action groups in two independent ways:

1. **Mount retargeting** — swap the bundled `/Volumes/Eksternal/Audio/` (or any custom mount) for your own save destination.
2. **Layout application** — pick a folder-structure preset and rewrite the post-genre portion of every format string in one pass.

The same path string lives in three places in the repo and the script rewrites all of them:

- Individual `*.mta` action scripts in `Actions/Eksternal/...`
- Per-category JSON action groups (`Actions/Eksternal/Eksternal.json`, …)
- The master importable bundle `Actions/Action Groups.json`

Both unescaped and JSON-escaped (`\/`) forms are handled.

#### Interactive wizard

The recommended way to use the script — just run it with no arguments:

```bash
python3 Scripts/retarget-paths.py
# or, from the repo root:
./configure
```

The wizard is designed to feel like a polished installer. It walks through **4 steps**, each with a progress indicator and sensible defaults so you can press <kbd>Enter</kbd> to accept:

1. **Where should Mp3tag save your files?** — Which mount path to replace, and your new save destination. The wizard auto-detects mounted volumes on macOS and presents them in visually separated groups (last used / recommended / external drives).
2. **How should your files be organised?** — A **card-based layout browser** displays every preset as a scannable card with name, folder structure, short description, and an ASCII folder-tree preview. Type the card number, the preset id (e.g. `standard`), `0` to build a custom layout, or `–` to keep the current layout.
3. **Which files should be updated?** — Both `.mta` scripts and JSON action groups (recommended), or JSON only.
4. **Where should the updated files be written?** — In-place, to a separate output folder, or to stdout.

Before asking for confirmation, the wizard **pre-scans the repository** and displays a rich summary:

```
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Ready to apply
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Mount path          /Volumes/Eksternal/Audio/  →  /Volumes/MyExternal/Music/
  Layout              Standard Hierarchy
  Genre folders       No change
  Files updated       .mta + JSON files
  Output              In-place

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Estimated work
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Action scripts      24 .mta files
  JSON bundles        6 .json files
  Total replacements  217
```

If stdout is a TTY, the wizard uses ANSI colour and box-drawing characters. Pass `--no-color` to disable, or set `NO_COLOR=1` in the environment. The wizard auto-skips interactive mode if stdin/stdout aren't a TTY — use the CLI flags in that case.

At any prompt, type `?` for inline help, `b` to go back one step, or `q` to quit.

#### Custom layout builder

Choosing `0` at the layout browser enters a **guided sub-wizard** (steps A–F) that builds a custom folder hierarchy and filename format from scratch. A live preview updates after each choice:

| Step | Question |
|---|---|
| A | Group artists into A–Z folders? |
| B | Add a folder for the specific genre tag? |
| C | Group by decade? |
| D | How should the release year appear? |
| E | Separate multi-disc albums into Disc N/ folders? |
| F | Track filename format |

After step F you name the layout and it behaves identically to a built-in preset throughout the rest of the wizard.

#### Non-interactive (for scripting / CI)

```bash
# Mount retarget only (in-place).
python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --yes

# Apply a layout only (keep current mount).
python3 Scripts/retarget-paths.py --layout standard --yes

# Mount retarget + layout (in-place).
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout artist_year_album --yes

# Write a retargeted copy to a directory (originals untouched).
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout alphabetical \
    --out /tmp/retargeted/ --yes

# Print the retargeted master JSON to stdout — pipe or paste into Mp3tag.
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout flat \
    --stdout --yes > "Action Groups.retargeted.json"

# Skip the per-action .mta files; rewrite only the JSON action groups.
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout standard \
    --json-only --yes

# Tilde expansion.
python3 Scripts/retarget-paths.py --new '~/Music/Audio/' --yes

# List or inspect layouts without running.
python3 Scripts/retarget-paths.py --list-layouts
python3 Scripts/retarget-paths.py --show-layout standard

# Forget the saved configuration and exit.
python3 Scripts/retarget-paths.py --reset

# Force non-interactive mode (errors if neither --new nor --layout is given).
python3 Scripts/retarget-paths.py --no-interactive \
    --new /Volumes/MyExternal/Music/ \
    --layout standard --yes
```

#### Layout presets

Bundled in [`layouts.py`](layouts.py). Each preset defines 5 format-string templates (E, D, C, DC, S). Run `./configure --list-layouts` for the complete list, or `./configure --show-layout <id>` for detail on any one preset.

**Common presets**

| Preset id | Structure | Best for |
|---|---|---|
| `standard` | `Artist / Album / TrackNo. Title` | General-purpose libraries |
| `artist_year_album` | `Artist / Year – Album / TrackNo. Title` | Discography-order browsing |
| `alphabetical` | `FirstLetter / Artist / Album / TrackNo. Title` | Very large libraries |
| `flat` | `TrackNo - Artist - Year - Album - Title` (single folder) | Metadata-driven / player-tag libraries |

**All 15 presets across three categories**

| Category | Preset id | Structure |
|---|---|---|
| Common | `standard` | Artist / Album / Track |
| Common | `artist_year_album` | Artist / Year – Album / Track |
| Common | `alphabetical` | A–Z / Artist / Album / Track |
| Time & Genre | `artist_year_folder` | Artist / Year / Album / Track |
| Time & Genre | `album_year_suffix` | Artist / Album (Year) / Track |
| Time & Genre | `year_album_prefix` | Artist / (Year) Album / Track |
| Time & Genre | `genre_artist_album` | Genre / Artist / Album / Track |
| Time & Genre | `genre_decade_artist` | Genre / Decade / Artist / Year–Album / Track |
| Time & Genre | `decade` | Decade / Artist / Year–Album / Track |
| Time & Genre | `year_first` | Year / Artist / Album / Track |
| Special Purpose | `release_type` | Artist / Albums\|EPs\|Singles / Album / Track |
| Special Purpose | `flat` | Single-folder flat filenames |
| Special Purpose | `metadata_filename` | Single-folder, all metadata in filename |
| Special Purpose | `compilation` | Compilations / Album / Artist – Track |
| Special Purpose | `soundtrack` | Soundtracks / Title / Artist / Track |

The action types are:

| Type | File pattern | Folder marker | Track filename |
|---|---|---|---|
| `E` | `E - <Genre>.mta` | — | `Track# - Title` |
| `D` | `D - <Genre>.mta` | (adds `Disc N/`) | `Track# - Title` |
| `C` | `C - <Genre> - Compilation.mta` | `-Compilations-` | `Track# - Artist - Title` |
| `DC` | `DC - <Genre> Compilation.mta` | `-Compilations-` (+ `Disc N/`) | `Track# - Artist - Title` |
| `S` | `S - <Genre> - Split.mta` | `-Splits-` | `Track# - Artist - Title` |

#### Output modes

| Mode | Originals touched? | Use when |
|---|---|---|
| **In-place** (default) | yes | You've forked the repo and want the upstream files to match your local library. |
| **`--out DIR`** | no — copies retargeted files into `DIR` | You want a "ready to import" bundle without touching the source repo. |
| **`--stdout`** | no — writes the retargeted `Actions/Action Groups.json` to stdout | You want to pipe or paste the importable bundle straight into Mp3tag. |

#### UX features

| Feature | Description |
|---|---|
| **Card-based layout browser** | Each preset shown as a visual card: name, structure, description, ASCII folder-tree preview |
| **Progress indicator** | `[████████░░░░░░░░░░░░] 50%` on every step header |
| **Pre-scan summary** | File counts and total replacement count shown before confirmation |
| **Custom layout wizard** | Steps A–F with live preview after every choice |
| **Library picker** | Auto-detects common paths and external volumes, grouped with notes |
| **Option blocks** | Each choice displayed as a short block with description and badge |
| **Configuration save/restore** | Saves to `configure.json`; offered on next run |
| **Validation** | Checks paths are absolute and reachable before writing |
| **Back / Help / Quit** | Type `b`, `?`, or `q` at any prompt |

#### What it touches

The script scans every `*.mta` and `*.json` under `Actions/` and `Sources/`. The bundled templates contain path occurrences across 30 files (all under `Actions/Eksternal/`, `Actions/`, and `Sources/Mp3tagSettings/`). The `Format/`, `Genre/`, and `Regex/` action groups are tag-only and are never modified.

#### After running

- **In-place**: re-import `Actions/Action Groups.json` into Mp3tag (or refresh the already-imported groups) so the new paths take effect. Commit the rewritten files if you forked the repo.
- **`--out DIR`**: import `<DIR>/Actions/Action Groups.json` into Mp3tag.
- **`--stdout`**: paste the output into Mp3tag via **Actions → File → Import Action Groups…**, or pipe it to a file with `> "Action Groups.retargeted.json"` and import the resulting file.

#### Configuration persistence

The wizard automatically saves your choices to `configure.json` in the repo root after a successful run. On the next run it offers to reuse them, skipping directly to the output-mode step.

To forget the saved configuration:

```bash
./configure --reset
```

#### Exit codes

| Code | Meaning |
|---|---|
| `0` | Success (or nothing to do) |
| `1` | User cancelled at a prompt, or no files matched |
| `2` | Invalid arguments (e.g. neither `--new` nor `--layout` in non-interactive mode, or `--out` and `--stdout` both given) |
| `130` | Aborted with Ctrl-C |

---

### `layouts.py`

Defines the 15 bundled layout presets. Each preset is a `LayoutPreset` dataclass with 5 format-string templates (`E`, `D`, `C`, `DC`, `S`) and a pre-built ASCII preview.

To add a new preset, append a `LayoutPreset(…)` entry to `_RAW_PRESETS` in this file — nothing else needs to change. The format strings use the standard [Mp3tag scripting syntax](https://docs.mp3tag.de/scripting/functions/). Useful building blocks:

- `FIRST_LETTER` — strips a leading "The " from `%albumartist%` and returns the first character.
- `YEAR_PREFIX` — `Year - ` if `%year%` is set, else empty.
- `DISC_SUBFOLDER` — `Disc N/` if `%discnumber%` is set, else empty.
- `TRACK_TITLE` — `Track# - Title`.
- `TRACK_ARTIST` — `Track# - Artist - Title` (for compilations and splits).

The action-type subfolders (`-Compilations-`, `-Splits-`) are hard-coded in `build_format_string()` and are not part of the layout templates.

---

## Option B: edit `.mta` files manually

The bundled `.mta` files are plain text and easy to edit by hand. The path string lives on the `1=...` line under `F=_FILENAME`. Open the file in any text editor and change that one line; the format string is standard [Mp3tag scripting](https://docs.mp3tag.de/scripting/functions/).

For example, to make the `E - Hip-Hop.mta` action save to `<mount>/Hip-Hop/By Year/<Year> - <Album>/<Track#>. <Title>`:

```
1=/Volumes/MyExternal/Music/Hip-Hop/By Year/$if(%year%,$left(%year%,4) - ,)%album%/$num(%track%,2). %title%
```

Repeat for any other `.mta` file you want to change. When you're done, update the matching entry in the relevant JSON file — `Actions/Eksternal/Eksternal.json`, `Actions/Eksternal/Disc Numbers/Disc Numbers.json`, etc. — so the master `Action Groups.json` import bundle stays in sync. The JSON `format` value is the same string, but with `/` escaped as `\/`.
