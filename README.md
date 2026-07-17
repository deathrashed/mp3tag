<div align="center">
<img src="https://mp3tag.app/assets/images/mp3tag-logo.png" width="450" alt="Mp3tag" />

# deathrashed / mp3tag

**A curated collection of web sources, tag sources, and configuration for [Mp3tag](https://www.mp3tag.de/en/) on macOS.**

Modular tag sources for streaming services, music databases, cover art, lyrics, and genres — each with a configurable settings panel and consistent comment style.

[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://www.mp3tag.de/en/mac.html)
[![Mp3tag](https://img.shields.io/badge/Mp3tag-v3.28%2B-blue)](https://www.mp3tag.de/en/)

</div>

---

## Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [What is Mp3tag?](#what-is-mp3tag)
- [Getting Started](#getting-started)
- [Tag Sources](#tag-sources)
  - [iTunes+](#-itunes)
  - [Metal Archives](#-metal-archives--tag-sources)
  - [Metallum Genres](#-metallum-genres)
  - [Last.fm Genres](#-lastfm-genres)
  - [MusicBrainz Expanded](#-musicbrainz-expanded)
  - [Bandcamp](#-bandcamp)
  - [Qobuz](#-qobuz)
  - [Deezer](#-deezer)
  - [Soundcloud](#-soundcloud)
  - [Genius Lyrics](#-genius-lyrics)
- [Cover Art Sources](#cover-art-sources)
  - [iTunes Cover Art](#-itunes-cover-art)
  - [Deezer Cover Art](#-deezer-cover-art-1)
  - [Qobuz Cover Art](#-qobuz-cover-art-1)
  - [Soundcloud Cover Art](#-soundcloud-cover-art-1)
  - [COV — Cover Art Search](#cov--cover-art-search)
- [Actions](#actions)
  - [Why the `S - ` / `F - ` / `D - ` prefixes?](#why-the-s-----f-----d---prefixes)
  - [Importing the bundled action groups](#importing-the-bundled-action-groups)
  - [Disc Number actions](#disc-number-actions-d---)
  - [External (Export) actions](#external-export-actions-e---)
  - [Adapting the export templates](#adapting-the-export-templates)
- [Settings System](#settings-system)
- [File Naming Conventions](#file-naming-conventions)
- [Creating and Editing Actions](#creating-and-editing-actions-mta-files)
- [Creating Web Sources](#creating-web-sources-src-files)
- [Scripting in Mp3tag](#scripting-in-mp3tag)
- [Git Workflow](#git-workflow)
- [Additional Resources](#additional-resources)

---

## Overview

This repository contains personal configuration, actions, and source scripts for **Mp3tag** on macOS. It is designed to be cloned directly into the Mp3tag application support directory so that sources and actions are available out of the box.

---

## Repository Structure

```
.
├── .icon/                          # Provider icons for documentation
├── Actions/                        # Mp3tag action groups (.mta files)
│   ├── Format/                     # Case conversion, date formats, etc.
│   ├── Genre/                      # Genre-specific actions and mappings
│   ├── Regex/                      # Regex-based text cleaning
│   ├── Disc Numbers/               # Disc number formatting
│   └── Eksternal/                  # External / export-related actions
├── Sources/                        # Web sources and supporting files
│   ├── *.src                       # Standalone tag / cover sources
│   ├── *.inc                       # Shared parser include files
│   ├── *#Settings….settings        # Settings panel definitions (JSON)
│   ├── Mp3tagSettings/             # Export templates, actions, mp3tag.cfg
│   └── settings.json               # Runtime settings store (auto-generated)
└── README.md
```

---

## What is Mp3tag?

Mp3tag is a metadata editor for audio files that allows you to:

- **Batch edit tags** for multiple files simultaneously
- **Rename files** based on tag information or vice versa
- **Import tags** from online databases (MusicBrainz, Deezer, Qobuz, etc.)
- **Download cover art** automatically from various sources
- **Format and clean** tag values using actions and scripts
- **Support multiple formats**: MP3, MP4, FLAC, OGG, WMA, APE, and more

For more information, visit the [official Mp3tag website](https://www.mp3tag.de/en/) and [documentation](https://docs.mp3tag.de/).

---

## Getting Started

### Installation



Then restart Mp3tag — sources appear automatically under **Tag Sources** in the toolbar.
## Getting Started with Mp3tag

### Installation

1. **Download**: Get the latest version from the [official website](https://www.mp3tag.de/en/download.html)
2. **Install**: Follow the installation instructions for macOS
3. **Configure**: Point Mp3tag to use this repository's actions and sources
Symlink (or copy) this repository into your Mp3tag application support directory:

```bash
# macOS — Mp3tag reads from this path
git clone https://github.com/deathrashed/mp3tag.git \
  ~/Library/Containers/app.mp3tag.Mp3tag/Data/Library/Application\ Support/Mp3tag
```

Or symlink the `Sources/` folder only:

```bash
ln -s ~/mp3tag \
  ~/Library/Containers/app.mp3tag.Mp3tag/Data/Library/Application\ Support/Mp3tag/Sources
```
### Basic Usage

1. **Load Files**:
   - Open Mp3tag
   - Navigate to `File > Add directory...` (or press `Cmd+D`)
   - Select the folder containing your audio files
   - Or drag and drop files directly into Mp3tag

2. **Edit Tags**:
   - Select one or more files in the file list
   - Modify tag fields in the Tag Panel on the left (Title, Artist, Album, Year, Genre, etc.)
   - Changes are applied immediately to the selected files

3. **Save Changes**:
   - Click the save icon in the toolbar
   - Or press `Cmd+S` to save all changes

4. **Import Tags from Online Databases**:
   - Select files you want to tag
   - Go to `Tag Sources` menu
   - Choose a source (e.g., MusicBrainz, Discogs, Deezer)
   - Search and select the correct match
   - Apply the tags

5. **Rename Files Based on Tags**:
   - Select files to rename
   - Go to `Convert > Tag - Filename` (or press `Alt+Cmd+1`)
   - Enter a format string, e.g., `%artist% - %title%`
   - Preview and apply the changes

---

## How to Edit Tags in Mp3tag

### Manual Tag Editing

1. **Select Files**: Click on files in the file list (use `Cmd+Click` for multiple files)
2. **Edit Fields**: Click on any field in the Tag Panel and type your changes
3. **Batch Edit**: Select multiple files to apply the same tag value to all
4. **Save**: Press `Cmd+S` or click the save icon

### Using Actions for Automated Editing

Actions allow you to automate repetitive tag editing tasks:

1. **Access Actions**: Go to `Actions > Actions...` (or press `Alt+6`)
2. **Select Action Group**: Choose from your custom action groups
3. **Apply**: Select files and run the action

Actions can:
- Format text (case conversion, date formats)
- Replace text or use regex patterns
- Clean and normalize tag values
- Remove duplicates or unwanted fields
- Merge or split fields
### Basic Usage

1. **Load Files**: `File > Add directory…` (`Cmd+D`) or drag and drop files into Mp3tag
2. **Edit Tags**: Select files and modify fields in the Tag Panel on the left
3. **Save Changes**: `Cmd+S` or click the save icon
4. **Import Tags**: `Tag Sources` menu → choose a source → search and apply
5. **Rename Files**: `Convert > Tag - Filename` (`Alt+Cmd+1`) with a format string like `%artist% - %title%`

### Using Actions

1. Open `Actions > Actions…` (`Alt+6`)
2. Select an action group
3. Select files and run the action

---

## Tag Sources

### <img src=".icon/itunes.png" height="20" valign="middle" /> iTunes+

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

### <img src=".icon/metallum.png" height="20" valign="middle" /> Metal Archives — Tag Sources

**Files:** `Me&tal Archives#S - Search by Band.src` · `Me&tal Archives#S - Search by Band + Album.src` · `Me&tal Archives#S - Search by Album.src`

Three search modes for fetching complete release metadata from [metal-archives.com](https://www.metal-archives.com):

| Source | Search by | Use case |
|---|---|---|
| Search by Band | `%artist%` | Find all releases for an artist |
| Search by Band + Album | `%artist% %album%` | Most precise — recommended |
| Search by Album | `%album%` | When artist is ambiguous |

Returns: Title, Artist, Album, Year, Genre, Country, Label, Catalog Number, and track listing.

---

### <img src=".icon/metallum-genres.png" height="20" valign="middle" /> Metallum Genres

**Files:** `Metallum Genres#S - Metallum Genres.src` · `Metallum Genres#Settings….settings`

Standalone genre-only source querying Metal Archives directly. Designed to run alongside other tag sources to enrich genre tags. Includes a suite of genre normalisation replacements (e.g. `Death/Thrash Metal` → `Death/Thrash; Death Metal; Thrash Metal`) that expand hybrid genres into individual searchable tokens.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Keep era descriptions | `false` | Preserve brackets like `(early)`, `(mid-period)` |
| Deduplicate genres | `true` | Remove duplicate genre tokens |
| Genre separator | `; ` | Delimiter between multiple genres |
| Write dedicated tags | `true` | Fill `Metal Archives Country`, `Status`, `Formed`, etc. |
| Write band info to Comment | `true` | Append country, location, status, themes to `COMMENT` |

**Custom genre replacements:** Edit the `CUSTOM GENRE REPLACEMENTS` block inside the `.src` file:
```
replace "Original Text" "Replacement Text"
```

---

### <img src=".icon/lastfm.png" height="20" valign="middle" /> Last.fm Genres

**Files:** `Last.fm#S - Last.fm Genres.src` · `Last.fm#Settings….settings`

Fetches an artist's top tags from the Last.fm API and writes them as genre tags. Genre count and separator are configurable.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Genre limit | `1` | How many top tags to retrieve (1, 2, 3, 4, 5, or 10) |
| Genre separator | `; ` | Delimiter between multiple genres |

> Uses the Last.fm `artist.gettoptags` endpoint with a public embedded API key.

---

### <img src=".icon/musicbrainz.png" height="20" valign="middle" /> MusicBrainz Expanded

**Files:** `MusicBrainz Expanded.inc` + 7 `.src` entry points · `MusicBrainz Expanded#Settings….settings`

Feature-rich MusicBrainz source with multiple search entry points:

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

### <img src=".icon/bandcamp.png" height="20" valign="middle" /> Bandcamp

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

### <img src=".icon/qobuz.png" height="20" valign="middle" /> Qobuz

**Files:** `Qobuz.inc` · `&Qobuz#S - Qobuz AU.src` · `&Qobuz#S - Qobuz US.src` · `&Qobuz#Settings….settings`

Full metadata source for Qobuz with regional entry points (AU and US) sharing a common parser.

Returns: Title, Artist, AlbumArtist, Album, Year, Genre, Label, Track number, Disc number, Composer, Lyricist, Credits, Publisher, ISRC, and high-resolution cover art.

---

### <img src=".icon/deezer-icon.png" height="20" valign="middle" /> Deezer

**Files:** `Deezer#S - Deezer by Album.src` · `Deezer#S - Deezer by Title.src`

| Source | Search by |
|---|---|
| By Album | Artist + Album |
| By Title | Track title |

Returns: Title, Artist, AlbumArtist, Album, Year, Genre, Track number, and cover art.

---

### <img src=".icon/soundcloud.png" height="20" valign="middle" /> Soundcloud

**Files:** `Soundcloud.inc` · `Soundcloud#S - Soundcloud Search.src` · `Soundcloud Artwork.inc` · `Soundcloud#Settings….settings`

Searches SoundCloud for tracks and retrieves metadata.

Returns: Title, Artist, Year, Genre, Description, and cover art.

---

### <img src=".icon/genius.png" height="20" valign="middle" /> Genius Lyrics

**Files:** `Genius#Lyrics.inc` · `Genius#S - Genius Lyrics.src` · `Genius#Settings….settings`

Fetches lyrics from [genius.com](https://genius.com) and writes them to the `UNSYNCEDLYRICS` tag field.

**Settings:**

| Setting | Default | Description |
|---|---|---|
| Line ending character | `CR (Mac)` | Line ending format for lyrics |
| Write UNSYNCEDLYRICS | `true` | Write to standard UNSYNCEDLYRICS field |

---

## Cover Art Sources

### <img src=".icon/itunes.png" height="20" valign="middle" /> iTunes Cover Art

**File:** `&Art#&iTunes.src` → `iTunes Artwork.inc`

Searches Apple Music for cover art. Always retrieves the original uncompressed source image at maximum available resolution. No settings required — hardcoded to highest quality.

---

### <img src=".icon/deezer-icon.png" height="20" valign="middle" /> Deezer Cover Art

**File:** `&Art#&Deezer.src`

Searches Deezer for album artwork. Returns up to 1200×1200 px JPEG. Parses Deezer's embedded JSON state object.

**Search by:** Artist + Album

---

### <img src=".icon/qobuz.png" height="20" valign="middle" /> Qobuz Cover Art

**File:** `&Art#&Qobuz.src` → `Qobuz.inc`

Searches Qobuz for album artwork and extracts the best available image URL from the structured JSON response.

**Search by:** AlbumArtist + Album

---

### <img src=".icon/soundcloud.png" height="20" valign="middle" /> Soundcloud Cover Art

**File:** `&Art#&Soundcloud.src` → `Soundcloud Artwork.inc`

Fetches SoundCloud track or artist artwork by artist name and title, or by direct URL.

---

### COV — Cover Art Search

**File:** `COV#S - Cover Art Search.src`

Opens [covers.musichoarders.xyz](https://covers.musichoarders.xyz/) in your default web browser, pre-filled with the track's artist and album. Aggregates cover art from Apple Music, Spotify, Tidal, Deezer, Amazon, and Discogs.

> Opens your browser for manual interaction, in accordance with the site's [integration guidelines](https://covers.musichoarders.xyz/).

---

## Actions

This repo ships a curated set of action groups under `Actions/`, plus a single bundled import file `Actions/Action Groups.json`. They are organised by the first letter of the group name, which doubles as the keyboard accelerator shown in Mp3tag's **Actions** menu:

| Prefix | Category | Purpose |
|---|---|---|
| `F` | **Format** | Text formatting, value transformation, tag moves |
| `G` | **Genre** | Per-genre canonicalisation (e.g. `G - Death Metal` → `Death Metal`) |
| `R` | **Regex** | Regex-based cleanup and normalisation |
| `D` | **Disc Numbers** | Filename templates that include a `Disc N/` subfolder |
| `E` | **Eksternal** | Maintainer's personal export templates (no `Disc/` subfolder) |

The bundled action groups in this repo:

| Action | Purpose |
|---|---|
| `F - Artist to Album Artist` | Copy `ARTIST` → `ALBUMARTIST` |
| `F - Case Conversion` | Convert tag values to UPPER / lower / Title Case |
| `F - Combo` | Combined formatting pass for tags |
| `F - Combo - Accents` | Combo plus accent stripping |
| `F - Fix` | General tag fixes (whitespace, separators) |
| `F - Mixed Case` | Force Mixed Case for the standard tag fields |
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
| `R - Add Apostrophes` | Insert apostrophes in common English contractions |
| `R - English Naming` | Standardise English-language naming conventions |
| `R - Smart Title Case` | Apply a smarter Title Case to `TITLE`/`ALBUM` |
| `R - Spacing Proper` | Fix spacing around punctuation |
| `R - Strip Accents` | Strip diacritics from tag values |
| `R - Trim Extra Space` | Remove leading/trailing/duplicate whitespace |
| `R - Upper Case Feats` | Uppercase `FEAT.`, `PROD.`, `WITH` in titles |
| `D - Electronic` | Electronic exports (with `Disc/` subfolder) |
| `D - Hip-Hop` | Hip-Hop exports (with `Disc/` subfolder) |
| `D - Metal` | Metal exports (with `Disc/` subfolder) |
| `D - Miscellaneous` | Catch-all (with `Disc/` subfolder) |
| `D - Punk & Hardcore` | Punk & Hardcore exports (with `Disc/` subfolder) |
| `D - Rock & Grunge` | Rock & Grunge exports (with `Disc/` subfolder) |
| `E - Electronic` | Electronic exports (flat, no `Disc/`) |
| `E - Hip-Hop` | Hip-Hop exports (flat, no `Disc/`) |
| `E - Metal` | Metal exports (flat, no `Disc/`) |
| `E - Miscellaneous` | Catch-all (flat, no `Disc/`) |
| `E - Punk & Hardcore` | Punk & Hardcore exports (flat, no `Disc/`) |
| `E - Rock & Grunge` | Rock & Grunge exports (flat, no `Disc/`) |

Apply actions via **Actions → Actions…** (`⌥6`). For the technical reference on `.mta` syntax and `T=` action types, see [Creating and Editing Actions](#creating-and-editing-actions-mta-files).

### Why the `S - ` / `F - ` / `D - ` prefixes?

When you assign a custom macOS keyboard shortcut via **System Settings → Keyboard → Keyboard Shortcuts → App Shortcuts**, the shortcut is matched to a menu item by its **exact** title — the first character of the title is what macOS uses as the trigger key. If six action groups all start with the same word (e.g. "Save Album"), they collide and the system shortcut is ambiguous.

The single-letter prefix (`S - Search`, `F - Fix`, `D - Disc Number`, `E - Export`, etc.) gives every action group a **unique first letter**, so you can assign a clean, distinct macOS shortcut to each one without collisions. The letter is also the mnemonic Mp3tag itself shows in its **Actions** menu accelerator, so the keyboard hint matches what you see in the menu bar.

In short: the prefixes exist so both macOS and Mp3tag can give every action a unique, predictable keyboard shortcut that matches the menubar text exactly.

### Importing the bundled action groups

All actions in this repo are pre-bundled into [`Actions/Action Groups.json`](Actions/Action%20Groups.json) — a single file you can import into Mp3tag in one go instead of loading each `.mta` file individually.

To import:

1. Open Mp3tag.
2. **Actions → Actions…** (`⌥6`) to open the Actions window.
3. In the left sidebar, right-click the action group list and choose **Import…** (or use the **File → Import Action Groups** menu in the Actions window).
4. Select `Actions/Action Groups.json` from this repo.

All action groups (`F - …`, `G - …`, `R - …`, `D - …`, `E - …`) will appear in the sidebar. The `.mta` files in the subdirectories remain useful as readable, diff-friendly source — the JSON file is the importable bundle.

**To export your own customised groups back to JSON** (e.g. before committing your fork), right-click the group list in the Actions window and choose **Export…** — Mp3tag will write a fresh `Action Groups.json` you can drop back into the repo.

### Disc Number actions (`D - …`)

> **These are personal export templates** shipped as-is for reference. The format strings in the `.mta` files point to the maintainer's external library mount (`/Volumes/Eksternal/Audio/`) — edit them to match your own library layout before running. See [Adapting the export templates](#adapting-the-export-templates) below.

Each action rewrites `_FILENAME` to a folder structure that includes a `Disc N/` subfolder, then strips embedded cover images. Useful when exporting a multi-disc album where you want disc folders.

### External (Export) actions (`E - …`)

> **Personal export templates** — same caveat as the `D - …` actions above. Edit the mount path before running.

Like the Disc Number actions, but **without** a `Disc N/` subfolder. Shipped for single-disc albums on the maintainer's `/Volumes/Eksternal/...` export path.

### Adapting the export templates

The `D - …` and `E - …` actions are shipped with the maintainer's personal library layout hard-coded into the format string. Before running them, you need to swap `/Volumes/Eksternal/Audio/<Genre>/` for your own export root.

**Quick `sed` one-liner.** Run this from the repo root, replacing the two paths with your own:

```bash
# Example: point the templates at /Volumes/MyExternal/Music/Metal/...
find . -type f \( -name "*.mta" -o -name "Action Groups.json" \) -print0 | \
  xargs -0 sed -i '' \
    -e 's|/Volumes/Eksternal/Audio/|/Volumes/MyExternal/Music/|g' \
    -e 's|/Audio/Metal/|/Music/Metal/|g' \
    -e 's|/Audio/Electronic/|/Music/Electronic/|g' \
    -e 's|/Audio/Hip-Hop/|/Music/Hip-Hop/|g' \
    -e 's|/Audio/Punk|/Music/Punk|g' \
    -e 's|/Audio/Rock|/Music/Rock|g'
```

This rewrites the path in every `.mta` file and in `Action Groups.json` in one pass. Adjust the genre folder names (`Metal`, `Electronic`, `Hip-Hop`, etc.) to match whatever your library uses.

**Manual edit (per file).** If you prefer a more targeted change, open each `.mta` file in a text editor and edit the `1=...` line:

1. **Change the mount path.** Replace `/Volumes/Eksternal/Audio/` with your own export root, e.g. `/Volumes/MyExternal/Music/`, `~/Music/`, or wherever your library lives.
2. **Change the genre folder** (`Metal`, `Electronic`, etc.) to match your own folder naming.
3. **Adjust the format string** if you want a different folder/file layout. The string is standard Mp3tag scripting — see [Scripting in Mp3tag](#scripting-in-mp3tag) and the [format string reference](https://docs.mp3tag.de/scripting/functions/).

**Tip:** If you imported the action groups via the JSON bundle (see [Importing the bundled action groups](#importing-the-bundled-action-groups)), duplicate an action first via **Actions → Actions… → right-click → Duplicate**, edit the copy, and leave the original alone. This keeps the upstream file untouched and makes future `git pull` updates conflict-free.

---

## Settings System

All sources use Mp3tag's native `.settings` JSON panel system. Settings files follow the naming convention:

```
SourceName#Settings….settings
```

The `….` (ellipsis `U+2026`) distinguishes settings files from other `.settings` files. Settings are loaded automatically when you open a source's settings dialog and stored persistently in `settings.json`.

---

## File Naming Conventions

| Convention | Meaning |
|---|---|
| `&` prefix on a letter | Keyboard shortcut accelerator |
| `#S` | Tag source entry point (appears in the Tag Sources menu) |
| `#Settings….` | Settings panel file for a source |
| `.inc` | Shared include file — not standalone, included by `.src` files |
| `.src` | Standalone source file |

---

## Creating and Editing Actions (.mta Files)

Actions are stored as `.mta` files in the `Actions/` directory. Each file contains one or more action definitions in a numbered INI-like format:

```ini
[#0]
T=1
F=_ALL
1=Feat
2=feat
3=0
```

### Action Types

| Type | Description | Example Use |
|------|-------------|-------------|
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

### Common Parameters

- **`F`**: Field name (e.g. `TITLE`, `ARTIST`, `ALBUM`, `_ALL` for all fields)
- **`1`**: Input string, format pattern, or search string
- **`2`**: Replacement string or format string
- **`3`**: Additional parameter (varies by action type)

### Example Action

```ini
[#0]
T=1
F=_ALL
1=Feat
2=feat
3=0
```

For detailed action type documentation, see `Actions/MTA Guide.md` in this repository.

---

## Creating Web Sources (.src Files)

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

### Key Parameters

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

### Common Parser Commands

- `FindLine "text"` — Find a line containing text
- `RegexpReplace "pattern" "replacement"` — Replace using regex
- `json "ON" "current"` — Enable JSON parsing
- `json_select "key"` — Select a JSON field
- `say "text"` — Output literal text
- `sayrest` — Output the rest of the current line

For full documentation, see the [Mp3tag Tag Sources documentation](https://docs.mp3tag.de/tag-sources/).

---

## Scripting in Mp3tag

Mp3tag supports scripting functions in format strings, actions, and filters.

### Common Functions

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

### Examples

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

See the full [Mp3tag Scripting Documentation](https://docs.mp3tag.de/scripting/functions/).

---

## Additional Resources

- **[Mp3tag Official Website](https://www.mp3tag.de/en/)**: Download and general information
- **[Mp3tag Documentation](https://docs.mp3tag.de/)**: Comprehensive user guide
- **[Mp3tag Community Forums](https://community.mp3tag.de/)**: Community support and discussions
- **[Mp3tag Scripting Functions](https://docs.mp3tag.de/scripting/functions/)**: Complete scripting reference
- **[Mp3tag Tag Sources](https://docs.mp3tag.de/tag-sources/)**: Guide to creating custom tag sources

---

## License

Personal toolkit — free to fork and adapt. Some sources incorporate upstream scripts from the [Mp3tag community forums](https://community.mp3tag.de/). Check individual source file headers for attribution.
