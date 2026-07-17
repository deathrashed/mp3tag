# Additional Regex

Extended regex-driven text normalization and cleanup actions. Each action is a sequence of `replace` / `regexp` / `caseconv` steps that fix a specific class of tagging issue across `_TAG` (every tag), `_ALL` (every field), or targeted fields like `TITLE`, `ARTIST`, `ALBUM`, `GENRE`.

## Actions

### Whitespace & formatting

| File | What it does |
| --- | --- |
| `R - Clean Whitespace.mta` | Strips tab / CR / LF characters, collapses repeated whitespace, and trims leading/trailing whitespace from every tag. |
| `R - Trim Extra Space.mta` | Trims leading/trailing whitespace and collapses runs of internal whitespace to a single space across all tags. |
| `R - Remove Parentheses.mta` | Removes `(...)` content and surrounding whitespace from `TITLE`, `ARTIST`, `ALBUM`. |
| `R - Remove Square Brackets.mta` | Removes `[...]` content and surrounding whitespace from `TITLE`, `ARTIST`, `ALBUM`. |
| `R - Remove Trailing Info.mta` | Strips trailing `(Live)`, `(Remix)`, `(feat. ...)`, `- Live/Remix/...`, and `[...]` suffixes from `TITLE`. |
| `R - Normalize Separators.mta` | Replaces `&` / `,` / `-` / `/` in `ARTIST` and `GENRE` with `;` for consistent multi-value separators. |
| `R - Add Apostrophes.mta.txt` | Adds missing apostrophes to common contractions (`dont` → `don't`, `thats` → `that's`, `lets` → `let's`). Note: filename has the `.mta.txt` extension (and a typo variant `R - Add Apostropies` exists alongside it). |
| `R - Add Apostropies` | Duplicate of the above with a typo in the filename. Intentionally excluded from `Additional Regex.json`. |

### Spelling & casing

| File | What it does |
| --- | --- |
| `R - Fix Common Typos.mta` | Replaces common typos across all fields (`teh` → `the`, `adn` → `and`, `recieve` → `receive`, `seperate` → `separate`, `occured` → `occurred`, `definately` → `definitely`, etc.). |
| `R - Fix Abbreviations.mta` | Uppercases abbreviations and short caps (`tv`, `dj`, `mc`, `ufo`, `cia`, `fbi`, `nasa`, `ep`, `lp`, `uk`, `us`, etc.) when used as standalone words. |
| `R - Fix Contractions.mta` | Normalizes contractions: `don't`, `it's`, `that's`, `won't`, `should've`, `they'll`, `we're`, `I'd`, etc. Handles `feat.` / `ft.` / `featuring` too. |
| `R - Fix Roman Numerals.mta` | Normalizes Roman numerals in track/sequel names (`Ii` → `II`, `Iii` → `III`, `Iv` → `IV`, etc.). |
| `R - English Naming.mta` | Fixes capitalization of English-style name patterns: `O'[...]` (not `O'e[...]`), `Mc[...]`, `Mac[bdfgln]`, `DeMarco` / `DeSyl`. |
| `R - Smart Title Case.mta` | Lowercases minor words (`a`, `the`, `of`, `for`, `as`, `at`, `an`, `by`, `off`, `on`, `from`, `in`, `to`, `and`, `with`, `or`, `nor`, `von`, `de`) unless preceded/followed by delimiters; uppercases the letter after a leading apostrophe. |
| `R - Upper Case Feats.mta` | Uppercases abbreviations and `DJ` / `MC` / `Vs` patterns and Roman numerals. |

### Accent stripping

| File | What it does |
| --- | --- |
| `R - Spacing Proper.mta` | Strips all diacritics and accents from `a-zA-Z` (50 steps, one character class per source letter pair). |
| `R - Strip Accents.mta` | Same accent-stripping pipeline as `Spacing Proper`. |

## Files

- `Additional Regex.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each regex action.

## Notes

- `R - Add Apostrophes.mta.txt` and `R - Add Apostropies` are both kept in this folder for reference but are **excluded** from `Additional Regex.json` (one has the wrong extension, the other is a typo-duplicate of the same content).
- `R - Spacing Proper.mta` and `R - Strip Accents.mta` contain the same accent-stripping pipeline (50 character-class replacements each) and appear both here and in the top-level `Regex/` folder.
