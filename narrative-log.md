**[1] WHO**

The orchestrator thinks by collecting raw material first and resisting interpretation until the material forces it — he will spend hours gathering sources, normalizing schemas, and deferring judgment rather than committing early to a framework that might be wrong. His cognitive signature is a distrust of premature closure paired with an unusual patience for staying in the exploratory phase without anxiety. The bias that shows up most consistently is a preference for letting the data speak before imposing structure — he asked "what does wordfreq actually have?" before deciding whether to use it, asked "what does CMU actually contain?" before deciding whether to keep it. He also carries a calibrated instinct for when a system has reached diminishing returns, which is why he named "tâm trí hết idea để mổ thêm" not as frustration but as a clean signal to stop.

---

**[2] WHAT HAPPENED**

The session opened with a simple question about building a frequency table for common English words, and the belief at the start was that the main challenge was finding the right single source. That belief dissolved within the first hour when the distinction between wordfreq (balanced corpus), OpenSubtitles (spoken English), and Oxford (editorial classification) made it clear that no single source was right — each was right about a different dimension of the same question. The session then became about building a schema that could hold all three dimensions simultaneously rather than collapsing them into one.

The first artifact was `merged.csv` — a join of three sources with rank, frequency percentage, and Zipf score preserved independently for each corpus. The discovery that Zipf scores from the subtitles file were secretly borrowed from wordfreq forced a recalculation, and the corrected data revealed the first meaningful signal: "you" had a higher sub_zipf than wf_zipf, confirming spoken bias in a way raw rank could not.

The second phase was mathematical. Starting from a naive absolute rank difference, the session worked through a series of formula proposals — Priority Score from Gemini, delta/avg_zipf from Claude, magnitude penalty with free parameters — stress-testing each against concrete examples like `unto` vs `deal` and `connection` vs `boss`. Each formula failed in a specific way that forced the next. The session converged on `|wf_zipf - sub_zipf| / avg_zipf²` not because it was theoretically elegant but because it was the only formula that produced no free parameters while correctly ordering all test cases.

The final artifact `merged_learning.csv` revealed two emergent tiers that no one designed: a "cement" layer of structural words at the top, and a "brick" layer of culturally survivable words immediately below — a distinction that ChatGPT named "cultural survivability" and that held up across all three LLMs without prompting.

---

**[3] WHERE IT BROKE**

The stance that collapsed was the assumption that a single ranking formula could encode three independent dimensions — commonness, cross-corpus agreement, and word type. The evidence that destroyed it was `elbow` floating to rank 2010 despite wf_rank 9037, and `unto` sitting next to `deal` despite being a near-obsolete preposition. What replaced the destroyed belief was not a better formula but a cleaner boundary: the formula can encode two dimensions (commonness and agreement), and the third dimension (word type — proper noun, domain-specific, common word) is not computable from corpus data alone. That third dimension was named and set aside deliberately, not abandoned.

---

**[4] WHAT REMAINS UNRESOLVED**

The proper noun problem sits quietly in every range of the learning table. `adam`, `george`, `michael`, `jesus` all score well because they are balanced across corpora — but they are not vocabulary to be learned, they are names to be recognized. There is no column in the current schema that distinguishes them, and filtering them requires either a named-entity tagger or manual curation. The mechanism is invisible by design: the formula has no way to know that a lowercase string is a proper noun unless told.

The domain divergence beyond rank 500 is named but unbuilt. The data supports the claim that past a certain threshold, a single ranked list stops being useful and domain packs become necessary — but no domain pack exists yet, and the boundary where cultural survivability ends and domain specificity begins has not been measured, only intuited.

CMU phonetic data sits in `cmu_raw.txt` with no integration path yet. It holds syllable count, stress position, and rhyme group as future metadata, but the join logic has not been designed and the use case (pronunciation-aware flashcards, minimal pair drills) has not been committed to.

---

**[5] WHAT WAS LEARNED — AND AT WHAT COST**

The lesson that changed behavior most durably: **defer source commitment until the schema can hold multiple sources simultaneously**. The early instinct to pick one source and go deep would have produced a cleaner pipeline and a worse dataset. The cost of learning this was zero in this session because the multi-source design was chosen before any single source was over-invested in.

The second durable lesson: **free parameters are a smell**. Every formula that required an α, an n, or a manually chosen ceiling (7.5) eventually broke on an edge case that forced parameter re-tuning. The formula that survived had no free parameters — the mathematics self-regulated through the properties of the log scale. The cost was one full cycle of formula iteration before this property became visible.

The third lesson, emerging from the closing conversation: **knowing when the design phase is complete is itself a skill**. The signal was not external — no test failed, no deadline hit — it was internal: the orchestrator noticed that no new angles were presenting themselves and named that as the stopping condition. That metacognitive move is rarer than it looks.

---

**[6] METAPHOR ANCHOR**

A cartographer who spent the day triangulating three different maps of the same territory — each drawn by a different expedition, each biased by the route they took — and produced not one authoritative map but a transparent overlay where the disagreements between maps are themselves the most useful information.

---

[2026-06-08] The session ended with a ranked learning table whose top tier separates structural cement from cultural bricks, carrying the proper noun contamination problem and the unbuilt domain divergence layer into the next.
---

**[1] WHO**

The orchestrator thinks by building independent systems first and integrating them only when each piece has proven stable in isolation — he spent an entire prior session building a multi-source corpus pipeline before touching UI, and opened this session by questioning whether to expand the dataset further before deciding the question was answerable cheaply without rebuilding the pipeline. His cognitive signature is a preference for cheap verification over expensive commitment: he asks what a source actually contains before deciding whether to use it, asks what a formula actually produces before trusting it. The bias that shows up most consistently is a structural instinct — he frames problems as architecture questions before feature questions, which is why the conversation about "what UI to build" became "what schema will hold without breaking when the project scales." He also uses multiple LLMs not for generation but for adversarial stress-testing: he collects their critiques, filters by signal quality, and passes only the residue forward.

---

**[2] WHAT HAPPENED**

The session opened after a completed data pipeline — `merged_learning.csv` already existed with learning_rank, wf_zipf, sub_zipf, ox_cefr, ox_pos, and learning_score. The belief at the start was that the next step was straightforward UI scaffolding. That belief was partially correct but the session quickly revealed that "straightforward UI" concealed three unresolved architectural decisions: what the data schema for user state should look like, what tech stack matched the project's long-term shape, and how the UI's navigation metaphor should map to the underlying data structure.

The first decision was stack. The orchestrator had an existing Electron repo for 4-LLM interaction and considered integrating the vocabulary app into it. That path was rejected cleanly — the existing repo is an interface layer, the new app is a data-driven app, and merging them would require refactoring state management in the older repo at disproportionate cost. The decision to build `vocab-explorer` as an independent Electron repo was made before any code was written.

The second decision was schema. An early proposal used `words[word]` as the primary key for `session_state.json`. Four LLMs were run as observers and ChatGPT identified the critical flaw: if `word` is the key, any dataset rebuild that changes a word's surface form or introduces duplicates (proper nouns, domain variants) corrupts progress silently. The key was changed to `entries[id]` with a surrogate format `{source}_{rank_padded}`, making progress portable across dataset rebuilds.

The third decision was navigation. The initial prototype used a block-nav button array — one button per 100-word range, all rendered simultaneously. With 10k entries this produced 100 buttons, which was immediately recognized as unusable. The replacement was a single page-input box with scroll-direction reversal: down = higher rank, matching the metaphor of descending into less-familiar territory.

The scaffold was built incrementally — `main.js` boot, IPC bridge via `preload.js`, CSV parse in main process, renderer displaying 100 rows with block nav, then dark mode styling, then grid-based column alignment. A `package.json` syntax error (missing comma after scripts block) caused a failed start that was diagnosed immediately from the error message. A Windows cache-write permission error was fixed by pre-creating the `app-data/` directory before `app.setPath('userData', ...)`. Nodemon was added for hot-reload workflow.

A parallel data question emerged mid-session: the Oxford source in the existing pipeline was CEFR-J, which caps at B2 and was designed for Japanese learners. A second Oxford source — `nalgeon/words oxford-5k.csv` — was identified with A1–C1 coverage, clean schema, and crucially, a `voice_url` column linking directly to Oxford's `.ogg` pronunciation files. A diff script was written to compare the two sources across four categories: only in CEFR-J, only in Oxford 5k, label conflict, label same.

---

**[3] WHERE IT BROKE**

The stance that collapsed was the assumption that `session_state.json` could use the word string as its primary key. The evidence that destroyed it was not a runtime failure but a logical argument: the word `"bank"` could appear in a future domain pack with a different context, and lowercase proper nouns like `"adam"` or `"george"` are indistinguishable from common words in the current schema. What replaced the destroyed belief was `entries[id]` with a surrogate key — not because it solved the proper noun problem (it does not) but because it decouples progress tracking from surface string identity, making the contamination containable rather than structural.

---

**[4] WHAT REMAINS UNRESOLVED**

The proper noun contamination sits in the dataset without a filter. Words like `adam`, `george`, `jesus`, `michael` score well on learning_rank because they are corpus-balanced, but they are names to recognize rather than vocabulary to learn. There is no column in `merged_learning.csv` that marks them as proper nouns, and no named-entity tagger has been applied. The current UI will display them as learnable vocabulary.

The Oxford source decision is unresolved. The diff between CEFR-J and Oxford 5k has been scripted but not yet run and read. Until the four output files are examined, it is not known whether CEFR-J's labels contradict Oxford 5k's labels systematically or only at the margins, and it is not known which source's POS tagging is more useful for the learner.

The `voice_url` integration path exists in the new Oxford 5k source but has not been merged into `merged_learning.csv`. The mechanism for surfacing audio in the UI — a play button per row that fetches the `.ogg` URL and plays it — has been named but not built.

The write-queue pattern for `session_state.json` was designed (pending + flush) but not yet implemented. The tick-completion feature does not exist in the current UI. Until both are built, progress tracking is unbuilt and the `app-data/` directory is empty.

CMU phonetic data remains in `data/cmu_raw.txt` with no join logic and no UI slot designed for it.

---

**[5] WHAT WAS LEARNED — AND AT WHAT COST**

The lesson that changed behavior most durably this session: **surrogate keys decouple progress from data shape**. Using `word` as primary key feels natural and costs nothing until the dataset changes. Using `id` feels like overhead until the first dataset rebuild, at which point it is the only thing that prevents silent progress corruption. The cost of learning this was zero — it was caught before any user state was written.

The second durable lesson: **four LLMs as adversarial observers produce diminishing returns quickly**. Of the four inputs passed forward, one changed the schema (ChatGPT on `entries[id]`), one correctly identified a real engineering hazard with low signal-to-noise (Gemini on write queue), and two confirmed things already known (Grok on filter blocks, Claude on offline/online conflict). The 4-LLM observer workflow produced roughly 15–20% quality uplift concentrated in one decision. The cost was the orchestrator's time to read and filter four outputs.

The third lesson: **`voice_url` as a free column in a public dataset is a rare find**. The Oxford 5k source from `nalgeon/words` contains direct links to Oxford's own `.ogg` files — no TTS needed, no scraping needed. This changes the pronunciation integration path from "future complex feature" to "one attribute join and one audio element."

---

**[6] METAPHOR ANCHOR**

An engineer laying conduit before the walls go up — the pipes are invisible in the finished building, but every future decision about where to run electricity was made possible or impossible by where the conduit was placed before the concrete poured.

---

[2026-06-09] The session ended with a running dark-mode Electron scaffold displaying 10k entries with page navigation, carrying the unbuilt tick-completion system, the unresolved Oxford source comparison, and the unjoined voice_url column into the next.