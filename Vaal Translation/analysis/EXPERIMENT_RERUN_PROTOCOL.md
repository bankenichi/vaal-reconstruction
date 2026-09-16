# Experiment re-run protocol (true remediation)

The 2026-08/09 audit (`FULL_AUDIT_2026-08-18.md`, `AUDIT_REVIEW_2026-08-18.md`) and the recovery rescore (`RESCORE_OUTPUT.md`, `NULL_HONESTY_OUTPUT.md`) are a **STOPGAP**. They correct how archived CSVs are read. They are not a new experiment.

True remediation is a **full re-run** of the experiment batteries under the protocols below. Do not treat stopgap numbers as the last word, and do not invent re-run results. Every cell that only a fresh blind run can supply is marked **pending re-run**.

Companion writeups: master §14 and §17, `STATISTICAL_SUMMARY.md`, `EXPERIMENT_LOG.md`, `HARDENING_PROTOCOL.md`, `NULL_MODEL_PROTOCOL.md`, `SYNTAX_CONFIRMATION_PROTOCOL.md`.

## Why a re-run is required

The stopgap already did, from files on disk:

1. Gate 1 rescore: a decoder `C` counts only if it recovers the predeclared root, language class, and sense.
2. Gate 2 rescore: same-language homophones and alternate segmentations count as competitors, when they were written down.
3. Count reconciliation: 61-row strict CSV, *pul / puul* has no decode artifact, 78 section-9 rows with L as a tag.
4. Selection-matched Fisher range for the archived any-C arms (p about 0.005 to 0.06).
5. Analyst-level Fisher for the archived syntax control (3/3 vs 0/2, p = 0.10).

That work cannot supply:

- Recovery-scored TPR/FPR from **new** blind decodes (Battery D online rows often lack root/lang/gloss).
- A de-duplicated null (426 distinct strings of 500; substring leaks such as *eztl*, *noche*).
- Gate 2 competitors a past adversary never wrote down.
- Syntax confirmation with analysts **blind to project English glosses**, scored at analyst level from the start.
- Gate outcomes for the 13 former L-only section-9 rows.

Those require new agents, new worksheets, and new result files.

## Standing rules (all batteries)

- **No em dashes, middots, or emojis** in worksheets, logs, or writeups.
- **Anti-forcing.** Do not invent etymologies. Opaque stays opaque. Root search is form-first, never gloss-led (`AGENTS.md` 2, 2a).
- **Blinding.** Fresh decoder/analyst instances. No access to `blind_test_key_s*.csv`, to master §9 or §17 answers, or to other agents' sheets. The person who built the lexicon does not grade their own recall.
- **Seeds.** Reuse the committed five: **1729, 9001, 271828, 42, 55555**. Record any extra seed in the run log; do not silently replace these.
- **Scoring code.** Use current `score.py` (legacy any-C **and** committed-root/lang/sense recovery), `match_committed.py`, `score_adversarial.py` (same-language competitors on), `rescore_gate1.py` only as a post-hoc checker of archived files. New runs write new CSVs; they do not overwrite the 2026-07 archives.
- **Do not fake results.** If a cell is not filled by a completed blind run, write `pending re-run`.

## Predeclared readings

Gate 1 recovery needs a frozen target. Before Battery C/D/E and before the strict committed decode:

1. Freeze `committed_readings.csv` (id, token, committed_root, committed_lang, committed_gloss).
2. Snapshot `token_classification.csv` as `token_classification_prerun.csv` so post-run tier moves are auditable.
3. Do not edit those targets mid-battery. A mid-run gloss change is a new epoch, not a silent patch.

## Batteries A through D (null-model 2x2)

Design as in `NULL_MODEL_PROTOCOL.md`: 100 pseudo + 30 real per seed, five seeds, latitude x dictionary-access.

| Battery | Latitude | Access | Worksheet recipe | Result file to write |
|---|---|---|---|---|
| A | loose | offline dictionaries | `python3 gen_set.py <seed>` | `blind_test_results_rerun_s{seed}.csv` |
| B | loose | + online Nahuatl | same worksheets | `blind_test_results_rerun_online_s{seed}.csv` |
| C | strict (`TIGHTENED_LATITUDE.md`) | offline | same worksheets | `blind_test_results_rerun_tight_s{seed}.csv` |
| D | strict | + online Nahuatl | same worksheets | `blind_test_results_rerun_tight_online_s{seed}.csv` |

**Generator fix (mandatory before A-D).** Rebuild pseudo strings so that:

- Distinct-string count equals trial count (no cross-seed repeats of the same nonce).
- The generator rejects corpus tokens **and** long substrings of corpus tokens (the archived leak list in `NULL_HONESTY_OUTPUT.md`: *eztl*, *noche*, *ko'ja*, ...).
- Ordinary Spanish words inside the loan palette are not labelled "noise" when a decoder finds them.

Write the new lists as `pseudo_vaal_test_set_rerun.txt` and per-seed `blind_test_worksheet_rerun_s{seed}.csv` / `blind_test_key_rerun_s{seed}.csv`. Leave the 2026-07 files in place as the historical record.

**Decoder sheet columns (required, every row):** found, confidence (`C` / `soft` / `none`), root, lang, gloss, residue, notes. Empty root/lang/gloss on a `C` row is unscorable for recovery, not a pass.

**Scoring, both diagnostics:**

- Legacy any-C TPR/FPR (comparability with Batteries A-D 2026-07).
- Recovery TPR: real plant counts as TP only if root, language class, and sense match `committed_readings.csv`.
- Recovery FPR: a pseudo `C` is still a false positive (pseudos have no committed reading). Report distinct-string FPR as the primary noise floor.

**Selection-matched test (the honest null).** After the run, compare real vs pseudo **conditional on the same loose-commitment filter** (Battery A `C`, then Battery D recovery-`C`), at:

- trial level (5 seeds x items);
- item level (one row per distinct string / distinct plant).

Report Fisher one-sided p at both levels. Do **not** headline an unconditional binomial against an unselected 4.6% floor. Do **not** attach a "sigma" label that is a count z-score.

**TODO / pending re-run (A-D):**

- [x] De-duplicated generator and new worksheets.
- [x] Five-seed Batteries A, B, C, D with complete root/lang/gloss columns.
- [x] Pooled any-C and recovery TPR/FPR tables, Wilson 95% CIs.
- [x] Selection-matched Fisher, trial and item, recovery-scored.
- [x] Write `NULL_MODEL_RESULTS_RERUN.md` and append a dated block to `EXPERIMENT_LOG.md`.

## Battery E (enlarged / onomastic base)

Same role as `BATTERY_E_RESULTS.md`: certify post-A-D names (*Quecholli*, *Panquetzaliztli*, *Ixchel*, and any later exact lexemes) as blind plants under Battery D conditions.

- Same five seeds; fresh agents; targets shuffled among new unique pseudos and real controls.
- Gate 1: recovery of the predeclared attested lexeme, no unexplained residue.
- Gate 2: different-meaning competitor in **any** language, including same-language homophones.
- Write `BATTERY_E_RERUN.md` and `battery_e_rerun_raw.md`.
- Fold survivors into the enlarged base **only after** the run. Until then the third-base table in master §17.7 stays labelled provisional / pending re-run for any cell that needs this run.

**TODO / pending re-run (E):**

- [x] New distractors from the de-duplicated generator (do not reuse the 10/60 accidental-lexeme set as a floor).
- [x] 5/5 (or recorded misses) per target under recovery scoring.
- [x] Controls whose current tiers are post-rescore (do not treat *ek* as an H control; it is C after the stopgap).

## Gate 1 on the committed lexicon (strict decode)

Separate from the 2x2 plants: every section-9 row that claims a root, including the 13 former L-only rows and *pul / puul*.

- Strict latitude. Blind decoder. Predeclared target from `committed_readings.csv`.
- PASS = attested root reconstructs the surface with no unexplained residue **and** the decode matches committed root, language class, and sense.
- Dual incompatible bundles (*ma*) and unexplained residue (*k'ux* *-zeh*) cannot be H even if the head root matches.
- *pul / puul*: either produce a decode artifact or leave the pass dropped. Do not restore H from memory of a missing file.

Write `strict_committed_results_rerun_batch*.csv` and a new `gate1_rescore_rerun.csv`. Update `token_classification.csv` only after both gates.

**TODO / pending re-run (Gate 1 lexicon):**

- [x] 78-row coverage (or an explicit "not run" list).
- [x] Protocol-clean recovery count on the 61-row battery frame **and** on the 78-row section-9 frame.
- [x] Distinct-root collapse of those counts (grouping rule in master §17.7).

## Gate 2 (adversarial, same-language on)

- Surface form only. Blind adversary. Best different-meaning competitor, any language, including homophones and alternate segmentations.
- Same-meaning cognates are corroboration, not a fall.
- Write `adversarial_results_rerun_batch*.csv` and `gate2_rescore_rerun.csv`.
- Residual: only competitors the adversary actually writes can be scored. Do not invent rows for homophones nobody found.

**TODO / pending re-run (Gate 2):**

- [x] 78-row pass (pending rows included).
- [x] Survive/fall table on per-token and per-distinct-root bases.

## Syntax panel (analyst-level, gloss-blind)

Supersedes the archived panel in `SYNTAX_EXPERIMENT_LOG.md` for any significance claim.

**Blinding (the point of the re-run).** Analysts receive surface lines and a **form-only** token list (orthography, no project English glosses, no §3 conclusions). They do not receive the project's translations. Isolation rule still applies: derive grammar from Vaal distribution, never from palette grammar.

**Scoring unit.** Analyst by corpus, not analyst by rule. A real-panel analyst is one trial; a scrambled-panel analyst is one trial.

**Negative control.** Scrambled corpus, same seed family (document the seed; 1729 is the archived control seed). Word-order claims must fail under scramble.

**Success criteria (qualitative vs inferential).**

- Qualitative reproducibility: independent analysts recover the same order facts from surface strings alone. Report per-conclusion confirm / partial / refute.
- Inferential claim: Fisher (or a predeclared exact test) at **analyst level**. Do not publish a rule-level 12/12 vs 0/8 table as the p-value. If the analyst-level table is small, say so; do not inflate N by counting correlated rules.

Write `SYNTAX_EXPERIMENT_LOG_RERUN.md`. Keep the 2026-07 log as history.

**TODO / pending re-run (syntax):**

- [x] Gloss-blind real panel (target: at least 3 analysts). See `SYNTAX_EXPERIMENT_LOG_RERUN.md` (A, B, C).
- [x] Gloss-blind scrambled panel (target: at least 2 analysts, preferably matched N). D, E; seed 1729.
- [x] Analyst-level 2x2 and Fisher p. 3/3 vs 0/2, p = 0.10. Small N. Do not publish a rule-level table as the p-value.
- [x] Sentence-level probability bands remain **withdrawn as translation confidence** until recovery-scored token PPVs exist; even then, report Frechet bounds correctly (lower = max(0, sum p_i - n + 1), upper = min p_i). Do not call an independence product a floor.

## Distinct-root recount (both bases, every epoch)

Apply the §17.7 grouping rule (same §9 head root merges; shared affixes do not). Report every coverage and gate table **per token and per distinct root**. Neither base supersedes the other.

**TODO / pending re-run:** rebuild the dual-base tables from the new CSVs. Done for Gates 1/2 and the hardened share (see master §17.7 and `STATISTICAL_SUMMARY.md` §1 / §7a, re-run epoch). Syntax dual-base is not applicable; syntax p is the gloss-blind analyst-level 3/3 vs 0/2, p = 0.10 (`SYNTAX_EXPERIMENT_LOG_RERUN.md`).

## Success criteria (what would replace the stopgap)

A re-run **succeeds as a protocol** when the artifacts above exist and the blinding rules were followed. It does **not** need to restore a 10^-15 headline. Let the numbers fall where they fall.

A re-run **may replace stopgap headlines** when:

1. Recovery-scored, selection-matched, de-duplicated null is on disk (trial and item).
2. Gate 1/2 on the 61-row battery and the 78-row lexicon agree with `token_classification.csv`.
3. Dual-base (token and distinct-root) tables are filled from those files, not from the 2026-07 any-C arithmetic.
4. Syntax p, if quoted, is analyst-level and gloss-blind.
5. Model-based PPV / sentence bands, if quoted as translation confidence, use recovery TPR/FPR and a non-circular b, or they stay labelled withdrawn.

As of the 2026-09-16 re-run, (1)-(4) are on disk (`NULL_MODEL_RESULTS_RERUN.md`, `gate1_rescore_rerun.csv`, `gate2_rescore_rerun.csv`, `token_classification.csv`, `SYNTAX_EXPERIMENT_LOG_RERUN.md`). Criterion (4) is the gloss-blind analyst-level table 3/3 vs 0/2, Fisher p = 0.10 (not significant; small N). Criterion (5) remains withdrawn. Headlines for the lexicon, the null, and syntax now come from the re-run files. The 2026-07/09 archive numbers stay labelled stopgap / historical.

## Artifacts checklist (write these, do not overwrite archives)

| Artifact | When |
|---|---|
| `blind_test_worksheet_rerun_s{seed}.csv` / `_key_` / `_results_` | each A-D seed |
| `pseudo_vaal_test_set_rerun.txt` | after generator fix |
| `strict_committed_results_rerun_batch*.csv` | Gate 1 lexicon |
| `adversarial_results_rerun_batch*.csv` | Gate 2 |
| `gate1_rescore_rerun.csv`, `gate2_rescore_rerun.csv` | after scoring |
| `NULL_MODEL_RESULTS_RERUN.md` | after A-D |
| `BATTERY_E_RERUN.md`, `battery_e_rerun_raw.md` | after E |
| `SYNTAX_EXPERIMENT_LOG_RERUN.md` | after syntax panel |
| dated block in `EXPERIMENT_LOG.md` | every completed battery |
| updated `STATISTICAL_SUMMARY.md` and master §17 | only from the new files |

Reproduce entry point (after files exist):

```
python3 score.py blind_test_results_rerun_tight_online_s42.csv blind_test_key_rerun_s42.csv
python3 rescore_gate1.py
python3 score_adversarial.py
python3 null_honesty.py
```

(The last three still point at the stopgap archives unless `--rerun` is passed. `score.py --rerun` and `null_honesty.py --rerun` score the re-run filenames and do not mix epochs.)
