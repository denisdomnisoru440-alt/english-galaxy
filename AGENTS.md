# English Galaxy — Project Guide

## Project Structure

- `vocab.html` — Main SPA app (English vocabulary learning)
- `serve_vocab.py` — HTTP server on port 8080 for local network access
- `galaxy_app.py` — Opens vocab.html in browser
- `galaxy.spec` — PyInstaller config for building EnglishGalaxy.exe
- `galaxy_tutor.html` — Interactive tutorial explaining the code
- `english_c2_vocabulary/` — Separate JSON word files by level (A1-C2, Dota2, Grammar)

## Code Conventions (vocab.html)

- All JS is in a single `<script>` tag at the end of the file
- Variables are declared with `var` (ES5 style)
- Global data: `G` array holds all categories, each with `{id, words[]}`
- CSS uses dark theme as default, `.light` class for light theme
- No external dependencies or libraries

## Safe localStorage Helpers

Use these instead of raw localStorage calls:

- `lsGet(k, def)` — safe getItem
- `lsSet(k, v)` — safe setItem
- `lsGetObj(k, def)` — safe JSON.parse getItem
- `lsSetObj(k, v)` — safe JSON.stringify setItem
- `lsRemove(k)` — safe removeItem

## Category Lookup

- `getCat(id)` — find category by id in G array
- `getGrammarCat()` — shortcut for `getCat('Grammar')`

Do NOT use hardcoded indices like `G[8]` — always use `getCat('Grammar')`.
