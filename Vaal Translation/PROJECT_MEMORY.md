# Project memory (running summary)

Carried-over summary of the Vaal Translation project state. Update as work progresses. For operating rules see `AGENTS.md`; for the statistics see master §17 and `analysis/STATISTICAL_SUMMARY.md`.

## Purpose and context

Kenichi is producing a rigorous academic reconstruction of the "Vaal language" (Vaalish) from Path of Exile 2, read as a Mesoamerican-sourced constructed language. The core layer is Yucatec Maya, with Classical Nahuatl (divinity, place-names), K'iche' (a thin /r/ seam), Spanish loans, and Xinkan and Nawat/Pipil as secondary candidate pools. Standards are historical-linguistic: every committed root is attested in a named primary dictionary with explicit phonology, competing readings are logged not discarded, forced etymologies are prohibited (form-first, never gloss-led), and no lore is fabricated. Hard formatting rule across all documents and chat: no em dashes, middots, or emojis.

## Files and where they live

- Canonical master: `Vaal Translation/Vaal_Reconstruction.md`. Parent copy at repo-root `Vaal_Reconstruction.md`, kept byte-identical. The `Vaal Translation Mirror/` tree is gitignored and is not in this repository.
- Companions in `analysis/`: STATISTICAL_SUMMARY, EXPERIMENT_LOG, EXPERIMENT_RERUN_PROTOCOL, NULL_MODEL_PROTOCOL/RESULTS, NULL_HONESTY_OUTPUT, ADVERSARIAL_RESULTS, HARDENING_PROTOCOL, TIGHTENED_LATITUDE, SYNTAX_CONFIRMATION_PROTOCOL, SYNTAX_EXPERIMENT_LOG, REVIEW, token_classification.csv, gate1_rescore.csv, committed_readings.csv, RESCORE_OUTPUT.md, and the scorers (`score.py`, `score_adversarial.py`, `match_committed.py`, `rescore_gate1.py`, `null_honesty.py`).

## Data-integrity protocol (mandatory, learned the hard way)

Data loss is unacceptable. Designate the one canonical master, verify it is COMPLETE against the checklist (sections 1-18 present, citations contiguous to 59, ends cleanly, line count not shrunken, zero em dashes/emoji) BEFORE using it as a copy source, propagate one-way only (canonical to parent), and verify destination identity by md5. Full rule in `AGENTS.md` section 4. The mirror is not in git; do not treat a missing mirror as a copy to invent.

## Current state (2026-09: stopgap rescore, structure restored, re-run pending)

- Master: 18 sections, roughly 147 morpheme-index elements, 59 citations. Parent copy kept byte-identical with the canonical.
- **The audit plus recovery rescore is a STOPGAP, not the last word.** True remediation is a full re-run of Batteries A-E under `analysis/EXPERIMENT_RERUN_PROTOCOL.md` (recovery Gate 1 matching committed root/lang/sense; Gate 2 including same-language competitors; de-duplicated null; syntax with analysts blinded to project English glosses, scored at analyst level). Do not frame the old batteries as simply invalid and closed.
- Lexicon population: **78 section-9 rows**, each with H/C/S/O; L is a tag only. `token_classification.csv` has 78 rows. Battery-tested Gate 1 is the **61-row** strict CSV. *pul / puul* has no decode artifact; its published Gate-1 pass is dropped (now C, cell kept as `no_artifact` / pending re-run).
- Hardened after recovery scoring and protocol demotion: **17 of 78 = 21.8% [14.1, 32.2]** per token, **17 of 69 distinct roots = 24.6% [16.0, 36.0]**. Battery frame: **14 of 61 = 23.0% [14.2, 34.9]** / **14 of 52 = 26.9% [16.8, 40.3]**. Provisional enlarged base (61 + three Battery E names): **17 of 64 = 26.6% [17.3, 38.5]** / **17 of 55 = 30.9% [20.3, 44.0]**. Dual-base tables and the third-base subsection are restored in master §17.5-17.7 and `STATISTICAL_SUMMARY.md`. Demoted from H: *akal, ek, tul, uch', xi, k'ux, ma, pul*. Old 22/62 and 25/65 figures are the prior published epoch, not current certification rates.
- Scorers: `score.py` now reports legacy any-C TPR and committed-root/lang/sense recovery. `score_adversarial.py` counts same-language homophones and alternate segmentations as competitors. Proof: `RESCORE_OUTPUT.md`, `NULL_HONESTY_OUTPUT.md`.
- Null model: the 2 x 10^-15 (and 10^-18 / 10^-19) all-noise headlines are withdrawn as headlines, as is the sigma column (those labels were count z-scores). Stopgap selection-matched range: **p about 0.005 to 0.06 (marginal)**. Recovery-scored de-duplicated p: pending re-run. Pseudo corpus: 426 distinct of 500; some noise hits are palette substrings. Cite `AUDIT_REVIEW_2026-08-18.md`.
- PPV and sentence-level percentages: structure restored in §17.5 and `STATISTICAL_SUMMARY.md` §§3-6; labelled **withdrawn as translation confidence / stopgap pending re-run**. Independence products are not a Frechet floor. *yan* is not a lexicon row.
- Syntax: report analyst-level Fisher **3/3 vs 0/2, p = 0.10**, not the rule-level 12/12 vs 0/8 as a significance claim. Analysts were not blind to project glosses. Gloss-blind analyst-level re-run: pending (`EXPERIMENT_RERUN_PROTOCOL.md`).
- Texts 1 and 2 closed and source-validated; Texts 3, 4, 5 documented with soft tokens in the §10 appendix.

## Remaining open analytical debt

- Full re-run of Batteries A-E under `EXPERIMENT_RERUN_PROTOCOL.md` (the true remediation). Do not fake those results.
- Full-pipeline null (commit then strict-gate on each unique pseudo string) not re-run; matched A-then-D is the archived-file stopgap.
- Battery D online rows often lack root/lang/gloss; recovery TPR there is partly unscorable.
- Gate 2 can only score competitors the adversary wrote down. Homophones absent from those CSVs are not invented (Gate 1 already fails *ek* wasp).
- Syntax panel not re-run blinded to project English.
- Several section-9 C+L rows (the former L-only 13) have gates pending.
- *xi* section-9 gloss (Nahuatl "do/make") is independently doubtful as a free verb; it is demoted from H on scoring, not re-etymologized.

## Open items (tracked, not forced)

The o-...-s wrapping around tsuk in Otsuks; the exact K'iche' lemma behind jare'; fukuur's phonetic fit; ta' (ti' vs taak); ukto (leading reading Nahuatl ocotl "pine torch," soft); and from the syntax pass the particles ka and ti, and the le le doubling.

## Out of scope

A phonetic (audio-based) phonology. Anyone with the specialist skills is welcome to take it up; §17.9 is the ceiling this project sets for phonology.

## Key principles

Anti-forcing (opaque stays opaque); form-first, never gloss-led (applies to roots and to syntax); competing readings logged; semantic field constrains the search; romanization artifacts are distinguished from morphology; living-Maya and Nawat sources corroborate; variant NPC names are a game mechanic, not lore drift; the PDF and parent copy are kept current under the data-integrity protocol. Kenichi ordered the 2026-09 remediation executed without a further approval wait, then ordered dual-base structure restored and the stopgap/re-run distinction made explicit, again without a further wait.
