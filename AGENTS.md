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

## Navigation Tabs

5 tabs: Browse, Quiz, Games, Grammar, Me. `switchTab(tab)` handles routing. Games tab: `renderGames()`.

## XP & Gamification

- `getXP()`, `getLevel()`, `getLevelName()`, `addXP(n)` — XP system (100 XP per level, 11 levels)
- `ACHIEVEMENTS[]` — 13 achievements, `checkAchievements()` auto-unlocks
- `getDailyChallenges()` — 3 daily challenges with XP rewards
- Sound effects: `playSound(type)` — correct, wrong, click, levelup, achieve, flip, match
- `spawnConfetti(n)` — canvas particle animation
- `scoreFly(el, text, color)` — floating XP popup on correct answer

## Mini-Games

4 games on Games tab: Memory, Match Words, Guess Word, Typing. Each `start*Game()` renders into `#games`. XP awarded per game.

## Spaced Repetition (SRS)

- `scheduleWord(word, group, quality)` — schedule next review (Again=0, Hard=1, Good=2, Easy=3)
- Intervals: 1d → 3d → 7d → 14d → 30d → 60d → 120d
- `startSRSReview(catId)` — review due words from a category
- SRS auto-integrated: `saveQuizResult` override schedules words after quiz
- Games page shows Due/Learned/New counts per category

## Git Remotes & Deployment

- `origin` = GitLab, `github` = GitHub
- GitLab CI: `.gitlab-ci.yml` copies `vocab.html` → `public/index.html`
- GitHub Pages: serves `index.html` from `master` branch
- SW cache: `eg-cache-v6` (network-first strategy)
