<div align="center">
<img src="Assets/Icon/mp3tag-ring-2.png" width="400" alt="Mp3tag" />

# 𝗠𝗣𝟯𝗧𝗔𝗚

**A curated collection of web sources, tag sources, and configuration for [Mp3tag](https://www.mp3tag.de/en/) on macOS.**

Modular tag sources for streaming services, music databases, cover art, lyrics, and genres — each with a configurable settings panel and consistent comment style.

[![MP3TAG](https://img.shields.io/badge/Mp3tag%20—%20v3.28%2B-1e1e1e?style=for-the-badge&logo=applemusic&logoColor=faa701)](https://www.mp3tag.de/en/)
[![PLATFORM](https://img.shields.io/badge/macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=faa701)](https://www.apple.com/macos/)
[![CONFIGURE](https://img.shields.io/badge/interactive%20wizard-1e1e1e?style=for-the-badge&logo=gnubash&logoColor=faa701)](./configure)

[![SOURCES](https://img.shields.io/badge/tag%20sources%20—%208%2B-1e1e1e?style=for-the-badge&logo=audiomack&logoColor=faa701)](./Sources)
[![ACTIONS](https://img.shields.io/badge/action%20groups%20—%2012%2B-1e1e1e?style=for-the-badge&logo=audiomack&logoColor=faa701)](./Actions)
[![GENRES](https://img.shields.io/badge/genre%20presets%20—%2070%2B-1e1e1e?style=for-the-badge&logo=audiomack&logoColor=faa701)](./Actions/Genre)

[OVERVIEW](./Assets/DOCS.md) · [SOURCES](#sources) · [ACTIONS](./Actions/README.md) · [SCRIPTS](./Scripts/README.md) · [SETTINGS](./Assets/DOCS.md) · [GUIDES](#guides) · [FAQ](#faq)

</div>

## Quick Start

1. **Configure the repository (recommended).** Run the interactive configuration wizard to personalise the bundled actions for your library:

   ```bash
   chmod +x configure
   ./configure
   ```
   
   The wizard lets you:
   
   * Retarget bundled export paths to your own library
   * Choose a folder layout preset
   * Rename the parent music folder
   * Regenerate `.mta` files and JSON action bundles
   * Preview or write the generated files
   
   See [Quick Start: `./configure`](#quick-start-configure) for all available options.

> [!TIP]
> **New here?** Run `./configure` first. It automatically updates the bundled actions for your library and saves you from manually editing `.mta` files.

2. **Install Tag Sources.** Copy this repository's `Sources/` folder into Mp3tag's data directory (see [Getting Started](./Assets/DOCS.md#getting-started) for the exact location), or let Mp3tag open it for you:

   * Open the **Tag Sources** by selecting it from the menubar.
   * Select **Open Tag Sources Folder** at the bottom of the menu.
   * Copy the contents of this repository's `Sources/` folder into the folder that opens.

3. **Import Action Groups.** Open **Actions → Actions…** (`⌘6`), click the **+** button in the lower-left corner, choose **Import…**, then select:

   * `Actions/Action Groups.json` to import every action, or
   * any category `.json` file to import a single action group, or
   * individual `.mta` files to import specific actions.

   See [Importing Actions](./Assets/DOCS.md#importing-actions) for more details.

4. **Start tagging.** Your tag sources will appear immediately under **Tag Sources**, and imported actions will be available from **Actions** (`⌘6`).

Prefer the terminal?

```bash
DATA_DIR="$HOME/Library/Containers/app.mp3tag.Mp3tag/Data/Library/Application Support/Mp3tag"

cp -R Sources "$DATA_DIR"
```

> [!NOTE]
> **Copy the files—don't create symlinks.** The App Store sandbox and Mp3tag's file-access model do not support symlinked sources. Use `cp -R` or Mp3tag's **Import…** dialog instead.

**[↑](#contents)**


---

<details>
<summary>
<a id="overview"></a><strong><a href="#overview"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;OVERVIEW</strong>
</summary>

────────

This repository contains personal configuration, tag sources, actions, and scripts for [Mp3tag](https://www.mp3tag.de/en/) on macOS. It is designed to be cloned directly into the Mp3tag application support directory so that sources and actions are available out of the box.

**What you get:**

- **9 tag sources** — Apple Music, Metal Archives, Last.fm, MusicBrainz, Bandcamp, Qobuz, Deezer, SoundCloud, and Genius Lyrics
- **4 cover art sources** — iTunes, Deezer, Qobuz, and SoundCloud album artwork
- **151 action scripts** — formatting, genre canonicalisation, regex cleanup, and library export
- **70+ genre presets** — one-click `GENRE` tag setters covering metal sub-genres, hip-hop, punk, electronic, and more
- **Interactive configure wizard** — retarget paths, pick folder layouts, and generate importable JSON bundles

### Repository Structure

<details>
<summary><strong>Show full directory tree…</strong></summary>

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

</details>

| Folder | What it is |
|---|---|
| `Eksternal/` | Save actions with per-genre folders. Includes `Disc Numbers/`, `Compilation/`, `Splits/` sub-folders. Each has a README. |
| `Format/` | Tag clean-up, normalisation, and value transformation. Tag-only — no file paths. |
| `Genre/` | One-click `GENRE` setters. 9 top-level + 60+ extended presets under `Additional Genres/`. |
| `Regex/` | Regex-driven cleanup actions. 6 top-level + 15 extended under `Additional Regex/`. |

---

### What is Mp3tag?

Mp3tag is a metadata editor for audio files that allows you to:

- **Batch edit tags** for multiple files simultaneously
- **Rename files** based on tag information or vice versa
- **Import tags** from online databases (MusicBrainz, Deezer, Qobuz, etc.)
- **Download cover art** automatically from various sources
- **Format and clean** tag values using actions and scripts
- **Support multiple formats**: MP3, MP4, FLAC, OGG, WMA, APE, and more

For more information, visit the [official Mp3tag website](https://www.mp3tag.de/en/) and [documentation](https://docs.mp3tag.de/).

---

### Getting Started

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

1. **Load files** — `File > Add directory…` (`Cmd+D`) or drag and drop into Mp3tag
2. **Edit tags** — Select files, modify fields in the Tag Panel, changes apply immediately
3. **Save** — `Cmd+S` or click the save icon
4. **Import tags** — `Tag Sources` menu → choose a source → search and apply
5. **Rename files** — `Convert > Tag - Filename` (`Alt+Cmd+1`) with a format string like `%artist% - %title%`

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="sources"></a><strong><a href="#sources"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;SOURCES</strong>
</summary>
────────

<p align="">
<a href="https://performance-partners.apple.com/search-api"><strong>iTUNES</strong></a> •
<a href="https://www.metal-archives.com/users/dethrashed"><strong>METALLUM</strong></a> •
<a href="https://musicbrainz.org/user/deathrashed"><strong>MUSICBRAINZ</strong></a> •
<a href="https://www.last.fm/user/deathrashed"><strong>LAST.FM</strong></a> •
<a href="https://bandcamp.com/deathrashed"><strong>BANDCAMP</strong></a> •
<a href="https://www.deezer.com/us/profile/6670925423"><strong>DEEZER</strong></a> •
<a href="https://soundcloud.com/deathrashed"><strong>SOUNDCLOUD</strong></a> •
<a href="https://genius.com/deathrashed"><strong>GENIUS</strong></a>
</p>

### Individual Tag Sources

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

#### 

> <details>
> <summary><a id="cover-art-sources"></a><strong>Cover Art Sources</strong></summary>
>
> #### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/applemusic.svg" height="18" valign="middle" /> iTunes Cover Art
>
> **File:** `&Art#&iTunes.src` → `iTunes Artwork.inc`
>
> Searches Apple Music for cover art. Always retrieves the original uncompressed source image at maximum available resolution. No settings required — hardcoded to highest quality.
>
> ---
>
> #### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/deezer.svg" height="18" valign="middle" /> Deezer Cover Art
>
> **File:** `&Art#&Deezer.src`
>
> Searches Deezer for album artwork. Returns up to 1200×1200 px JPEG. Parses Deezer's embedded JSON state object.
>
> **Search by:** Artist + Album
>
> ---
>
> #### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/qobuz.svg" height="18" valign="middle" /> Qobuz Cover Art
>
> **File:** `&Art#&Qobuz.src` → `Qobuz.inc`
>
> Searches Qobuz for album artwork and extracts the best available image URL from the structured JSON response.
>
> **Search by:** AlbumArtist + Album
>
> ---
>
> #### <img src="https://raw.githubusercontent.com/Arcticons-Team/Arcticons/386408031661cef2ac6e33ab97f57060a952be6f/icons/white/soundcloud.svg" height="18" valign="middle" /> Soundcloud Cover Art
>
> **File:** `&Art#&Soundcloud.src` → `Soundcloud Artwork.inc`
>
> Fetches SoundCloud track or artist artwork by artist name and title, or by direct URL.
>
> </details>

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="actions"></a><strong><a href="#actions"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;ACTIONS</strong>
</summary>

────────

<p align="">
<a href="./Actions/Format/README.md"><strong>FORMAT</strong></a> •
<a href="./Actions/Genre/README.md"><strong>GENRE</strong></a> •
<a href="./Actions/Regex/README.md"><strong>REGEX</strong></a> •
<a href="./Actions/README.md"><strong>MAIN</strong></a> •
<a href="./Actions/Eksternal/README.md"><strong>FILE SAVING</strong></a> •
<a href="./Actions/Eksternal/Disc%20Numbers/README.md"><strong>DISC NUMBERS</strong></a> •
<a href="./Actions/Eksternal/Compilation/README.md"><strong>COMPILATIONS</strong></a> •
<a href="./Actions/Eksternal/Splits/README.md"><strong>SPLITS</strong></a>
</p>


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

> <details>
> <summary><a id="bundled-actions"></a><strong>Bundled Actions</strong> — 38 actions across 5 groups</summary>
>
> | Action | Purpose |
> |---|---|
> | `F - Artist to Album Artist` | Copy `ARTIST` → `ALBUMARTIST` |
> | `F - Case Conversion` | Convert to UPPER / lower / Title Case |
> | `F - Combo` | Combined formatting pass for tags |
> | `F - Combo - Accents` | Combo plus accent stripping |
> | `F - Fix` | General tag fixes (whitespace, separators) |
> | `F - Mixed Case` | Force Mixed Case for standard fields |
> | `F - Move Feat to Title` | Move `feat.` artists from `ARTIST` into `TITLE` |
> | `F - Standard` | Standard formatting pass over common fields |
> | `F - Strip Remaster` | Remove remaster info from `TITLE`/`ALBUM` |
> | `F - Style to Genre` | Promote `STYLE` into `GENRE` |
> | `F - Year` | Normalise `YEAR` formatting |
> | `G - Black Metal` | `Black Metal` |
> | `G - Blackened Death Metal` | `Blackened Death Metal` |
> | `G - Crossover Thrash` | `Crossover Thrash` |
> | `G - Death Metal` | `Death Metal` |
> | `G - Death Thrash` | `Death/Thrash Metal` |
> | `G - Hardcore` | `Hardcore` |
> | `G - Heavy Metal` | `Heavy Metal` |
> | `G - Hip-Hop` | `Hip-Hop` |
> | `G - Thrash Metal` | `Thrash Metal` |
> | `R - Add Apostrophes` | Insert apostrophes in common contractions |
> | `R - English Naming` | Standardise English-language naming conventions |
> | `R - Smart Title Case` | Apply smarter Title Case to `TITLE`/`ALBUM` |
> | `R - Spacing Proper` | Fix spacing around punctuation |
> | `R - Strip Accents` | Strip diacritics from tag values |
> | `R - Trim Extra Space` | Remove leading/trailing/duplicate whitespace |
> | `R - Upper Case Feats` | Uppercase `FEAT.`, `PROD.`, `WITH` in titles |
> | `D - <Genre>` | Genre exports (with `Disc N/` subfolder) |
> | `E - <Genre>` | Genre exports (flat, no `Disc/`) |
>
> </details>

### Importing Actions

All actions are pre-bundled into [`Actions/Action Groups.json`](Actions/Action%20Groups.json) — a single file you can import into Mp3tag in one go.

1. **Actions → Actions…** (`⌥6`) to open the Action Groups window
2. Click the **+** icon at the bottom-left of the sidebar to open its context menu
3. Choose **Import…** and select `Actions/Action Groups.json` from this repo (individual `.mta` files can be imported the same way)

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

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="scripts"></a><strong><a href="#scripts"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;SCRIPTS</strong>
</summary>
────────


One-off setup and maintenance scripts that ship with the repo. None are required for day-to-day Mp3tag use — they exist to make retargeting, syncing, and other bulk edits easier.

**Files:** `Scripts/retarget-paths.py`, `Scripts/layouts.py` (and the top-level wrapper `./configure`)

### Quick Start: `./configure`

```bash
./configure                                   # interactive wizard
./configure --new /Volumes/MyExternal/Music/ --layout standard --json-only --out /tmp/retargeted/ --yes
./configure --list-layouts
./configure --show-layout standard
```

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

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="settings"></a><strong><a href="#settings"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;SETTINGS</strong>
</summary>
────────


Configuration formats used across sources and actions — how settings panels are wired up, the file-naming conventions that tie everything together, and how the `.mta` action format works under the hood.

> <details>
> <summary><a id="settings-system"></a><strong>Settings System</strong></summary>
>
> All sources use Mp3tag's native `.settings` JSON panel system. Settings files follow the naming convention:
>
> ```
> SourceName#Settings….settings
> ```
>
> The `….` (ellipsis `U+2026`) distinguishes settings files from other `.settings` files. Settings are loaded automatically when you open a source's settings dialog and stored persistently in `settings.json`.
>
> </details>

> <details>
> <summary><a id="file-naming-conventions"></a><strong>File Naming Conventions</strong></summary>
>
> | Convention | Meaning |
> |---|---|
> | `&` prefix on a letter | Keyboard shortcut accelerator |
> | `#S` | Tag source entry point (appears in the Tag Sources menu) |
> | `#Settings….` | Settings panel file for a source |
> | `.inc` | Shared include file — not standalone, included by `.src` files |
> | `.src` | Standalone source file |
>
> </details>

> <details>
> <summary><a id="creating--editing-actions"></a><strong>Creating & Editing Actions</strong></summary>
>
> Actions are stored as `.mta` files in the `Actions/` directory. Each file contains one or more action definitions in a numbered INI-like format:
>
> ```ini
> [#0]
> T=1
> F=_ALL
> 1=Feat
> 2=feat
> 3=0
> ```
>
> **Action types**
>
> | Type | Description | Example Use |
> |---|---|---|
> | `T=1` | Replace | Replace `"feat."` with `"ft."` |
> | `T=2` | Replace with Regex | Remove trailing parentheses |
> | `T=3` | Format Value | Set field using placeholders |
> | `T=4` | Guess Values | Parse filename into tags |
> | `T=6` | Remove Fields | Delete specific fields |
> | `T=7` | Remove Fields Except | Keep only specified fields |
> | `T=8` | Merge Duplicate Fields | Combine multiple values |
> | `T=9` | Split Field by Separator | Split field into multiple values |
> | `T=10` | Import Cover from File | Add cover art from file |
> | `T=11` | Export Cover to File | Save cover art to file |
> | `T=13` | Remove Duplicate Fields | Remove duplicate entries |
>
> **Common parameters**
>
> - **`F`**: Field name (e.g. `TITLE`, `ARTIST`, `ALBUM`, `_ALL`)
> - **`1`**: Input string, format pattern, or search string
> - **`2`**: Replacement string or format string
> - **`3`**: Additional parameter (varies by action type)
>
> For detailed documentation, see `Actions/MTA Guide.md` in this repository.
>
> </details>

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="guides"></a><strong><a href="#guides"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;GUIDES</strong>
</summary>
────────

<p align="">
<a href="./Actions/MTA%20Guide.md"><strong>MTA GUIDE</strong></a> •
<a href="https://community.mp3tag.de/c/howto/"><strong>HOWTO</strong></a> •
<a href="https://docs.mp3tag.de/tag-sources/development/"><strong>TAG SOURCES</strong></a> •
<a href="https://docs.mp3tag.de/actions/"><strong>ACTIONS</strong></a> •
<a href="https://docs.mp3tag.de/"><strong>DOCS</strong></a>
</p>


Reference material for extending the repo — building new tag sources from scratch and writing Mp3tag format strings.

> <details>
> <summary><a id="creating-web-sources"></a><strong>Creating Web Sources</strong></summary>
>
> Source files use an INI-like format:
>
> ```ini
> [Name]=Source Name
> [BasedOn]=www.example.com
> [IndexUrl]=https://www.example.com/search/%s
> [AlbumUrl]=https://api.example.com/album/
> [WordSeparator]=%20
> [IndexFormat]=%_preview%|%_url%|%Album%|%Artist%|%Year%
> [SearchBy]=%Artist% %Album%
> [Encoding]=url-utf-8
>
> [ParserScriptIndex]=...
> # Parser script goes here
>
> [ParserScriptAlbum]=...
> # Album parser goes here
> ```
>
> **Key parameters**
>
> | Parameter | Description |
> |---|---|
> | `[Name]` | Display name for the source |
> | `[BasedOn]` | Base website URL |
> | `[IndexUrl]` | Search URL with `%s` placeholder |
> | `[AlbumUrl]` | Album detail URL template |
> | `[IndexFormat]` | Format string for search results |
> | `[SearchBy]` | Fields used for searching |
> | `[ParserScriptIndex]` | Script to parse search results |
> | `[ParserScriptAlbum]` | Script to parse album details |
>
> **Common parser commands**
>
> - `FindLine "text"` — Find a line containing text
> - `RegexpReplace "pattern" "replacement"` — Replace using regex
> - `json "ON" "current"` — Enable JSON parsing
> - `json_select "key"` — Select a JSON field
> - `say "text"` — Output literal text
> - `sayrest` — Output the rest of the current line
>
> For full documentation, see the [Mp3tag Tag Sources documentation](https://docs.mp3tag.de/tag-sources/).
>
> </details>

> <details>
> <summary><a id="mp3tag-scripting"></a><strong>Mp3tag Scripting</strong></summary>
>
> Mp3tag supports scripting functions in format strings, actions, and filters.
>
> **Common functions**
>
> | Function | Description |
> |---|---|
> | `$upper(string)` | Convert to uppercase |
> | `$lower(string)` | Convert to lowercase |
> | `$caps(string)` | Title case |
> | `$replace(string,from,to)` | Replace occurrences |
> | `$regexp(string,pattern,replacement)` | Regex replace |
> | `$if(condition,then,else)` | Conditional |
> | `$trim(string)` | Remove leading/trailing whitespace |
> | `$num(number,length)` | Format number with zero-padding |
> | `$if2(a,b)` | Return `a` if not empty, else `b` |
>
> **Examples**
>
> ```
> $caps(%title%)
> $replace(%artist%, " & ", " and ")
> $if(%albumartist%, %albumartist%, %artist%)
> ```
>
> In an action (`T=3`):
>
> ```ini
> [#0]
> T=3
> F=TITLE
> 1=$caps(%title%)
> ```
>
> For the full reference, see the [Mp3tag Scripting Documentation](https://docs.mp3tag.de/scripting/functions/).
>
> </details>

**[&uarr;](#contents)**

</details>

<details>
<summary>
<a id="faq"></a><strong><a href="#faq"><img src="Assets/Icon/mp3tag-color.png" height="20" valign="middle" /></a>&nbsp;FAQ</strong>
</summary>
────────
<p align="">
<a href="https://community.mp3tag.de/categories"><strong>COMMUNITY</strong></a> •
<a href="https://docs.mp3tag.de/"><strong>DOCS</strong></a> •
<a href="https://www.mp3tag.de/en/index.html"><strong>OFFICIAL</strong></a> •
<a href="https://github.com/deathrashed/mp3tag/issues/new"><strong>ISSUES</strong></a> •
<a href="https://github.com/deathrashed/mp3tag/issues/new"><strong>REQUESTS</strong></a> 
</p>

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

**[&uarr;](#contents)**

</details>

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
