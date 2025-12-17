Here’s a complete breakdown of all known Mp3tag action types (`T=` codes) with **realistic `.mta` examples** for each — including how the `F`, `1`, `2`, and other parameters are used. 

---

## Mp3tag Action Types with Examples

### `T=1` — Replace
Replaces a string in a field.

```ini
T=1
F=TITLE
1=feat.
2=ft.
```
- `F`: Field to modify
- `1`: Search string
- `2`: Replacement string

---

###  `T=2` — Replace with Regular Expression
Uses regex to match and replace.

```ini
T=2
F=ARTIST
1=\s+\(.*?\)$
2=
```
- Removes trailing parentheses like “Artist (Live)”

---

###  `T=3` — Format Value
Sets a field to a new value using placeholders.

```ini
T=3
F=ALBUM
1=Greatest Hits - %YEAR%
```

---

###  `T=5` — Format Value (same as T=3)
Used interchangeably with `T=3`.

```ini
T=5
F=ALBUMARTIST
1=%ARTIST%
```

---

###  `T=4` — Guess Values
Parses a string into fields using a format string.

```ini
T=4
F=FILENAME
1=%TRACK% - %ARTIST% - %TITLE%
```
- Extracts tags from filename structure.

---

###  `T=6` — Remove Fields
Deletes specific fields.

```ini
T=6
F=COMMENT
```

---

###  `T=7` — Remove Fields Except
Keeps only specified fields, deletes all others.

```ini
T=7
F=ARTIST;TITLE;ALBUM;TRACK
```

---

###  `T=8` — Merge Duplicate Fields
Combines multiple values into one.

```ini
T=8
F=GENRE
1= /
```
- Merges multiple genres into one using ` / ` as separator.

---

###  `T=9` — Split Field by Separator
Splits a field into multiple values.

```ini
T=9
F=GENRE
1= /
```
- Opposite of `T=8`.

---

###  `T=10` — Import Cover from File

```ini
T=10
1=cover.jpg
```

---

###  `T=11` — Export Cover to File

```ini
T=11
1=folder.jpg
```

---

###  `T=12` — Set Cover Properties

```ini
T=12
1=3
2=Front Cover
```
- `1`: Cover type (e.g., 3 = Front Cover)
- `2`: Description

---

###  `T=13` — Remove Duplicate Fields

```ini
T=13
F=GENRE
```

---

###  `T=14` — Import Text File

```ini
T=14
1=tags.txt
```

---

###  `T=15` — Export

```ini
T=15
1=export.cfg
```

---

##  Notes on Parameters

| Param | Meaning                              |
|-------|--------------------------------------|
| `F`   | Field name (e.g., `TITLE`, `ARTIST`) |
| `1`   | Input string, format, or search      |
| `2`   | Replacement or format string         |

Some actions (like `T=6`, `T=10`, `T=14`) don’t use `F` because they act on files or global state.

---

Would you like a Typinator snippet scaffold that lets you insert these with field prompts and examples? I can also bundle these into a `.typubset` or CSV-ready format for your clipboard pipeline.