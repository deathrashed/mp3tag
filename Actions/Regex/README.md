# Regex

Regex-driven text normalization and cleanup actions. Each action is a sequence of `replace` / `regexp` / `caseconv` steps that fix common tagging issues across `_TAG` (every tag), `_ALL` (every field), or specific fields like `TITLE`, `ARTIST`, `ALBUM`.

## Top-level actions

| File | What it does |
| --- | --- |
| `R - English Naming.mta` | Fixes capitalization of English-style name patterns: `O'[...]` (not `O'e[...]`), `Mc[...]`, `Mac[bdfgln]`, `DeMarco` / `DeSyl`. |
| `R - Smart Title Case.mta` | Lowercases minor words (a, the, of, for, as, at, an, by, off, on, from, in, to, and, with, or, nor, von, de) unless preceded/followed by delimiters; uppercases the letter after a leading apostrophe. |
| `R - Spacing Proper.mta` | Strips all diacritics and accents from `a-zA-Z` (50 steps, one character class per source letter pair). |
| `R - Strip Accents.mta` | Same accent-stripping pipeline as `Spacing Proper`. |
| `R - Trim Extra Space.mta` | Trims leading/trailing whitespace and collapses runs of internal whitespace to a single space across all tags. |
| `R - Upper Case Feats.mta` | Uppercases abbreviations and `DJ` / `MC` / `Vs` patterns and Roman numerals. |

## Subfolders

| Folder | What it does |
| --- | --- |
| `Additional Regex/` | Extended regex library. Includes `R - Add Apostrophes`, `R - Clean Whitespace`, `R - Fix Abbreviations`, `R - Fix Common Typos` (teh→the, recieve→receive, …), `R - Fix Contractions` (don't, it's, …), `R - Fix Roman Numerals` (II/III/IV/…), `R - Normalize Separators` (`,`/`&`/`-` → `;` in ARTIST/GENRE), `R - Remove Parentheses`, `R - Remove Square Brackets`, `R - Remove Trailing Info` (strips `(Live)`, `(Remix)`, `(feat. ...)`, `[...]` suffixes from TITLE), and the accent/case rules from the top level. See `Additional Regex/Additional Regex.json` for the full list. |

## Files

- `Regex.json` — full action group as a single mp3tag-compatible JSON array.
- `*.mta` — individual mp3tag action scripts for each top-level regex action.

## Notes

- Two files in the repo have a typo: `R - Add Apostropies` (no extension) and `R - Add Apostrophes.mta.txt`. They are duplicates of each other; the canonical version should be `R - Add Apostrophes.mta`. Both are kept here for reference and were intentionally excluded from the JSON conversion.
- `R - Spacing Proper.mta` and `R - Strip Accents.mta` contain the same accent-stripping pipeline (50 character-class replacements each).
