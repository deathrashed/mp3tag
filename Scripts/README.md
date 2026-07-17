# Scripts

Helper scripts for working with this repo. None of them are required for day-to-day Mp3tag use — they exist to make one-off setup tasks easier when you fork the repo or sync it to a new machine.

## Available scripts

### Top-level wrapper: `./configure`

For convenience, the repo root has a small bash wrapper called `configure` that `exec`s into `Scripts/retarget-paths.py`. It forwards all arguments unchanged, so anything you'd do with the full path works the same way:

```bash
# Interactive wizard from the repo root.
./configure

# Non-interactive — same flags, just shorter to type.
./configure --new /Volumes/MyExternal/Music/ --layout standard --yes
./configure --list-layouts
./configure --show-layout chronological
```

The wrapper has no other logic — it just locates the script relative to itself and runs it through `python3`. If you prefer, you can still call `python3 Scripts/retarget-paths.py` directly; both forms are equivalent.

### `retarget-paths.py`

An **interactive wizard** that rewrites the Eksternal action groups in two independent ways:

1. **Mount retargeting** — swap the bundled `/Volumes/Eksternal/Audio/` (or any custom mount) for your own save destination.
2. **Layout application** — pick a folder-structure preset (`standard`, `chronological`, `alphabetical`, `flat`, etc.) and rewrite the post-genre portion of every format string in one pass.

The same path string lives in three places in the repo and the script rewrites all of them in one pass:

- Individual `*.mta` action scripts in `Actions/Eksternal/...`
- Per-category JSON action groups (`Actions/Eksternal/Eksternal.json`, …)
- The master importable bundle `Actions/Action Groups.json`)

Both unescaped and JSON-escaped (`\/`) forms are handled.

#### Interactive wizard

The recommended way to use the script — just run it with no arguments and answer the prompts:

```bash
python3 Scripts/retarget-paths.py
# or, from the repo root:
./configure
```

The wizard walks through **4 steps** in a logical top-down flow, each with sensible defaults so you can just press <kbd>Enter</kbd> to accept:

1. **Save Location** — the foundation of the retarget: which mount path to replace, and where Mp3tag should save files. Old defaults to the bundled `/Volumes/Eksternal/Audio/` (auto-detected if you've already retargeted once); new accepts any absolute path (e.g. `/Volumes/MyExternal/Music/`, `~/Music/`, `/Volumes/Backup/Audio/`). Tilde is expanded; the script warns (but doesn't abort) if the directory doesn't exist.
2. **Filename Structure** — builds on the save location: pick a layout preset (`standard`, `chronological`, `alphabetical`, `flat`) and optionally rename the genre subfolders from `/Audio/<Genre>/` to `/Music/<Genre>/`.
3. **File Scope** — which files should be rewritten: both the per-action `.mta` files and the JSON action groups (default), or just the JSONs (with `--json-only`). The JSONs are usually enough for bulk retargeting; the `.mta` files can always be regenerated from the JSON.
4. **Output Mode** — where the rewritten files go: in-place (rewrite the source files) / `--out DIR` (write a retargeted copy to a new directory, originals untouched) / `--stdout` (write the retargeted `Actions/Action Groups.json` to the terminal for piping).

After step 4 the script shows a **Review** panel summarising every change, then asks for a final confirmation. The actual file modifications only happen after you say yes.

If stdout is a TTY, the wizard uses ANSI colour and box-drawing characters to make the steps easy to follow (paths in yellow, prompts in green, errors in red, etc.). Pass `--no-color` to disable, or set `NO_COLOR=1` in the environment. The wizard auto-skips if stdin/stdout aren't a TTY — in that case use the CLI flags below.

#### Non-interactive (for scripting / CI)

```bash
# Mount retarget only (in-place).
python3 Scripts/retarget-paths.py --new /Volumes/MyExternal/Music/ --yes

# Apply a layout only (keep current mount).
python3 Scripts/retarget-paths.py --layout standard --yes

# Mount retarget + layout (in-place).
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout chronological --yes

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
# Useful for bulk retargeting when the .mta files would be regenerated
# from the JSON anyway.
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout standard \
    --json-only --yes

# JSON-only + --out: produces a clean "ready to import" bundle of just
# the JSON files (no per-action .mta noise).
python3 Scripts/retarget-paths.py \
    --new /Volumes/MyExternal/Music/ \
    --layout alphabetical \
    --out /tmp/retargeted/ \
    --json-only --yes

# Tilde expansion.
python3 Scripts/retarget-paths.py --new '~/Music/Audio/' --yes

# List or inspect layouts without running.
python3 Scripts/retarget-paths.py --list-layouts
python3 Scripts/retarget-paths.py --show-layout standard

# Force non-interactive mode (errors if neither --new nor --layout is given).
python3 Scripts/retarget-paths.py --no-interactive \
    --new /Volumes/MyExternal/Music/ \
    --layout standard --yes
```

#### Layout presets

Bundled in [`layouts.py`](layouts.py). Each preset defines 5 format-string templates (E, D, C, DC, S) — one per action type — that replace the post-genre portion of every save action.

| Preset | Structure (per genre) | Best for |
| --- | --- | --- |
| `standard`      | `Artist / Album / TrackNo - Title`            | General-purpose libraries. |
| `chronological` | `Artist / Year - Album / TrackNo - Title`     | Browsing an artist's discography chronologically. |
| `alphabetical`  | `FirstLetter / Artist / Album / TrackNo - Title` | Very large libraries where you want to limit the number of direct subfolders (e.g. `A-E`, `F-J`, …). |
| `flat`          | `TrackNo - Artist - Year - Album - Title` (one folder) | Metadata-driven libraries; rely on the media player for the ID3 tags. |

The other structures from the music-library literature (genre-rooted, classical composer, DJ-BPM/Key, format-separation, archival-by-acquisition-date) don't fit the bundled genre-split action model out of the box. Use a custom layout (edit `layouts.py`) or edit the `.mta` files directly — see [Option B: edit `.mta` files manually](#option-b-edit-mta-files-manually) below.

The action types are:

| Type | File pattern | Folder marker | Track filename |
| --- | --- | --- | --- |
| `E`  | `E - <Genre>.mta`               | —                                | `Track# - Title` |
| `D`  | `D - <Genre>.mta`               | — (adds `Disc N/`)                | `Track# - Title` |
| `C`  | `C - <Genre> - Compilation.mta` | `-Compilations-`                  | `Track# - Artist - Title` |
| `DC` | `DC - <Genre> Compilation.mta`  | `-Compilations-` (+ `Disc N/`)    | `Track# - Artist - Title` |
| `S`  | `S - <Genre> - Split.mta`       | `-Splits-`                        | `Track# - Artist - Title` |

#### Output modes

| Mode | Originals touched? | Use when |
| --- | --- | --- |
| **In-place** (default) | yes | You've forked the repo and want the upstream files to match your local library. |
| **`--out DIR`** | no — copies retargeted files into `DIR` | You want a "ready to import" bundle (e.g. for another machine, a backup profile, or a `tar czf` archive) without touching the source repo. |
| **`--stdout`** | no — writes the retargeted `Actions/Action Groups.json` to stdout | You want to pipe or paste the importable bundle straight into Mp3tag via the clipboard. |

#### What it touches

The script scans every `*.mta` and `*.json` under `Actions/` and `Sources/`. As of the latest scan, the bundled templates contain 79 path occurrences across 30 files (all under `Actions/Eksternal/`, `Actions/`, and `Sources/Mp3tagSettings/`). The `Format/`, `Genre/`, and `Regex/` action groups are tag-only and are never modified.

#### After running

- **In-place**: re-import `Actions/Action Groups.json` into Mp3tag (or refresh the already-imported groups) so the new paths take effect. Commit the rewritten files if you forked the repo.
- **`--out DIR`**: import `<DIR>/Actions/Action Groups.json` into Mp3tag. The `<DIR>` tree contains a complete retargeted copy of the matched files; you can `cp -R` it anywhere or `tar czf` it for transfer.
- **`--stdout`**: paste the output into Mp3tag via **Actions → File → Import Action Groups…**, or pipe it to a file with `> "Action Groups.retargeted.json"` and import the resulting file.

#### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success (or nothing to do) |
| `1` | User aborted at a prompt, or no files matched |
| `2` | Invalid arguments (e.g. neither `--new` nor `--layout` given in non-interactive mode, or `--out` and `--stdout` both given) |
| `130` | Aborted with Ctrl-C |

---

### `layouts.py`

Defines the four bundled layout presets (`standard`, `chronological`, `alphabetical`, `flat`). Each preset is a Python dict with 5 format-string templates (`E`, `D`, `C`, `DC`, `S`).

To add a custom layout, edit this file and add a new entry to the `LAYOUTS` dict. The format strings use the standard [Mp3tag scripting syntax](https://docs.mp3tag.de/scripting/functions/). Useful building blocks:

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

Repeat for any other `.mta` file you want to change. Use the same `1=...` pattern across all matching files so the actions stay consistent.

When you're done, edit (or create) a matching entry in the relevant JSON file — `Actions/Eksternal/Eksternal.json`, `Actions/Eksternal/Disc Numbers/Disc Numbers.json`, etc. — so the master `Action Groups.json` import bundle stays in sync. The JSON `format` value is the same string, but with `/` escaped as `\/` (e.g. `\/` instead of `/` in the path).
