# index_map.md
<!-- SPATIAL NAVIGATION EDITION — do not add sections, do not rename sections, do not modify rules -->

---

## [DISPATCH]

data pipeline → ZONE_DATA
user state / progress / tick → ZONE_STATE
renderer / UI / display / list → ZONE_RENDERER
main process / IPC / file read → ZONE_MAIN
styles / dark mode / colors / CSS → ZONE_STYLE
oxford / CEFR / source comparison → ZONE_OXFORD
audio / voice / pronunciation → ZONE_AUDIO
schema / session_state / entries → ZONE_STATE

---

## [ZONES]

ZONE_DATA
PATH: vocab-explorer/data/
ROLE: All source CSVs and Python pipeline scripts — immutable input layer
SIGNAL: STABLE
NOTE: merged_learning.csv is current display source; merged.csv is base merge without learning_score; both are outputs of Python pipeline, not hand-edited
CS: 0.85

ZONE_STATE
PATH: vocab-explorer/app-data/session_state.json
ROLE: User progress store — learned status, timestamps, flags per entry
SIGNAL: CRITICAL
NOTE: File does not exist yet — unbuilt. Schema designed (entries[id] surrogate key) but no write logic in codebase. Next immediate build target.
CS: 0.0

ZONE_RENDERER
PATH: vocab-explorer/src/renderer/
ROLE: Display layer — renders entry list, handles page navigation, shows badges
SIGNAL: HIGH
NOTE: Grid column alignment implemented; tick-completion UI not yet added; audio play button not yet added
CS: 0.75

ZONE_MAIN
PATH: vocab-explorer/src/main.js
ROLE: Electron main process — file I/O, CSV parse, IPC handler, userData path override
SIGNAL: STABLE
NOTE: CSV parser is quote-aware (handles fields like "infinitive-to, preposition"); app-data/ pre-created at boot to prevent Windows cache permission error
CS: 0.90

ZONE_STYLE
PATH: vocab-explorer/src/renderer/style.css
ROLE: Visual layer — dark mode palette, zipf color scale, CEFR badge colors
SIGNAL: STABLE
NOTE: Zipf color by Math.floor(zipf): 7=amber #e2c97e, 6=teal #7eb8a0, 5=blue-gray #7a9cbf, 4=purple #8a7aaa, 3=gray #666; scroll-direction reversal via CSS spinner transform
CS: 0.80

ZONE_OXFORD
PATH: vocab-explorer/data/oxford_raw.csv + vocab-explorer/data/oxford5k_raw.csv
ROLE: CEFR label sources — CEFR-J (A1–B2) vs Oxford 5k (A1–C1)
SIGNAL: HIGH
NOTE: Diff script written but not yet run. Four output files pending: only_cefrj, only_ox5k, label_conflict, label_same. Source selection unresolved until diff is read.
CS: 0.60

ZONE_AUDIO
PATH: vocab-explorer/data/oxford5k_raw.csv (voice_url column)
ROLE: Pronunciation audio source — direct .ogg links to Oxford CDN
SIGNAL: HIGH
NOTE: voice_url exists in oxford5k_raw.csv but not yet joined into merged_learning.csv; audio play button in renderer unbuilt; no TTS needed
CS: 0.40

---

## [UNKNOWN]

vocab-explorer/data/cmu_raw.txt — CMU phonetic dict downloaded, schema known (word + phoneme string), but join logic to merged_learning.csv not designed and use case (IPA display, syllable count, minimal pairs) not committed to
