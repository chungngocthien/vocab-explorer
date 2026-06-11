# who.md
<!-- COGNITIVE SIGNATURE EDITION — do not add sections, do not rename sections, do not modify rules -->

---

## [SIGNAL]

Last updated: 2026-06-09 after 2 sessions

---

## [CORE]

LOCKED: Defers source commitment until the schema can hold multiple sources simultaneously. Demonstrated in session 1 (corpus pipeline: wordfreq + subtitles + Oxford held in parallel before any single source was over-invested in) and session 2 (Oxford source comparison scripted before deciding which source to use in rebuild).

LOCKED: Asks "what does this actually contain?" before deciding whether to use it. Demonstrated across both sessions: asked what wordfreq contained before using it, asked what CMU contained before committing to it, asked what Oxford 5k's schema looked like before writing the diff script.

STABLE [count: 2/4]: Uses multiple LLMs as adversarial stress-testers, not generators. Session 1: four LLMs ran formula stress-tests on learning_score candidates. Session 2: four LLMs ran architectural critique on schema and UI decisions. Counter-evidence check: orchestrator could have used LLM output as primary driver rather than filter — but in both sessions he read outputs, judged signal quality explicitly (naming ChatGPT's contribution as the only structurally significant one in session 2), and passed only residue forward.

STABLE [count: 1/4]: Frames problems as architecture questions before feature questions. Session 2 only so far. "What UI to build" became "what schema will hold without breaking" before any code was written. Counter-evidence check: he could have scaffolded the UI first and designed schema later — he did not.

STABLE [count: 1/4]: Names stopping conditions explicitly rather than running until blocked. Session 1: named "tâm trí hết idea để mổ thêm" as a clean signal to stop. Session 2: recognized that expanding the dataset to 50k entries would satisfy curiosity cheaply without rebuilding the pipeline, and chose not to rebuild. Counter-evidence check: he did continue the Oxford source investigation rather than stopping — but that was additive exploration, not continuation past a named stopping point.

---

## [THRESHOLDS]

Schema-first trigger → when a feature requires persisting user state, stop and design the schema before writing any code. Do not write placeholder state.

Source-first trigger → when a new data source is proposed, ask for its schema and sample rows before writing any pipeline logic. Do not assume schema from source name.

Free-parameter smell → when a formula requires a manually chosen constant (α, ceiling, n), treat it as a signal that the formula is wrong. Look for a parameter-free formulation before tuning.

LLM-as-oracle risk → when an LLM gives a long detailed answer, treat signal-to-noise ratio as the primary question. Do not treat length or technical detail as quality signal.

Scope-inflation recognition → when a new feature would require refactoring a stable component in a separate repo, stop and evaluate whether the cost is proportionate. Default answer is no.

Dataset-expansion skepticism → when the impulse is to expand a dataset for completeness, ask whether the question can be answered by sampling instead. Rebuild the full pipeline only if sampling cannot answer it.

---

## [GROWTH]

2026-06-08 [session 1] No prior baseline → established: defers source commitment, resists premature closure, calibrates stopping conditions internally rather than by external failure signal.

2026-06-09 [session 2] Single-repo assumption → multi-repo with shared data protocol: recognized that a stateful data app and a stateless interface layer have incompatible architectures and should not be merged. Shared state via portable JSON file named as protocol boundary.

2026-06-09 [session 2] LLM-as-observer pattern formalized: moved from using LLMs for generation to using them explicitly as adversarial filters, with explicit quality assessment of each contribution before passing residue forward.

---

## [METAPHOR]

A cartographer who triangulates from multiple expeditions' maps — each biased by the route taken — and produces not one authoritative map but a transparent overlay where the disagreements between maps are themselves the most useful information. Now also the engineer who lays conduit before the walls go up: the invisible infrastructure placed early determines what is possible later, and no amount of feature work after the concrete pours can fix a conduit placed wrong.
