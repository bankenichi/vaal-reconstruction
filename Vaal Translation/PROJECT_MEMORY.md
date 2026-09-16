# Project memory (running summary)

Carried-over summary of the Vaal Translation project state. Update as work progresses. For operating rules see `AGENTS.md`; for the statistics see master §17 and `analysis/STATISTICAL_SUMMARY.md`.

## Purpose and context

Kenichi is producing a rigorous academic reconstruction of the "Vaal language" (Vaalish) from Path of Exile 2, read as a Mesoamerican-sourced constructed language. The core layer is Yucatec Maya, with Classical Nahuatl (divinity, place-names), K'iche' (a thin /r/ seam), Spanish loans, and Xinkan and Nawat/Pipil as secondary candidate pools. Standards are historical-linguistic: every committed root is attested in a named primary dictionary with explicit phonology, competing readings are logged not discarded, forced etymologies are prohibited (form-first, never gloss-led), and no lore is fabricated. Hard formatting rule across all documents and chat: no em dashes, middots, or emojis.

## Files and where they live

- Canonical master: `Vaal Translation/Vaal_Reconstruction.md`. Parent copy at repo-root `Vaal_Reconstruction.md`, kept byte-identical. The `Vaal Translation Mirror/` tree is gitignored and is not in this repository.
- Companions in `analysis/`: STATISTICAL_SUMMARY, EXPERIMENT_LOG, EXPERIMENT_RERUN_PROTOCOL, NULL_MODEL_PROTOCOL/RESULTS, NULL_HONESTY_OUTPUT, ADVERSARIAL_RESULTS, HARDENING_PROTOCOL, TIGHTENED_LATITUDE, SYNTAX_CONFIRMATION_PROTOCOL, SYNTAX_EXPERIMENT_LOG, REVIEW, token_classification.csv, gate1_rescore.csv, committed_readings.csv, RESCORE_OUTPUT.md, and the scorers (`score.py`, `score_adversarial.py`, `match_committed.py`, `rescore_gate1.py`, `null_honesty.py`).

## Data-integrity protocol (mandatory, learned the hard way)

Data loss is unacceptable. Designate the one canonical master, verify it is COMPLETE against the checklist (sections 1-18 present, citations contiguous to 59, ends cleanly, line count not shrunken, zero em dashes/emoji) BEFORE using it as a copy source, propagate one-way only (canonical to parent), and verify destination identity by md5. Full rule in `AGENTS.md` section 4. The mirror is not in git; do not treat a missing mirror as a copy to invent.

## Current state (2026-09: re-run on disk, Ixchel Gate 1 honesty)

- Master: 18 sections, roughly 147 morpheme-index elements, 59 citations. Parent copy kept byte-identical with the canonical.
- **The audit plus recovery rescore is a STOPGAP, not the last word.** True remediation is the re-run of Batteries A-E under `analysis/EXPERIMENT_RERUN_PROTOCOL.md` (now on disk). Gate 1 is recovery of committed root/lang/sense. Do not frame the old batteries as simply invalid and closed, and do not claim the re-run rejects a pure-noise null.
- Lexicon population: **78 section-9 rows**, each with H/C/S/O; L is a tag only. `token_classification.csv` has 78 rows. Battery-tested Gate 1 is the **61-row** strict CSV. *pul / puul* has a decode artifact (Gate 1 yes, Gate 2 fall, C*).
- Hardened after recovery scoring, protocol, and Ixchel Gate 1 honesty: **2 of 78 = 2.6% [0.7, 8.9]** per token, **2 of 69 distinct roots = 2.9% [0.8, 10.0]**. Battery frame: **1 of 61 = 1.6% [0.3, 8.7]** / **1 of 52 = 1.9% [0.3, 10.1]**. Enlarged base (61 + three Battery E names): **2 of 64 = 3.1% [0.9, 10.7]** / **2 of 55 = 3.6% [1.0, 12.3]**. Hardened set: *xefe*, *Quecholli*. *Ixchel* is C+L (Cordemex herb ≠ approved theonym / Godstealer; gloss unchanged). Split: H 2 / C* 30 / C 45 / S 1. Dual-base tables in master §17.5-17.7 and `STATISTICAL_SUMMARY.md`.
- Translation batteries T-M / T-D: vs-gold match+partial about 29% both arms (T-M 29.4% [24.2, 35.3]; T-D 28.2% [23.1, 34.1]). Methodology does not lift agreement; it cuts clash and raises abstain (`TRANSLATION_BATTERY_RESULTS.md`).
- Secure-line grades (2026-09-16): 0/51 secure (0%), 12/51 working (~24%), 38/51 fragile (~75%), 1/51 opaque-blocked (`analysis/SECURE_LINE_TAGS.md`). Not PPV. Working count unchanged by Ixchel (the name is not in the 51 lines).
- Leave-one-text-out (2026-09-16): ok 12/51 = 23.5% [14.0, 36.8]; ok+partial 33/51 = 64.7% [51.0, 76.4]; T3 0/13 ok (`analysis/LEAVE_ONE_TEXT_OUT.md`).
- Null model: the 2 x 10^-15 (and 10^-18 / 10^-19) all-noise headlines are withdrawn as headlines, as is the sigma column. Re-run selection-matched any-C: **p = 0.09494** (p ≈ 0.095) trial, **p = 0.3069** (p ≈ 0.31) item. Recovery-scored matched: **p = 1** / **p = 0.9991**. That is not a claim that the corpus is very unlikely to be pure noise. Pseudo corpus this epoch: 500 distinct of 500. Cite `AUDIT_REVIEW_2026-08-18.md`.
- PPV and sentence-level percentages: structure restored in §17.5 and `STATISTICAL_SUMMARY.md` §§3-6; labelled **withdrawn as translation confidence**. Independence products are not a Frechet floor. *yan* is not a lexicon row. The committed lexicon is the project's chosen readings; most rows are C or C*, not a probable-as-a-whole certification. Transcriptions and corpus documentation are stable; interpretive and translation confidence is thin.
- Syntax: report analyst-level Fisher **3/3 vs 0/2, p = 0.10**, not the rule-level 12/12 vs 0/8 as a significance claim. Gloss-blind re-run (2026-09-16): 3/3 vs 0/2, p = 0.10, not significant (`SYNTAX_EXPERIMENT_LOG_RERUN.md`). Possession undetermined for two of three real analysts; do not overclaim.
- Scorers: `score.py` reports legacy any-C TPR and committed-root/lang/sense recovery. `score_adversarial.py` counts same-language homophones and alternate segmentations as competitors. Proof: `RESCORE_OUTPUT.md`, `NULL_HONESTY_OUTPUT.md`, `NULL_MODEL_RESULTS_RERUN.md`.
- Tournaments / particles (2026-09-16): `RIVAL_READING_TOURNAMENTS.md`, `PARTICLE_PROBES_3_7.md`. Five C* stars (*ik'el, 'Ibil, mucane, kifba, Tzokan'te*); *tlayeb* stays C+L (ladder is a cross-graft loser, logged). Gloss wording unchanged. H is 2 of 78 after Ixchel honesty. §3.7 items leaning or still open.
- Texts 1 and 2 closed and source-validated; Texts 3, 4, 5 documented with soft tokens in the §10 appendix. Kamasan *jare'yantul* is not a full committed parse: *yan* is O.
- Family audit: grouping footnotes only; distinct-root N unchanged. *Panquetzaliztli* compound pass: missing whole form, stays C+L.

## Remaining open analytical debt

- Batteries A-E re-run is on disk. Remaining: do not mix epochs; do not restore the withdrawn 10^-15 headline.
- Full-pipeline null (commit then strict-gate on each unique pseudo string) not re-run; matched A-then-D is this epoch's selection-matched test (p = 0.09494 / 0.3069 any-C; recovery-scored p = 1 / 0.9991).
- Battery D online rows often lack root/lang/gloss; recovery TPR there is partly unscorable.
- Gate 2 can only score competitors the adversary wrote down. Homophones absent from those CSVs are not invented in the CSV (Gate 1 already fails *ek* wasp). The 2026-09-16 tournaments logged five additional homophones in `token_classification.csv` and §10.13 without rewriting `gate2_rescore_rerun.csv`.
- Gloss-blind syntax panel is on disk (3/3 vs 0/2, p = 0.10). Possession remains fragile.
- The 13 former L-only section-9 rows have re-run gates recorded in `token_classification.csv` (mostly Gate 1 fail). They are C+L / C+L* / S+L, not pending ungated rows.
- *xi* section-9 gloss (Nahuatl "do/make") is independently doubtful as a free verb; it is demoted from H on scoring, not re-etymologized.
- *Ixchel* is C+L after Gate 1 honesty (herb ≠ approved theonym). Gloss frozen.

## Open items (tracked, not forced)

The o-...-s wrapping around tsuk in Otsuks; the exact K'iche' lemma behind jare'; fukuur's phonetic fit; ta' (leaning relational ti', not closed); ukto (leading reading Nahuatl ocotl "pine torch," soft); and from the syntax pass the particles ka and ti (leaning verbal-question linker), the le le doubling (still open), and tlayeb category (still open).

## Out of scope

A phonetic (audio-based) phonology. Anyone with the specialist skills is welcome to take it up; §17.9 is the ceiling this project sets for phonology.

## Key principles

Anti-forcing (opaque stays opaque); form-first, never gloss-led (applies to roots and to syntax); competing readings logged; semantic field constrains the search; romanization artifacts are distinguished from morphology; living-Maya and Nawat sources corroborate; variant NPC names are a game mechanic, not lore drift; the PDF and parent copy are kept current under the data-integrity protocol. Kenichi ordered the 2026-09 remediation executed without a further approval wait, then ordered dual-base structure restored and the stopgap/re-run distinction made explicit, again without a further wait. Tournaments and particle probes (plan items 1 then 2) were ordered the same way: execute, log losers in §10, do not rebuild the PDF, do not commit dictionaries.
