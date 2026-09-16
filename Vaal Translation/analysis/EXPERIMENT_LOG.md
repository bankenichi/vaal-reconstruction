# Experiment log

Evidence-based record of the statistical work behind the lexicon hardening (master §17). All runs are blind (fresh decoders, no access to the answer key or the master). All null-model worksheets are reproducible: `python3 gen_set.py <seed>`.

## What was run

| Experiment | Design | Seeds | Sample | Result files |
|---|---|---|---|---|
| Null model, Battery A | loose latitude, offline dictionaries | 1729, 9001, 271828, 42, 55555 | 500 pseudo + 150 real | `blind_test_results_s{seed}.csv` (+ base) |
| Null model, Battery B | loose latitude, + online Nahuatl | same 5 | 500 + 150 | `blind_test_results_online_s{seed}.csv` |
| Null model, Battery C | strict latitude, offline | same 5 | 500 + 150 | `blind_test_results_tight_s{seed}.csv` |
| Null model, Battery D | strict latitude, + online Nahuatl | same 5 | 500 + 150 | `blind_test_results_tight_online_s{seed}.csv` |
| Null model, Battery E | strict + online; 3 post-battery names as blind plants | same 5 | 3 targets + 12 pseudo + 5 controls / seed | `BATTERY_E_RESULTS.md`, `battery_e_raw.md` |
| Adversarial pass | best root in a different language, per committed token | n/a | 61 committed tokens | `adversarial_results_batch{1..4}.csv` |
| Strict decode of committed lexicon | strict latitude, per committed token | n/a | 61 committed tokens | `strict_committed_results_batch{1..4}.csv` |

Scorers: `score.py` (null model; prints legacy any-C and committed-recovery TPR), `score_adversarial.py` (Gate 2, including same-language homophones), `rescore_gate1.py`, `null_honesty.py`. Classification: `token_classification.csv` (78 rows). Proof of rescored counts: `RESCORE_OUTPUT.md`, `NULL_HONESTY_OUTPUT.md`.

## Headline results (pooled)

Null model, per battery:

| Battery | FPR(C) | FPR(C+soft) | TPR(C) | TPR(found) | Discrimination(C) | Enrichment(C) |
|---|---|---|---|---|---|---|
| A loose/offline | 0.062 | 0.670 | 0.207 | 0.767 | +0.145 | 3.3x |
| B loose/online | 0.080 | 0.576 | 0.173 | 0.653 | +0.093 | 2.2x |
| C strict/offline | 0.034 | 0.064 | 0.127 | 0.180 | +0.093 | 3.7x |
| D strict/online | 0.046 | 0.094 | 0.140 | 0.173 | +0.094 | 3.0x |

Battery D (the fourth cell of the latitude x access 2x2, run with fresh blind agents grepping the offline dictionaries plus online Nahuatl at Wired Humanities and the Gran Diccionario Nahuatl): adding online access under the strict rules moves FPR (0.034 to 0.046) and TPR (0.127 to 0.140) up together, leaving discrimination flat (+0.094). Same pattern as B vs A under loose rules: coverage, not separation. Latitude is the axis that matters.

(Metric definitions and formulas: master §17.2 and `NULL_MODEL_RESULTS.md`.)

Evidence-based conclusions:

- The soft tier is statistically close to noise (found rate 67% noise vs 77% real under loose rules). Soft = candidate, not evidence.
- The committed tier clears the noise floor by about 3x, stable across all 5 seeds.
- More dictionary coverage (Battery B) did not widen discrimination; it narrowed it. Coverage is not the bottleneck.
- Tightening latitude (Battery C) collapsed noise-matching (0.670 to 0.064) and the committed lexicon's reconstructability together (0.767 to 0.180): most committed readings depend on the permissive latitude.

Adversarial pass (original write-up, cross-language filter only): 51/58 testable committed tokens (88%) have no genuine cross-language competitor. After the 2026-09 rescore that also counts same-language homophones: **47/58 survive (81%)**, 11 falls (`ADVERSARIAL_RESULTS.md`, `gate2_rescore.csv`).

## Hardening outcome (master §9 tiers), prior epoch (pre-rescore)

Of 62 committed tokens as then published: **22 Hardened (H)** (pass strict decode + adversarial), **7 committed-with-competitor (C\*)**, **33 committed latitude-dependent (C)**. Hardened set then: akal, ascensionada, che', ek, -en, Eztli (Pilli), ich, k'áak', ki', kujkuali, k'ux, ma, máax, náach, pul, Ti, tul, u, uch', waaj, xefe, xi. (The battery first covered 61 tokens; *pul* "to throw, cast" was described as restored from the pre-import copy. **2026-09: no decode artifact for pul exists in this repository; that pass is dropped.**)

Those 22/62 figures used any-C Gate 1. They are retained only as the prior epoch. Current numbers: `STATISTICAL_SUMMARY.md` and `RESCORE_OUTPUT.md`.

## 2026-09 audit remediation (current)

Triggered by `FULL_AUDIT_2026-08-18.md` and `AUDIT_REVIEW_2026-08-18.md`. No new blind decoders. Existing CSVs rescored.

**Gate-1 count reconciliation.**

| Claim | Rebuilds from? | Decision |
|---|---|---|
| 23 Gate-1 passes of 62 | no. `strict_committed_results_batch*.csv` has 61 rows, 21 any-C | 21/61 is the legacy any-C count |
| 26 passes of 65 | 21 + pul + 3 Battery E names, with pul unproven | pul dropped; Battery E 3 names kept (exact lexemes, 15/15) |
| 26 `gate1_strict=pass` in the old 65-row CSV | 21 CSV-C + Eztli override + pul + 3 names | Eztli override kept: Battery D 5/5 C with matching *eztli*/blood, documented here. pul dropped. |

Where each remaining Gate-1 pass was decided: `gate1_rescore.csv` column `gate1_where`.

**Recovery scoring (F1).** 6 of the 21 any-C rows matched a different root, language, or sense (*akal* quarrel, *ek* wasp, *te* tree/locative, *tul* reed, *uch'* opossum, *xi* go). Protocol demotions: *k'ux* unexplained *-zeh*; *ma* dual bundle; *uch'* dual readings. Protocol-clean recovery passes on the 61-row set: **14**. Hardened after Gate 2: those 14 plus 3 Battery E names = **17 H of 78**.

**Null headline.** Withdrawn: 2 x 10^-15 / 12.2 sigma. Replacement: matched p ≈ 0.005 to 0.06 (`NULL_HONESTY_OUTPUT.md`). Sigma column removed (it reported count z-scores).

**Syntax.** Analyst-level 3/3 vs 0/2, p = 0.10, alongside the old rule-level 12/12 vs 0/8.

## Orthographic hardening of the correspondence rules

The §2.6 stylization rules were hardened as spelling correspondences (no audio; phonetic phonology is out of scope, master §2.6 scope note). This introduces no new run: the strict-versus-loose latitude the null model already varies IS the permissiveness of these rules. The old equation "23/62 Gate 1 = strict-safe spellings" used the withdrawn any-C pass set. After recovery scoring the protocol-clean Gate 1 set is 14/61. Full writeup: master §17.9, with the null-headline retraction in §17.3.

## Hardening of post-battery onomastic tokens (2026-07)

Three onomastic tokens added after the null-model battery were run through both gates per `HARDENING_PROTOCOL.md`:

| Token | Gate 1 (strict) | Gate 2 (adversarial) | Tier |
|---|---|---|---|
| Quecholli | pass (surface = attested Nah. *quecholli*, 14th veintena; no residue) | pass (no cross-language competitor) | H+L |
| Panquetzaliztli | pass (surface = attested Nah. *panquetzaliztli* = *pan* + *quetza* + *-liztli*; no residue) | pass | H+L |
| Ixchel | pass (Yuc. *Ix-* + *Chel* "rainbow"; the attested theonym Ix Chel; no residue) | pass (no equal-or-stronger different-language root; Nah. *ix-* "eye/face" has no source for *chel*) | H+L |

These three are onomastic (item and figure names). They remain H+L as exact attested lexemes (Battery E 15/15). They are 3 of the 17 current hardened rows, not an add-on to a 22/62 any-C core. The old 62/22 and 10^-15 figures are withdrawn (see 2026-09 section above).

The other new terms did not earn H: the strongbox artisans *Ixtolatl* and *Mahuatzi* and the pre-existing *Mahuxotl* fail Gate 1 (an unresolved medial or a contraction with residue), so they stay Soft (master §12.7); the Vaal Temple trio *K'aj Y'ara'az / K'aj Q'ura / K'aj A'alai* has no clean whole-name attested root and stays Open (master §12.8).

**Enlarged-base figures (withdrawn as headline).** The 2026-07 arithmetic (22/62 to 25/65; 23/62 p about 2 x 10^-15 with a ~12.2 count-z "sigma"; 26/65 p about 3 x 10^-18) is kept only as the prior published epoch. It used any-C scoring and an unselected 4.6% floor. Current hardened share is 17/78. Sigma labels are not normal-tail equivalents and are not reused.

**Update (Battery E, 2026-07).** The three names were run as blind plants under the same strict-and-online conditions across all five seeds (`BATTERY_E_RESULTS.md`): 15/15 Gate-1 passes (Quecholli 5/5, Panquetzaliztli 5/5, Ixchel 5/5), with the real controls calibrating (naach 5/5, ek 4/5 including one wasp reading, kutsen 1/5, sakilja 0/5, kilya 0/5). The names stay H+L. They do not restore an unconditional 10^-15 null rejection. The distractor false-positive rate (10/60) remains logged for transparency. *ek* as a control is itself no longer H in the lexicon (Gate 1 recovery failed: wasp vs star/dark).

## Task status

Batteries A-E remain the historical experimental record. 2026-09 remediation (scorer F1/N3, count reconciliation, withdrawn 10^-15 headline) is in `RESCORE_OUTPUT.md` and `NULL_HONESTY_OUTPUT.md`. Remaining debt: full-pipeline unique-string null; blinded syntax re-run; pending gates on the 13 former L-only rows.

## Reproduce / resume

- Regenerate any null-model worksheet: `python3 gen_set.py <seed>` (seeds above).
- Re-score a battery (legacy any-C plus recovery TPR): `python3 score.py <results.csv> <key.csv>`.
- Rescore Gate 1 / rewrite `token_classification.csv`: `python3 rescore_gate1.py`.
- Rescore Gate 2: `python3 score_adversarial.py`.
- Selection-matched p and pseudo de-duplication: `python3 null_honesty.py`.
- Per-token hardening test for future tokens: `HARDENING_PROTOCOL.md`.
