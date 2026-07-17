# Eksternal

Save actions for the **Eksternal** library on the `/Volumes/Eksternal/Audio/` external drive. These actions write `_FILENAME` so the selected files land in the right genre folder, then export the embedded front cover to `cover.jpg` in the album directory.

## Top-level actions

Save actions for a standard album. No disc-number subfolders.

| File | What it does |
| --- | --- |
| `E - Electronic.mta` | Saves the selected album into the **Electronic** Eksternal collection path and exports the front cover. |
| `E - Hip-Hop.mta` | Saves the selected album into the **Hip-Hop** Eksternal collection path and exports the front cover. |
| `E - Rock & Grunge.mta` | Saves the selected album into the **Rock & Grunge** Eksternal collection path and exports the front cover. |
| `E - Punk & Hardcore.mta` | Saves the selected album into the **Punk & Hardcore** Eksternal collection path and exports the front cover. |
| `E - Metal.mta` | Saves the selected album into the **Metal** Eksternal collection path and exports the front cover. |
| `E - Miscellaneous.mta` | Saves the selected album into the **Miscellaneous** Eksternal collection path and exports the front cover. |

All six use a destination template of the form:

```
/Volumes/Eksternal/Audio/<Genre>/<First Letter>/<Album Artist>/[<Year> - ]<Album>/<Track#>. <Title>
```

The first-letter subfolder is the first character of the album artist, with a `T` prefix stripped from bands that begin with "The" (e.g. "The Beatles" → `B/Beatles/`).

## Subfolders

| Folder | What it does |
| --- | --- |
| `Disc Numbers/` | Same as the top-level `E -` actions, but adds an optional `Disc N/` subfolder before the track number for multi-disc releases. |
| `Compilation/` | Saves compilations into a `-Compilations-` folder under each genre; tracks are named `<Track#>. <Artist> - <Title>` since the artist varies per track. |
| `Splits/` | Saves split releases into a `-Splits-` folder; tracks are named `<Track#>. <Artist> - <Title>` and the album path is keyed on the album artist. |

## Files

- `Eksternal.json` — full action group as a single mp3tag-compatible JSON array (matches the top-level group structure used in `Action Groups.json`).
- `*.mta` — individual mp3tag action scripts for each save action.
