# Genre

One-click `GENRE` tag setters. Each action rewrites the `GENRE` field on the selected files to a single, controlled value so the library stays consistent.

## Top-level actions

| File | What it does |
| --- | --- |
| `G - Black Metal.mta` | Sets `GENRE` to `Black Metal`. |
| `G - Blackened Death Metal.mta` | Sets `GENRE` to `Blackened Death Metal`. |
| `G - Crossover Thrash.mta` | Sets `GENRE` to `Crossover; Thrash Metal` (compound value). |
| `G - Death Metal.mta` | Sets `GENRE` to `Death Metal`. |
| `G - Death Thrash.mta` | Sets `GENRE` to `Death/Thrash; Death Metal; Thrash Metal` (compound value). |
| `G - Hardcore.mta` | Sets `GENRE` to `Hardcore`. |
| `G - Heavy Metal.mta` | Sets `GENRE` to `Heavy Metal`. |
| `G - Hip-Hop.mta` | Sets `GENRE` to `Hip-Hop`. |
| `G - Thrash Metal.mta` | Sets `GENRE` to `Thrash Metal`. |

## Subfolders

| Folder | What it does |
| --- | --- |
| `Additional Genres/` | Extended list of 60+ genre presets (Alternative, Atmospheric, Avantgarde, Beatdown, Blackened Punk, Brutal Death Metal, Crossover, Death, Deathgrind, Djent, Doom, Experimental, Folk, Funeral Doom, Grindcore, Groove Metal, Grunge, Hard Rock, Hardcore Punk, Hip-Hop; Trap, Horrorcore, Indie Rock, Industrial, Melodic Death Metal, Metal, Metallic Hardcore, New Wave, Nu Metal, Power Metal, Progressive, Psytance, Punk, Slamming Brutal Death Metal, Sludge Metal, Speed Metal, Stoner Metal, Symphonic Metal, Technical, etc.). See `Additional Genres/Additional Genres.json` for the full list. |

## Files

- `Genre.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each top-level genre preset.
