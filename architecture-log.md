# architecture-log.txt
<!-- CODING AGENT EDITION — do not add sections, do not rename sections, do not modify rules -->

---

## [1] CURRENT ARCHITECTURE STATE

**Repo:** `vocab-explorer/` — standalone Electron app, independent of existing `my-new-app` 4-LLM repo.

**Directory layout:**
```
vocab-explorer/
├── package.json          — main: src/main.js, start: nodemon --exec electron .
├── node_modules/
├── data/                 — all CSV and Python pipeline scripts
│   ├── merged_learning.csv   — primary ranked dataset (10k entries, learning_rank as sort axis)
│   ├── merged.csv            — base merge without learning_score (default load target)
│   ├── wordfreq_10k.csv
│   ├── subtitles_10k.csv
│   ├── oxford_raw.csv        — CEFR-J source (A1–B2, ~6863 rows)
│   ├── oxford5k_raw.csv      — Oxford 5k source (A1–C1, with voice_url)
│   ├── cmu_raw.txt           — CMU phonetic dict, unjoined
│   └── *.py                  — pipeline scripts
├── app-data/             — user state lives here (portable, pre-created at boot)
└── src/
    ├── main.js           — Electron main process: loads CSV via fs, exposes via ipcMain.handle('get-entries')
    ├── preload.js        — contextBridge exposes window.api.getEntries()
    └── renderer/
        ├── index.html    — app shell, page-input nav box
        ├── index.js      — allEntries[], currentBlock, renderList(), BLOCK_SIZE=100
        └── style.css     — dark mode (#000 bg), grid-based column alignment
```

**Active patterns:**
- Main process owns all file I/O. Renderer is read-only display layer. Communication is IPC only via preload bridge — no `nodeIntegration: true`.
- CSV parse in main process handles quoted fields (e.g. `"infinitive-to, preposition"`) with a character-by-character quote-aware parser.
- UI navigation: single `#page-input` number box, Enter key triggers `jumpToBlock()`. Scroll-direction is reversed (down = higher rank).
- Column layout uses `display: grid` with `grid-template-columns: 40px 140px 1fr 72px 72px 72px` in both `.col-header` and `.word-row` — ensures alignment is window-width-invariant.
- Zipf badges are colored by `Math.floor(zipf)`: 7=amber, 6=teal, 5=blue-gray, 4=muted purple, 3=gray.
- CEFR badges use dark-mode color pairs (background + text + border) per level A1–C2.

**Locked (must not refactor):**
- `app.setPath('userData', path.join(__dirname, '..', 'app-data'))` — portability: user state must travel with repo, not stay in Windows AppData.
- `entries[id]` as primary key format `{source}_{rank_padded}` — surrogate key decouples progress from word string identity; changing this breaks all existing progress records.
- IPC-only renderer communication — security boundary; do not add `nodeIntegration: true`.

---

## [2] CAUSAL SPINE

Started from a completed multi-source corpus pipeline (`merged_learning.csv` with wf_zipf, sub_zipf, ox_cefr, learning_score), forced to define user-state schema before building UI because ChatGPT's adversarial review identified that `words[word]` as primary key silently corrupts progress on dataset rebuild — pivoted to `entries[id]` surrogate key. Currently at a running Electron scaffold with dark-mode list display and page navigation, with tick-completion and `session_state.json` write logic unbuilt, and Oxford source comparison (CEFR-J vs Oxford 5k) unresolved.

---

## [3] FORBIDDEN PATHS

- **Integrating vocab-explorer into existing `my-new-app` Electron repo** → failed because the existing repo is a stateless interface layer and vocab-explorer requires persistent data state; merging would require full state management refactor of the older repo at disproportionate cost. Do not revisit.
- **`words[word]` as session_state.json primary key** → failed because word strings are not stable across dataset rebuilds and are non-unique across domain packs and proper noun variants. Do not revisit.
- **Block-nav button array (one button per 100-word range)** → failed because 10k entries produces 100 buttons simultaneously rendered, which is unusable. Replaced by single page-input box. Do not revisit.

---

## [4] ACTIVE TENSIONS

1. **Tick completion unbuilt.** `app-data/` directory exists and is writable. `session_state.json` schema is designed (`entries[id]` with `learned`, `learned_at`, `flags`, `notes`) but no write logic exists yet. Next coding task.

2. **Write queue not implemented.** Gemini identified concurrent async write risk for rapid tick interactions. Pattern designed (pending + flush) but not in codebase. Must be added before tick completion goes live.

3. **Oxford source unresolved.** Diff script written but not yet run. Until `diff_label_conflict.csv` is read, it is unknown whether CEFR-J and Oxford 5k contradict each other systematically. This affects which source gets used in the next `merged_learning.csv` rebuild.

4. **`voice_url` unjoined.** Oxford 5k source contains direct `.ogg` links to Oxford pronunciation audio. Column exists in `oxford5k_raw.csv` but has not been merged into `merged_learning.csv`. Audio play button in UI is unbuilt.

---

## [5] DECISION LOG

- **Standalone repo for vocab-explorer** — existing `my-new-app` is a stateless interface layer; merging a stateful data app into it would require full state management refactor at disproportionate cost.
- **`entries[id]` surrogate key with format `{source}_{rank_padded}`** — word strings are not stable across dataset rebuilds and are non-unique across domain variants; surrogate key decouples progress tracking from surface identity.
- **`app.setPath('userData')` overridden to `app-data/` inside repo** — default Windows AppData path is machine-local; override makes the repo self-contained and portable.
- **IPC-only renderer communication via contextBridge** — `nodeIntegration: true` is a security boundary violation in Electron; all file I/O stays in main process.
- **`display: grid` for row and header alignment** — `flex` with `flex: 1` on `.pos` caused column drift on window resize; grid with fixed column template is window-width-invariant.
