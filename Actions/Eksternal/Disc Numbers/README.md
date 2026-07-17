# Disc Numbers

Save actions for the **Eksternal** library layout with optional `Disc N/` subfolders. Use these for multi-disc releases where tracks need to be grouped under a per-disc folder.

Destination template:

```
/Volumes/Eksternal/Audio/<Genre>/<First Letter>/<Album Artist>/[<Year> - ]<Album>/[Disc N/]<Track#>. <Title>
```

The `Disc N/` segment is only inserted when `DISCNUMBER` is populated on the file.

## Actions

| File | What it does |
| --- | --- |
| `D - Electronic.mta` | Saves the selected album into the **Electronic** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |
| `D - Hip-Hop.mta` | Saves the selected album into the **Hip-Hop** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |
| `D - Metal.mta` | Saves the selected album into the **Metal** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |
| `D - Miscellaneous.mta` | Saves the selected album into the **Miscellaneous** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |
| `D - Punk & Hardcore.mta` | Saves the selected album into the **Punk & Hardcore** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |
| `D - Rock & Grunge.mta` | Saves the selected album into the **Rock & Grunge** Eksternal collection path with optional `Disc N/` subfolders and exports the front cover. |

The actions also include a nested `Compilation` group for the same layout with `-Compilations-` and `Disc N/` combined — see `Disc Numbers.json` for the full structure.

## Files

- `Disc Numbers.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each save action.
