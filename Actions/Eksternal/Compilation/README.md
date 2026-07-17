# Compilation

Save actions for compilation albums on the **Eksternal** library. Each action writes the selected compilation into a `-Compilations-` folder under the matching genre and exports the embedded front cover.

Compilations are stored with the format:

```
/Volumes/Eksternal/Audio/<Genre>/-Compilations-/[<Year> - ]<Album>/<Track#>. <Artist> - <Title>
```

The track filename uses `<Artist> - <Title>` (not just `<Title>`) because the artist varies per track on a compilation.

## Actions

| File | What it does |
| --- | --- |
| `C - Electronic - Compilation.mta` | Saves the selected compilation into the **Electronic** Eksternal collection under `-Compilations-` and exports the front cover. |
| `C - Hip-Hop - Compilation.mta` | Saves the selected compilation into the **Hip-Hop** Eksternal collection under `-Compilations-` and exports the front cover. |
| `C - Metal - Compilation.mta` | Saves the selected compilation into the **Metal** Eksternal collection under `-Compilations-` and exports the front cover. |
| `C - Miscellaneous - Compilation.mta` | Saves the selected compilation into the **Miscellaneous** Eksternal collection under `-Compilations-` and exports the front cover. |
| `C - Punk & Hardcore - Compilation.mta` | Saves the selected compilation into the **Punk & Hardcore** Eksternal collection under `-Compilations-` and exports the front cover. |
| `C - Rock & Grunge - Compilation.mta` | Saves the selected compilation into the **Rock & Grunge** Eksternal collection under `-Compilations-` and exports the front cover. |

## Files

- `Compilations.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each save action.
