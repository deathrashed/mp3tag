## Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
  - [Repository Structure](#repository-structure)
  - [What is Mp3tag?](#what-is-mp3tag)
  - [Getting Started](#getting-started)
- [Sources](#sources)
  - [Individual Tag Sources](#individual-tag-sources)
    - [iTunes+](#itunes)
    - [Metal Archives — Tag Sources](#metal-archives--tag-sources)
    - [Metallum Genres](#metallum-genres)
    - [Last.fm Genres](#lastfm-genres)
    - [MusicBrainz Expanded](#musicbrainz-expanded)
    - [Bandcamp](#bandcamp)
    - [Qobuz](#qobuz)
    - [Deezer](#deezer)
    - [Soundcloud](#soundcloud)
    - [Genius Lyrics](#genius-lyrics)
  - [Cover Art Sources](#cover-art-sources)
    - [iTunes Cover Art](#itunes-cover-art)
    - [Deezer Cover Art](#deezer-cover-art)
    - [Qobuz Cover Art](#qobuz-cover-art)
    - [Soundcloud Cover Art](#soundcloud-cover-art)
- [Actions](#actions)
  - [Prefix Guide](#prefix-guide)
  - [Bundled Actions](#bundled-actions)
  - [Importing Actions](#importing-actions)
  - [Export Actions](#export-actions)
  - [Adapting Templates](#adapting-templates)
- [Scripts](#scripts)
  - [Quick Start: `./configure`](#quick-start-configure)
  - [Interactive Wizard](#interactive-wizard)
  - [Layout Presets](#layout-presets)
  - [CLI Usage](#cli-usage)
  - [After Running](#after-running)
  - [Manual Editing](#manual-editing)
- [Settings](#settings)
  - [Settings System](#settings-system)
  - [File Naming Conventions](#file-naming-conventions)
  - [Creating & Editing Actions](#creating--editing-actions)
- [Guides](#guides)
  - [Creating Web Sources](#creating-web-sources)
  - [Mp3tag Scripting](#mp3tag-scripting)
- [FAQ](#faq)
- [Additional Resources](#additional-resources)
- [License](#license)

</div>

---

## Quick Start

Getting started with this repository involves two simple steps: copying the files into place and restarting Mp3tag. Here's the fastest way to get everything working:

1. **Copy the folders into place.** Copy this repo's `Sources/` and `Actions/` folders into Mp3tag's data directory (see the table in [Getting Started](#getting-started) for the exact path), **or** let Mp3tag show you exactly where:

   - **Actions** — In Mp3tag, open **Actions → Actions…** (`⌥6`) to open the *Action Groups* window. Click the **+** icon at the bottom-left of the sidebar to open its context menu, choose **Import…**, then select `Actions/Action Groups.json` from this repo (individual `.mta` files can be imported the same way).
   - **Sources** — Open the **Tag Sources** menu (the toolbar icon or right-click in the tag panel) and click **Open Tag Sources Folder** at the very bottom of the list. This reveals the exact folder Mp3tag reads sources from — copy everything from this repo's `Sources/` folder into it.

2. **Restart Mp3tag.** Sources appear under **Tag Sources**, actions under **Actions** (`⌥6`).

Prefer the terminal? Same result, no clicking required:

```bash
DATA_DIR=~/Library/Application\ Support/Mp3tag

cp -R Sources "$DATA_DIR"
cp -R Actions "$DATA_DIR"
```

> [!NOTE]
> **Copy, do not symlink.** Both the macOS sandbox (App Store version) and Mp3tag's file-access model reject symlinks. Use `cp -R` or the app's own **Import…** dialog instead.

**[&uarr; Back to Contents](#contents)**

---

## Overview

This section provides context about the repository, explains what Mp3tag is, and walks through the initial setup process. Understanding these fundamentals will help you make the most of the tag sources and actions provided here.

This repository contains personal configuration, tag sources, actions, and scripts for [Mp3tag](https://www.mp3tag.de/en/) on macOS. It is designed to be cloned directly into the Mp3tag application support directory so that sources and actions are available out of the box.

**What you get:**

- **9 tag sources** — Apple Music, Metal Archives, Last.fm, MusicBrainz, Bandcamp, Qobuz, Deezer, SoundCloud, and Genius Lyrics
- **4 cover art sources** — iTunes, Deezer, Qobuz, and SoundCloud album artwork
- **151 action scripts** — formatting, genre canonicalisation, regex cleanup, and library export
- **70+ genre presets** — one-click `GENRE` tag setters covering metal sub-genres, hip-hop, punk, electronic, and more
- **Interactive configure wizard** — retarget paths, pick folder layouts, and generate importable JSON bundles

### Repository Structure

The repository is organized into logical folders that separate concerns: sources, actions, scripts, and assets. Here's the complete directory tree:

```
.
├── Actions/                        # Action groups (.mta + .json)
│   ├── Action Groups.json          # Master importable bundle
│   ├── Main Actions.json           # Curated F - shortcuts
│   ├── MTA Guide.md                # .mta file-format reference
│   ├── README.md                   # Category guide + prefix docs
│   ├── Eksternal/                  # External library save actions
│   ├── Format/                     # Tag-formatting actions
│   ├── Genre/                      # Genre presets
│   └── Regex/                      # Regex-based cleanup
├── Sources/                        # Web sources (.src, .inc, .settings)
├── Assets/                         # Branding images and archived docs
│   ├── Icon/                       # Repository icons
│   └── Archive/                    # Legacy files
├── Scripts/                        # Python helpers
│   ├── layouts.py                  # Folder-structure presets
│   └── retarget-paths.py           # Bulk path/layout rewrite
├── configure                       # Top-level bash wrapper
└── README.md
```

Each subfolder under `Actions/` serves a specific purpose:

| Folder | What it is |
|---|---|
| `Eksternal/` | Save actions with per-genre folders. Includes `Disc Numbers/`, `Compilation/`, `Splits/` sub-folders. Each has a README. |
| `Format/` | Tag clean-up, normalisation, and value transformation. Tag-only — no file paths. |
| `Genre/` | One-click `GENRE` setters. 9 top-level + 60+ extended presets under `Additional Genres/`. |
| `Regex/` | Regex-driven cleanup actions. 6 top-level + 15 extended under `Additional Regex/`. |

---

### What is Mp3tag?

Mp3tag is a powerful and extensible metadata editor for audio files. It's available on Windows, macOS, and has limited functionality on Linux. This repository focuses on the macOS version. Mp3tag allows you to:

- **Batch edit tags** for multiple files simultaneously
- **Rename files** based on tag information or vice versa
- **Import tags** from online databases (MusicBrainz, Deezer, Qobuz, etc.)
- **Download cover art** automatically from various sources
- **Format and clean** tag values using actions and scripts
- **Support multiple formats**: MP3, MP4, FLAC, OGG, WMA, APE, and more

For more information, visit the [official Mp3tag website](https://www.mp3tag.de/en/) and [documentation](https://docs.mp3tag.de/).

---

### Getting Started

This section walks you through the complete installation process, from downloading Mp3tag to configuring the bundled actions for your own library. Follow these steps in order for the smoothest experience.

**Installation**

1. **Download** the latest version from the [official website](https://www.mp3tag.de/en/download.html)
2. **Install** following the macOS instructions
3. **Configure** the bundled actions for your library:

   ```bash
   ./configure
   ```

   This walks you through setting your mount path, file-naming layout, and output mode. See [Quick Start: `./configure`](#quick-start-configure) for details.

4. **Copy** the `Sources/` and `Actions/` folders into Mp3tag's data directory:

   | Install source | Data directory |
   |---|---|
   | **Website** ([mp3tag.de](https://www.mp3tag.de/en/download.html)) | `~/Library/Application Support/Mp3tag/` |
   | **App Store** | `~/Library/Containers/app.mp3tag.Mp3tag/Data/Library/Application Support/Mp3tag/` |

   ```bash
   # Pick the right DATA_DIR (see table above).
   DATA_DIR=~/Library/Application\ Support/Mp3tag

   cp -R Sources "$DATA_DIR"
   cp -R Actions "$DATA_DIR"
   cp configure "$DATA_DIR"
   ```

   Not sure which directory Mp3tag is actually using? Open the **Tag Sources** menu in the app and click **Open Tag Sources Folder** at the bottom — that's the live folder to copy `Sources/` into. The **Actions** window (`⌥6`) → **+** → **Import…** works the same way for `Actions/Action Groups.json` without needing to know the path at all.

5. **Restart** Mp3tag. Sources and actions appear in their respective menus automatically.

> [!CAUTION]
> Symlinks do not work. Both the macOS sandbox and Mp3tag's file-access model require files to be copied into the app's data directory.

**Basic usage**

Once everything is installed, here's how to use Mp3tag for common tasks:

1. **Load files** — `File > Add directory…` (`Cmd+D`) or drag and drop into Mp3tag
2. **Edit tags** — Select files, modify fields in the Tag Panel, changes apply immediately
3. **Save** — `Cmd+S` or click the save icon
4. **Import tags** — `Tag Sources` menu → choose a source → search and apply
5. **Rename files** — `Convert > Tag - Filename` (`Alt+Cmd+1`) with a format string like `%artist% - %title%`

**[&uarr; Back to Contents](#contents)**

---

## Sources

This section documents all the tag sources and cover art sources included in the repository. Tag sources fetch metadata from online databases and write it to your audio files, while cover art sources specifically retrieve album artwork. Each source is implemented as a `.src` file that Mp3tag can execute, often accompanied by `.inc` include files for shared parsing logic and `.settings` files for configuration options.

### Individual Tag Sources

These sources retrieve comprehensive metadata from various music databases and streaming services. They're designed to work together — you might use iTunes+ for mainstream releases, Metal Archives for metal-specific data, and MusicBrainz for the most complete information.

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/applemusic.svg" height="18" valign="middle" /> iTunes+

**Files:** `iTunes+#S - iTunes+.src` · `iTunes+#Settings….settings` · `iTunes API v2.inc` · `iTunes Artwork.inc`

Searches the Apple Music / iTunes Store catalog via the iTunes Search API. Returns comprehensive tag metadata including title, artist, album, composer, year, genre, track number, disc number, BPM, and cover art. Built on the v3.71 international script with a configurable settings panel.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Cover art size | `1200px` | Pixel size of the artwork fetched |
| Include tracks | `true` | List individual tracks in search results |
| Uncensored titles | `true` | Prefer clean/uncensored title strings |

**Search by:** Artist + Album (or fallback to folder names)

---

#### <img src="https://raw.githubusercontent.com/deathrashed/gupload/main/Uploads/Images/metallum-white.svg" height="18" valign="middle" /> Metal Archives — Tag Sources

**Files:** `Me&tal Archives#S - Search by Band.src` · `Me&tal Archives#S - Search by Band + Album.src` · `Me&tal Archives#S - Search by Album.src`

Three search modes for fetching release metadata from [metal-archives.com](https://www.metal-archives.com):

| Source | Search by | Use case |
|---|---|---|
| Search by Band | `%artist%` | Find all releases for an artist |
| Search by Band + Album | `%artist% %album%` | Most precise — recommended |
| Search by Album | `%album%` | When artist is ambiguous |

Returns: Title, Artist, Album, Year, Genre, Country, Label, Catalog Number, and track listing.

---

#### <img src="https://raw.githubusercontent.com/deathrashed/gupload/main/Uploads/Images/metallum-icon-white-ring.png" height="18" valign="middle" /> Metallum Genres

**Files:** `Metallum Genres#S - Metallum Genres.src` · `Metallum Genres#Settings….settings`

Standalone genre-only source querying Metal Archives directly. Includes a suite of genre normalisation replacements (e.g. `Death/Thrash Metal` → `Death/Thrash; Death Metal; Thrash Metal`) that expand hybrid genres into individual searchable tokens.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Keep era descriptions | `false` | Preserve brackets like `(early)`, `(mid-period)` |
| Deduplicate genres | `true` | Remove duplicate genre tokens |
| Genre separator | `; ` | Delimiter between multiple genres |
| Write dedicated tags | `true` | Fill `Metal Archives Country`, `Status`, `Formed`, etc. |
| Write band info to Comment | `true` | Append country, location, status, themes to `COMMENT` |

> [!TIP]
> Edit the `CUSTOM GENRE REPLACEMENTS` block inside the `.src` file to add custom genre mappings:
> ```
> replace "Original Text" "Replacement Text"
> ```

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/lastfm.svg" height="18" valign="middle" /> Last.fm Genres

**Files:** `Last.fm#S - Last.fm Genres.src` · `Last.fm#Settings….settings`

Fetches an artist's top tags from the Last.fm API and writes them as genre tags. Genre count and separator are configurable.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Genre limit | `1` | How many top tags to retrieve (1, 2, 3, 4, 5, or 10) |
| Genre separator | `; ` | Delimiter between multiple genres |

> Uses the Last.fm `artist.gettoptags` endpoint with a public embedded API key.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/musicbrainz.svg" height="18" valign="middle" /> MusicBrainz Expanded

**Files:** `MusicBrainz Expanded.inc` + 7 `.src` entry points · `MusicBrainz Expanded#Settings….settings`

Feature-rich MusicBrainz source with seven search entry points:

| Source | Search by |
|---|---|
| Search by Artist + Album | `%artist%` + `%album%` |
| Search by Artist + Album + Tracks | Artist, Album, and track count |
| Search by Artist + Album + Tracks + MediaType + Country | Full precision |
| Search by ASIN | Amazon ASIN |
| Search by Barcode | Barcode / EAN |
| Search by Catalog number | Catalog number |
| Search by MB AlbumID | MusicBrainz Release ID |

Returns: Artist, AlbumArtist, Album, Year, Genre, Label, Country, Media type, Catalog number, ISRC, track listing, and optionally MusicBrainz-specific tags.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Show MB media / tracks / recording metadata | `false` | Include extra MB-specific fields |
| Fill DISCNUMBER | `false` | Write disc number from MB data |
| Convert status and primary type | `true` | Normalise release type/status strings |
| Show MB nonstandard tags | `false` | Include `MUSICBRAINZ_*` ID fields |

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/bandcamp.svg" height="18" valign="middle" /> Bandcamp

**Files:** `Bandcamp#S - Bandcamp by &Album.src` · `Bandcamp#S - Bandcamp by &All.src` · `Bandcamp#S - Bandcamp by &Track.src` · `Bandcamp#S - Bandcamp by &URL.src` · `Bandcamp#ParserScriptAlbum.inc` · `Bandcamp#Settings….settings`

Fetches metadata directly from Bandcamp release pages.

| Source | Search by |
|---|---|
| By Album | Artist + Album name |
| By Track | Track title |
| By All | Broad search across Bandcamp |
| By URL | Paste a Bandcamp URL directly |

Returns: Title, Artist, AlbumArtist, Album, Year, Genre, Label, Track number, and cover art.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/qobuz.svg" height="18" valign="middle" /> Qobuz

**Files:** `Qobuz.inc` · `&Qobuz#S - Qobuz AU.src` · `&Qobuz#S - Qobuz US.src` · `&Qobuz#Settings….settings`

Full metadata source for Qobuz with regional entry points (AU and US) sharing a common parser.

Returns: Title, Artist, AlbumArtist, Album, Year, Genre, Label, Track number, Disc number, Composer, Lyricist, Credits, Publisher, ISRC, and high-resolution cover art.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/deezer.svg" height="18" valign="middle" /> Deezer

**Files:** `Deezer#S - Deezer by Album.src` · `Deezer#S - Deezer by Title.src`

| Source | Search by |
|---|---|
| By Album | Artist + Album |
| By Title | Track title |

Returns: Title, Artist, AlbumArtist, Album, Year, Genre, Track number, and cover art.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/soundcloud.svg" height="18" valign="middle" /> Soundcloud

**Files:** `Soundcloud.inc` · `Soundcloud#S - Soundcloud Search.src` · `Soundcloud Artwork.inc` · `Soundcloud#Settings….settings`

Searches SoundCloud for tracks and retrieves metadata.

Returns: Title, Artist, Year, Genre, Description, and cover art.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/genius.svg" height="18" valign="middle" /> Genius Lyrics

**Files:** `Genius#Lyrics.inc` · `Genius#S - Genius Lyrics.src` · `Genius#Settings….settings`

Fetches lyrics from [genius.com](https://genius.com) and writes them to the `UNSYNCEDLYRICS` tag field.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Line ending character | `CR (Mac)` | Line ending format for lyrics |
| Write UNSYNCEDLYRICS | `true` | Write to standard UNSYNCEDLYRICS field |

---

### Cover Art Sources

These sources specifically retrieve album artwork from various services. They're separate from the tag sources because cover art often requires different parsing logic and may come from different endpoints. Use these when you want to fetch artwork without importing other metadata.

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/applemusic.svg" height="18" valign="middle" /> iTunes Cover Art

**File:** `&Art#&iTunes.src` → `iTunes Artwork.inc`

Searches Apple Music for cover art. Always retrieves the original uncompressed source image at maximum available resolution. No settings required — hardcoded to highest quality.

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/deezer.svg" height="18" valign="middle" /> Deezer Cover Art

**File:** `&Art#&Deezer.src`

Searches Deezer for album artwork. Returns up to 1200×1200 px JPEG. Parses Deezer's embedded JSON state object.

**Search by:** Artist + Album

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/qobuz.svg" height="18" valign="middle" /> Qobuz Cover Art

**File:** `&Art#&Qobuz.src` → `Qobuz.inc`

Searches Qobuz for album artwork and extracts the best available image URL from the structured JSON response.

**Search by:** AlbumArtist + Album

---

#### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/soundcloud.svg" height="18" valign="middle" /> Soundcloud Cover Art

**File:** `&Art#&Soundcloud.src` → `Soundcloud Artwork.inc`

Fetches SoundCloud track or artist artwork by artist name and title, or by direct URL.

**[&uarr; Back to Contents](#contents)**

---

## Actions

This section documents all the action groups included in the repository. Actions are automated scripts that perform batch operations on your audio files — everything from formatting tag values to exporting files to specific folder structures. Each action is stored as a `.mta` file (Mp3tag Action format) and can be imported individually or as part of the bundled `Action Groups.json` file.

Each category is a subfolder under `Actions/` with a `README.md` explaining every action, a `<Category>.json` file, and per-action `<Prefix> - <Name>.mta` scripts. The master importable bundle `Actions/Action Groups.json` combines all groups in a single file.

Actions are organised by the first letter of the group name, which doubles as the keyboard accelerator shown in Mp3tag's **Actions** menu:

| Prefix | Category | Purpose |
|---|---|---|
| `F` | **Format** | Text formatting, value transformation, tag moves |
| `G` | **Genre** | Per-genre canonicalisation |
| `R` | **Regex** | Regex-based cleanup and normalisation |
| `D` | **Disc Numbers** | Filename templates with `Disc N/` subfolder |
| `E` | **Eksternal** | Export templates for the external library |

### Prefix Guide

When you assign a custom macOS keyboard shortcut via **System Settings → Keyboard → Keyboard Shortcuts → App Shortcuts**, the shortcut is matched to a menu item by its **exact** title — the first character is what macOS uses as the trigger key. If several action groups start with the same word (e.g. "Save Album"), they collide.

The single-letter prefix (`S - Search`, `F - Fix`, `D - Disc Number`, `E - Export`, etc.) gives every action group a **unique first letter**, so you can assign a clean, distinct macOS shortcut to each one without collisions.

### Bundled Actions

Here's the complete list of all 38 actions across the 5 groups, with their purposes explained:

| Action | Purpose |
|---|---|
| `F - Artist to Album Artist` | Copy `ARTIST` → `ALBUMARTIST` |
| `F - Case Conversion` | Convert to UPPER / lower / Title Case |
| `F - Combo` | Combined formatting pass for tags |
| `F - Combo - Accents` | Combo plus accent stripping |
| `F - Fix` | General tag fixes (whitespace, separators) |
| `F - Mixed Case` | Force Mixed Case for standard fields |
| `F - Move Feat to Title` | Move `feat.` artists from `ARTIST` into `TITLE` |
| `F - Standard` | Standard formatting pass over common fields |
| `F - Strip Remaster` | Remove remaster info from `TITLE`/`ALBUM` |
| `F - Style to Genre` | Promote `STYLE` into `GENRE` |
| `F - Year` | Normalise `YEAR` formatting |
| `G - Black Metal` | `Black Metal` |
| `G - Blackened Death Metal` | `Blackened Death Metal` |
| `G - Crossover Thrash` | `Crossover Thrash` |
| `G - Death Metal` | `Death Metal` |
| `G - Death Thrash` | `Death/Thrash Metal` |
| `G - Hardcore` | `Hardcore` |
| `G - Heavy Metal` | `Heavy Metal` |
| `G - Hip-Hop` | `Hip-Hop` |
| `G - Thrash Metal` | `Thrash Metal` |
| `R - Add Apostrophes` | Insert apostrophes in common contractions |
| `R - English Naming` | Standardise English-language naming conventions |
| `R - Smart Title Case` | Apply smarter Title Case to `TITLE`/`ALBUM` |
| `R - Spacing Proper` | Fix spacing around punctuation |
| `R - Strip Accents` | Strip diacritics from tag values |
| `R - Trim Extra Space` | Remove leading/trailing/duplicate whitespace |
| `R - Upper Case Feats` | Uppercase `FEAT.`, `PROD.`, `WITH` in titles |
| `D - <Genre>` | Genre exports (with `Disc N/` subfolder) |
| `E - <Genre>` | Genre exports (flat, no `Disc/`) |

### Importing Actions

All actions are pre-bundled into [`Actions/Action Groups.json`](Actions/Action%20Groups.json) — a single file you can import into Mp3tag in one go. Or each subfolder in `Actions` has individual .json and .mta files to import. 

1. **Actions → Actions…** (`⌘6`) to open the Action Groups window
2. Click the **+** icon at the bottom-left of the sidebar to open its context menu
3. Choose **Import…** and select `Actions/<filename>.json` from this repo (individual `.mta` files can be imported the same way)

All groups appear in the sidebar. The `.mta` files remain useful as readable, diff-friendly source — the JSON file is the importable bundle.

> [!TIP]
> To export your own customised groups back to JSON (e.g. before committing your fork), open the same **+** menu and choose **Export…**.

### Export Actions

**Disc Number actions (`D - …`)** rewrite `_FILENAME` to include a `Disc N/` subfolder, then export embedded cover images. **External actions (`E - …`)** do the same but **without** a `Disc N/` subfolder — intended for single-disc albums.

> [!WARNING]
> The `D - …`, `E - …`, `C - …`, and `S - …` action groups are **personal export templates** shipped as-is for reference. The format strings point to the maintainer's external library mount (`/Volumes/Eksternal/Audio/`). You **must** adapt them before running on your own machine.

### Adapting Templates

Only the `D —`, `E —`, `C —`, and `S —` actions hard-code the maintainer's personal mount. The `F —`, `G —`, and `R —` actions are tag-only and have no paths.

**Recommended: `./configure` wizard**

```bash
./configure --new /Volumes/MyExternal/Music/
```

See [Quick Start: `./configure`](#quick-start-configure) for full options including dry-run, output modes, and JSON-only mode.

**Alternative: `sed` one-liner**

```bash
find . -type f \( -name "*.mta" -o -name "Action Groups.json" \) -print0 | \
  xargs -0 sed -i '' \
    -e 's|/Volumes/Eksternal/Audio/|/Volumes/MyExternal/Music/|g'
```

**Alternative: Manual edit**

Open each `.mta` file and edit the `1=...` line under `F=_FILENAME`. The format string is standard [Mp3tag scripting](https://docs.mp3tag.de/scripting/functions/).

> [!TIP]
> If you imported via the JSON bundle, duplicate an action first (**Actions → Actions… → select an action → Duplicate**), edit the copy, and leave the original untouched. This keeps the upstream file clean for future `git pull` updates.

**[&uarr; Back to Contents](#contents)**

---

## Scripts

This section documents the Python scripts and bash wrappers included in the repository. These scripts automate common tasks like retargeting export paths, applying folder structure presets, and generating importable JSON bundles. They're designed to make bulk operations easier and more consistent across your library.

One-off setup and maintenance scripts that ship with the repo. None are required for day-to-day Mp3tag use — they exist to make retargeting, syncing, and other bulk edits easier.

**Files:** `Scripts/retarget-paths.py`, `Scripts/layouts.py` (and the top-level wrapper `./configure`)

### Quick Start: `./configure`

```bash
./configure                                   # interactive wizard
./configure --new /Volumes/MyExternal/Music/ --layout standard --json-only --out /tmp/retargeted/ --yes
./configure --list-layouts
./configure --show-layout standard
```

The wrapper forwards all arguments to `Scripts/retarget-paths.py`. Both forms are equivalent.

### Interactive Wizard

Run with no arguments and the wizard walks through **4 steps**:

1. **Where should Mp3tag save your files?** — Which mount path to replace, and your new save destination. Auto-detects mounted volumes on macOS.
2. **How should your files be organised?** — A **card-based layout browser** shows every preset as a scannable card with name, folder structure, description, and an ASCII folder-tree preview. Type the card number, the preset id (e.g. `standard`), `0` to build a custom layout, or `–` to skip.
3. **Which files should be updated?** — Both `.mta` scripts and JSON action groups (recommended), or JSON only.
4. **Where should the updated files be written?** — In-place, to a separate output folder, or to stdout.

Before confirmation the wizard **pre-scans the repository** and shows file counts, JSON bundle counts, and the total number of replacements so you know exactly what will happen.

Type `?` at any prompt for inline help, `b` to go back, or `q` to quit. Pass `--no-color` to disable ANSI output.

### Layout Presets

**Common presets**

| Preset id | Structure | Best for |
|---|---|---|
| `standard` | `Artist / Album / TrackNo. Title` | General-purpose libraries |
| `artist_year_album` | `Artist / Year – Album / TrackNo. Title` | Discography-order browsing |
| `alphabetical` | `FirstLetter / Artist / Album / TrackNo. Title` | Very large libraries |
| `flat` | `TrackNo - Artist - Year - Album - Title` (single folder) | Metadata-driven libraries |

Run `./configure --list-layouts` to see all 15 presets across three categories (Common / Time & Genre / Special Purpose), or `./configure --show-layout <id>` for the format-string templates for any preset.

Choose `0` at the layout browser to enter the **custom layout builder** — a guided sub-wizard (steps A–F) that builds a folder hierarchy and filename format from scratch with a live preview after each choice.


### CLI Usage

```bash
# Mount retarget only.
./configure --new /Volumes/MyExternal/Music/ --yes

# Apply a layout only.
./configure --layout standard --yes

# Mount retarget + layout.
./configure --new /Volumes/MyExternal/Music/ --layout artist_year_album --yes

# Write retargeted copy to a directory.
./configure --new /Volumes/MyExternal/Music/ --layout alphabetical --out /tmp/retargeted/ --yes

# Print master JSON to stdout.
./configure --new /Volumes/MyExternal/Music/ --layout flat --stdout --yes > "Action Groups.retargeted.json"

# JSON only (skip .mta files).
./configure --new /Volumes/MyExternal/Music/ --layout standard --json-only --yes

# List / inspect layouts.
./configure --list-layouts
./configure --show-layout standard

# Forget saved configuration.
./configure --reset
```

### After Running

- **In-place**: re-import `Actions/Action Groups.json` into Mp3tag. Commit the rewritten files if you forked the repo.
- **`--out DIR`**: import `<DIR>/Actions/Action Groups.json` into Mp3tag.
- **`--stdout`**: paste into the **+** → **Import…** dialog in the Action Groups window, or `> "Action Groups.retargeted.json"` and import the file.

### Manual Editing

The bundled `.mta` files are plain text. The path string lives on the `1=...` line under `F=_FILENAME`. Open the file in any text editor and change that one line:

```
1=/Volumes/MyExternal/Music/Hip-Hop/By Year/$if(%year%,$left(%year%,4) - ,)%album%/$num(%track%,2). %title%
```

When you're done, update the matching entry in the relevant JSON file so the master `Action Groups.json` import bundle stays in sync. The JSON `format` value uses the same string with `/` escaped as `\/`.

**[&uarr; Back to Contents](#contents)**

---

## Settings

This section documents the configuration formats and file naming conventions used throughout the repository. Understanding these conventions will help you create your own sources and actions that integrate seamlessly with the existing infrastructure.

Configuration formats used across sources and actions — how settings panels are wired up, the file-naming conventions that tie everything together, and how the `.mta` action format works under the hood.

### Settings System

All sources use Mp3tag's native `.settings` JSON panel system. Settings files follow the naming convention:

```
SourceName#Settings….settings
```

The `….` (ellipsis `U+2026`) distinguishes settings files from other `.settings` files. Settings are loaded automatically when you open a source's settings dialog and stored persistently in `settings.json`.

### File Naming Conventions

| Convention | Meaning |
|---|---|
| `&` prefix on a letter | Keyboard shortcut accelerator |
| `#S` | Tag source entry point (appears in the Tag Sources menu) |
| `#Settings….` | Settings panel file for a source |
| `.inc` | Shared include file — not standalone, included by `.src` files |
| `.src` | Standalone source file |

### Creating & Editing Actions

Actions are stored as `.mta` files in the `Actions/` directory. Each file contains one or more action definitions in a numbered INI-like format:

```ini
[#0]
T=1
F=_ALL
1=Feat
2=feat
3=0
```

**Action types**

| Type | Description | Example Use |
|---|---|---|
| `T=1` | Replace | Replace `"feat."` with `"ft."` |
| `T=2` | Replace with Regex | Remove trailing parentheses |
| `T=3` | Format Value | Set field using placeholders |
| `T=4` | Guess Values | Parse filename into tags |
| `T=6` | Remove Fields | Delete specific fields |
| `T=7` | Remove Fields Except | Keep only specified fields |
| `T=8` | Merge Duplicate Fields | Combine multiple values |
| `T=9` | Split Field by Separator | Split field into multiple values |
| `T=10` | Import Cover from File | Add cover art from file |
| `T=11` | Export Cover to File | Save cover art to file |
| `T=13` | Remove Duplicate Fields | Remove duplicate entries |

**Common parameters**

- **`F`**: Field name (e.g. `TITLE`, `ARTIST`, `ALBUM`, `_ALL`)
- **`1`**: Input string, format pattern, or search string
- **`2`**: Replacement string or format string
- **`3`**: Additional parameter (varies by action type)

For detailed documentation, see `Actions/MTA Guide.md` in this repository.

**[&uarr; Back to Contents](#contents)**

---

## Guides

This section provides reference material for extending the repository with your own custom tag sources and Mp3tag scripts. Whether you're building a new source for a music service or writing format strings for complex tag transformations, these guides will help you understand the underlying formats and capabilities.

Reference material for extending the repo — building new tag sources from scratch and writing Mp3tag format strings.

### Creating Web Sources

Source files use an INI-like format:

```ini
[Name]=Source Name
[BasedOn]=www.example.com
[IndexUrl]=https://www.example.com/search/%s
[AlbumUrl]=https://api.example.com/album/
[WordSeparator]=%20
[IndexFormat]=%_preview%|%_url%|%Album%|%Artist%|%Year%
[SearchBy]=%Artist% %Album%
[Encoding]=url-utf-8

[ParserScriptIndex]=...
# Parser script goes here

[ParserScriptAlbum]=...
# Album parser goes here
```

**Key parameters**

| Parameter | Description |
|---|---|
| `[Name]` | Display name for the source |
| `[BasedOn]` | Base website URL |
| `[IndexUrl]` | Search URL with `%s` placeholder |
| `[AlbumUrl]` | Album detail URL template |
| `[IndexFormat]` | Format string for search results |
| `[SearchBy]` | Fields used for searching |
| `[ParserScriptIndex]` | Script to parse search results |
| `[ParserScriptAlbum]` | Script to parse album details |

**Common parser commands**

- `FindLine "text"` — Find a line containing text
- `RegexpReplace "pattern" "replacement"` — Replace using regex
- `json "ON" "current"` — Enable JSON parsing
- `json_select "key"` — Select a JSON field
- `say "text"` — Output literal text
- `sayrest` — Output the rest of the current line

For full documentation, see the [Mp3tag Tag Sources documentation](https://docs.mp3tag.de/tag-sources/).

### Mp3tag Scripting

Mp3tag supports scripting functions in format strings, actions, and filters.

**Common functions**

| Function | Description |
|---|---|
| `$upper(string)` | Convert to uppercase |
| `$lower(string)` | Convert to lowercase |
| `$caps(string)` | Title case |
| `$replace(string,from,to)` | Replace occurrences |
| `$regexp(string,pattern,replacement)` | Regex replace |
| `$if(condition,then,else)` | Conditional |
| `$trim(string)` | Remove leading/trailing whitespace |
| `$num(number,length)` | Format number with zero-padding |
| `$if2(a,b)` | Return `a` if not empty, else `b` |

**Examples**

```
$caps(%title%)
$replace(%artist%, " & ", " and ")
$if(%albumartist%, %albumartist%, %artist%)
```

In an action (`T=3`):

```ini
[#0]
T=3
F=TITLE
1=$caps(%title%)
```

For the full reference, see the [Mp3tag Scripting Documentation](https://docs.mp3tag.de/scripting/functions/).

**[&uarr; Back to Contents](#contents)**

---

## FAQ

This section answers the most common questions about using this repository, troubleshooting installation issues, and understanding the design decisions behind the action prefixes and file organization.

**Why don't symlinks work?**

Both the macOS sandbox (used by the App Store version of Mp3tag) and the website version's file-access model reject symlinks to files outside the data directory. Always use `cp -R` to copy files into Mp3tag's application support folder.

**Why are there letter prefixes on the actions?**

The single-letter prefix (`F -`, `G -`, `R -`, etc.) gives every action group a unique first character. This lets you assign clean macOS keyboard shortcuts via **System Settings → Keyboard → Keyboard Shortcuts → App Shortcuts** without collisions, since the shortcut matches the exact menu-item title. The letter also doubles as Mp3tag's menu accelerator key.

**How do I change the export paths?**

Run the `./configure` wizard from the repo root:

```bash
./configure --new /Volumes/MyExternal/Music/
```

See [Quick Start: `./configure`](#quick-start-configure) for the full list of options (dry-run, output modes, layout presets, JSON-only).

**How do I update the repo?**

```bash
git pull origin main
```

If you've made local changes (e.g. after running `./configure` with the in-place mode), re-run `./configure` after pulling to preserve your modifications. Or use `--out` to write a separate copy and diff before merging.

**Can I use this on Windows or Linux?**

The tag sources and action files are platform-agnostic — they work wherever Mp3tag runs. The `./configure` wizard requires Python 3 and a POSIX shell. On Windows, use Git Bash, WSL, or run the Python script directly:

```bash
python3 Scripts/retarget-paths.py
```

The macOS-specific installation paths (`~/Library/Application Support/Mp3tag/`) will differ on other platforms — consult the [Mp3tag documentation](https://docs.mp3tag.de/) for the correct data directory.

**[&uarr; Back to Contents](#contents)**

---

## Additional Resources

- **[Mp3tag Official Website](https://www.mp3tag.de/en/)** — Download and general information
- **[Mp3tag Documentation](https://docs.mp3tag.de/)** — Comprehensive user guide
- **[Mp3tag Community Forums](https://community.mp3tag.de/)** — Community support and discussions
- **[Mp3tag Scripting Functions](https://docs.mp3tag.de/scripting/functions/)** — Complete scripting reference
- **[Mp3tag Tag Sources](https://docs.mp3tag.de/tag-sources/)** — Guide to creating custom tag sources

---

## License

Personal toolkit — free to fork and adapt. Some sources incorporate upstream scripts from the [Mp3tag community forums](https://community.mp3tag.de/). Check individual source file headers for attribution.
