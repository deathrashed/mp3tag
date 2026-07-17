# Splits

Save actions for split releases on the **Eksternal** library. Each action writes the selected split into a `-Splits-` folder under the matching genre and exports the embedded front cover.

Splits are stored with the format:

```
/Volumes/Eksternal/Audio/<Genre>/-Splits-/<Album Artist>/[<Year> - ]<Album>/<Track#>. <Artist> - <Title>
```

The track filename uses `<Artist> - <Title>` because the artist varies per track on a split. The album path is keyed on `<Album Artist>` (not `<Artist>`) so all bands on the split live under one folder.

## Actions

| File | What it does |
| --- | --- |
| `S - Electronic - Split.mta` | Saves the selected split into the **Electronic** Eksternal collection under `-Splits-` and exports the front cover. |
| `S - Hip-Hop - Split.mta` | Saves the selected split into the **Hip-Hop** Eksternal collection under `-Splits-` and exports the front cover. |
| `S - Metal - Split.mta` | Saves the selected split into the **Metal** Eksternal collection under `-Splits-` and exports the front cover. |
| `S - Miscellaneous - Split.mta` | Saves the selected split into the **Misc** Eksternal collection under `-Splits-` and exports the front cover. |
| `S - Punk & Hardcore - Split.mta` | Saves the selected split into the **Punk & Hardcore** Eksternal collection under `-Splits-` and exports the front cover. |
| `S - Rock & Grunge - Split.mta` | Saves the selected split into the **Rock & Grunge** Eksternal collection under `-Splits-` and exports the front cover. |

## Files

- `Splits.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each save action.
