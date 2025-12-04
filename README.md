<div align="center">

# Mp3tag Config

<img src="./.icon/AppIcon.png" alt="Mp3tag Icon" width="120">

</div>

---

## Overview

This repository contains my personal configuration, actions, and source scripts for **Mp3tag** on macOS. Mp3tag is a powerful and user-friendly tool for editing metadata (tags) of audio files. It supports batch tag-editing for various audio formats (MP3, MP4, FLAC, OGG, etc.) and integrates with online databases like Discogs, MusicBrainz, and Deezer to automatically retrieve tags and download cover art.

This configuration is designed to be cloned directly into `~/.config/tools/mp3tag` so that Mp3tag can use these presets out of the box.

### Repository Structure

- **`Actions/`**: Mp3tag action groups (`.mta` files) organized by purpose:
  - `Format/`: Formatting actions (case conversion, date formats, etc.)
  - `Genre/`: Genre-specific actions and mappings
  - `Regex/`: Regex-based text cleaning and normalization
  - `Disc Numbers/`: Disc number formatting actions
  - `Eksternal/`: External/export-related actions
- **`Sources/`**: Web sources and supporting files for metadata lookups:
  - Custom tag sources (`.src` files) for various music databases
  - Include files (`.inc`) with shared functions
  - `Mp3tagSettings/`: Export templates, additional actions, and `mp3tag.cfg`
  - Configuration files: `genres.ini`, `columns.ini`, `settings.json`, etc.
- **`.icon/`**: App icon files used for documentation and launchers

---

## What is Mp3tag?

Mp3tag is a metadata editor for audio files that allows you to:

- **Batch edit tags** for multiple files simultaneously
- **Rename files** based on tag information or vice versa
- **Import tags** from online databases (Discogs, MusicBrainz, Deezer, etc.)
- **Download cover art** automatically from various sources
- **Format and clean** tag values using actions and scripts
- **Support multiple formats**: MP3, MP4, FLAC, OGG, WMA, APE, and more

For more information, visit the [official Mp3tag website](https://www.mp3tag.de/en/) and [documentation](https://docs.mp3tag.de/).

---

## Getting Started with Mp3tag

### Installation

1. **Download**: Get the latest version from the [official website](https://www.mp3tag.de/en/download.html)
2. **Install**: Follow the installation instructions for macOS
3. **Configure**: Point Mp3tag to use this repository's actions and sources

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

---

## Creating and Editing Actions (.mta Files)

Actions are stored as `.mta` files in the `Actions/` directory. Each action file contains one or more action definitions.

### Action File Structure

Action files use an INI-like format with numbered sections. Each action is defined in a `[#N]` section:

```ini
[#0]
T=4
F=_ALL
1=%20
2=
3=0
```

### Action Types (T= codes)

| Type | Description | Example Use |
|------|-------------|-------------|
| `T=1` | Replace | Replace "feat." with "ft." |
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

### Common Action Parameters

- **`F`**: Field name (e.g., `TITLE`, `ARTIST`, `ALBUM`, `_ALL` for all fields)
- **`1`**: Input string, format pattern, or search string
- **`2`**: Replacement string or format string
- **`3`**: Additional parameter (varies by action type)

### Creating a New Action

1. **Create Action File**: Create a new `.mta` file in the appropriate `Actions/` subdirectory
2. **Define Actions**: Add action sections using the format above
3. **Test**: Load the action in Mp3tag and test on sample files
4. **Organize**: Group related actions in the same file

### Example Action File

Here's an example action that replaces spaces with underscores and standardizes "feat.":

```ini
[#0]
T=1
F=_ALL
1=
2=_
3=0

[#1]
T=1
F=_ALL
1=Feat
2=feat
3=0
```

For detailed action type documentation, see `Actions/MTA Guide.md` in this repository.

---

## Creating Web Sources (.src Files)

Web sources allow Mp3tag to fetch metadata from online databases. Source files are stored in the `Sources/` directory.

### Source File Structure

Source files use an INI-like format with sections:

```ini
[Name]=Source Name
[BasedOn]=www.example.com
[IndexUrl]=https://www.example.com/search/%s
[AlbumUrl]=https://api.example.com/album/
[WordSeparator]=%20
[IndexFormat]=%_preview%|%_url%|%Album%|%Artist%|%Year%
[SearchBy]=%Artist% %Album%
[Encoding]=url-utf-8
[UserAgent]=1

[ParserScriptIndex]=...
# Parser script goes here
```

### Key Source Parameters

- **`[Name]`**: Display name for the source
- **`[BasedOn]`**: Base website URL
- **`[IndexUrl]`**: Search URL with `%s` placeholder for search terms
- **`[AlbumUrl]`**: Album detail URL template
- **`[IndexFormat]`**: Format for search results display
- **`[SearchBy]`**: Fields to use for searching
- **`[ParserScriptIndex]`**: Script to parse search results
- **`[ParserScriptAlbum]`**: Script to parse album details

### Parser Script Commands

Parser scripts use commands like:
- `FindLine "text"`: Find a line containing text
- `RegexpReplace "pattern" "replacement"`: Replace using regex
- `json "ON" "current"`: Enable JSON parsing
- `json_select "key"`: Select JSON object/array
- `say "text"`: Output text to result

### Creating a New Web Source

1. **Study Existing Sources**: Look at examples in `Sources/` directory
2. **Create Source File**: Create a new `.src` file
3. **Define URLs**: Set up search and album URLs
4. **Write Parser Script**: Create scripts to parse HTML/JSON responses
5. **Test**: Use Mp3tag's tag source feature to test your source

For more details, see the [Mp3tag Tag Sources documentation](https://docs.mp3tag.de/tag-sources/).

---

## Scripting in Mp3tag

Mp3tag supports scripting functions for advanced tag manipulation. Scripts can be used in format strings, actions, and filters.

### Common Scripting Functions

- **`$upper(string)`**: Convert to uppercase
- **`$lower(string)`**: Convert to lowercase
- **`$caps(string)`**: Title case (capitalize first letter of each word)
- **`$replace(string,from,to)`**: Replace occurrences
- **`$regexp(string,pattern,replacement)`**: Regex replace
- **`$if(condition,then,else)`**: Conditional statement
- **`$trim(string)`**: Remove leading/trailing whitespace
- **`$num(number,length)`**: Format number with padding

### Using Scripts in Format Strings

Scripts can be used in format strings for renaming files or formatting tags:

```
$caps(%title%)
$replace(%artist%, " & ", " and ")
$if(%albumartist%, %albumartist%, %artist%)
```

### Using Scripts in Actions

When creating actions with `T=3` (Format Value), you can use scripting functions in the format string:

```ini
[#0]
T=3
F=TITLE
1=$caps(%title%)
```

For a complete list of scripting functions, see the [Mp3tag Scripting Documentation](https://docs.mp3tag.de/scripting/functions/).

---

## Git Workflow

<details>
<summary><strong>📥 Clone the Repository</strong></summary>

Clone this repository into your Mp3tag configuration directory:

```bash
git clone git@github.com:YOUR_USERNAME/mp3tag.git ~/.config/tools/mp3tag
```

Or if using HTTPS:

```bash
git clone https://github.com/YOUR_USERNAME/mp3tag.git ~/.config/tools/mp3tag
```

</details>

<details>
<summary><strong>🔄 Update to Latest Version</strong></summary>

Pull the latest changes from the remote repository:

```bash
cd ~/.config/tools/mp3tag
git pull
```

Or pull from a specific branch:

```bash
git pull origin edit
```

</details>

<details>
<summary><strong>📊 Check Status</strong></summary>

See what files have been modified:

```bash
cd ~/.config/tools/mp3tag
git status
```

View detailed changes:

```bash
git diff
```

</details>

<details>
<summary><strong>💾 Commit and Push Changes</strong></summary>

Save your local changes (new actions, modified sources, etc.):

```bash
cd ~/.config/tools/mp3tag
git status                    # see what changed
git add .                     # stage all changes
# or add specific files:
git add Actions/Format/F-New.mta
git commit -m "Add new formatting action"
git push
```

Push to a specific branch:

```bash
git push origin edit
```

</details>

<details>
<summary><strong>🌿 Create and Use Feature Branches</strong></summary>

Create a new branch for experimental changes:

```bash
cd ~/.config/tools/mp3tag
git checkout -b feature/new-genre-system
# make your changes to actions/sources
git add .
git commit -m "Add new genre mappings"
git push -u origin feature/new-genre-system
```

Switch between branches:

```bash
git checkout edit              # switch to edit branch
git checkout feature/new-genre-system  # switch back to feature branch
```

</details>

<details>
<summary><strong>🔀 Merge Feature Branch</strong></summary>

Merge a feature branch back into your main branch:

```bash
# switch to target branch
git checkout edit
git pull                      # ensure you're up to date

# merge feature branch
git merge feature/new-genre-system
git push
```

Or merge via GitHub's pull request interface.

</details>

<details>
<summary><strong>↩️ Discard Local Changes</strong></summary>

Reset all local changes to match the remote repository:

```bash
cd ~/.config/tools/mp3tag
git reset --hard HEAD         # discard uncommitted changes
git clean -fd                 # remove untracked files
```

Reset to a specific commit:

```bash
git reset --hard <commit-hash>
```

</details>

<details>
<summary><strong>📋 View Commit History</strong></summary>

View commit history:

```bash
git log --oneline             # compact view
git log                       # detailed view
```

View changes in a specific commit:

```bash
git show <commit-hash>
```

</details>

<details>
<summary><strong>🔍 Search and Find</strong></summary>

Search for text across all files:

```bash
git grep "search term"
```

Find when a file was last modified:

```bash
git log -1 --format="%ai" -- <file-path>
```

</details>

---

## Additional Resources

- **[Mp3tag Official Website](https://www.mp3tag.de/en/)**: Download and general information
- **[Mp3tag Documentation](https://docs.mp3tag.de/)**: Comprehensive user guide
- **[Mp3tag Community Forums](https://community.mp3tag.de/)**: Community support and discussions
- **[Mp3tag Scripting Functions](https://docs.mp3tag.de/scripting/functions/)**: Complete scripting reference
- **[Mp3tag Tag Sources](https://docs.mp3tag.de/tag-sources/)**: Guide to creating custom tag sources

---

## Notes

- **macOS Paths**: These presets assume macOS paths and a Mp3tag setup that reads from `~/.config/tools/mp3tag`
- **Personal Toolkit**: This repository is a personal toolkit tailored to specific tagging workflows, genre schemes, and external services
- **Version Control**: When you add or modify actions (`.mta`) or web sources (`.src`/`.inc`), commit and push to keep your configuration versioned and portable
- **Icon Path**: The Mp3tag icon is located at `./.icon/AppIcon.png` for proper display in this README

---

## License / Personal Use

This repository represents a **personal toolkit** for managing and tagging audio files. Feel free to fork and adapt it to your needs, but be aware that some actions and sources may be tailored to specific workflows, genre schemes, and external services.
