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
| Syntax confirmation (historical, 2026-07) | independent derivation + scrambled control | 1729 (scramble) | 3 real + 2 scrambled analysts | `SYNTAX_EXPERIMENT_LOG.md` |
| Syntax confirmation (gloss-blind re-run) | same, surface lines and form-only tokens only | 1729 (scramble) | 3 real + 2 scrambled analysts | `SYNTAX_EXPERIMENT_LOG_RERUN.md` |
| Translation batteries T-M / T-D | T-M methodology on vs T-D dictionaries only; vs-gold + inter-translator CIs | same 5 | 5 translators x 51 lines each battery | `TRANSLATION_BATTERY_RESULTS.md`, `translation_battery_T{M,D}_s{seed}.csv` |

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

**Enlarged-base figures (provisional third base, stopgap).** The 2026-07 any-C arithmetic (22/62 to 25/65; 23/62 p about 2 x 10^-15 with a ~12.2 count-z "sigma"; 26/65 p about 3 x 10^-18) is the prior published epoch and is not a current headline. Sigma labels are not reused. Recovery-scored third-base counts (61/52 battery, 64/55 enlarged, 78/69 section 9) are in master §17.7. Battery E re-run under the new protocol is pending (`EXPERIMENT_RERUN_PROTOCOL.md`).

**Update (Battery E, 2026-07).** The three names were run as blind plants under the same strict-and-online conditions across all five seeds (`BATTERY_E_RESULTS.md`): 15/15 Gate-1 passes (Quecholli 5/5, Panquetzaliztli 5/5, Ixchel 5/5), with the real controls calibrating (naach 5/5, ek 4/5 including one wasp reading, kutsen 1/5, sakilja 0/5, kilya 0/5). The names stay H+L. They do not restore an unconditional 10^-15 null rejection. The distractor false-positive rate (10/60) remains logged for transparency. *ek* as a control is itself no longer H in the lexicon (Gate 1 recovery failed: wasp vs star/dark).

## 2026-09-16 re-run (true remediation)

Protocol: `EXPERIMENT_RERUN_PROTOCOL.md`. Decoder: form-first lookup over attached text dictionaries (`dict_lookup.py`, `decode_blind.py`). Seeds 1729, 9001, 271828, 42, 55555. 2026-07 archive filenames were not overwritten.

**Generator.** `generate_pseudo_vaal.py --rerun` / `gen_set.py --rerun`: 500 distinct pseudo strings of 500 trials; corpus-token and long-substring rejection (leak list including *eztl*, *noche*, *ko'ja*); Spanish loan-palette hits labelled Spanish, not pure noise. Files: `pseudo_vaal_test_set_rerun.txt`, `blind_test_worksheet_rerun_s{seed}.csv`, `blind_test_key_rerun_s{seed}.csv`. Prerun freeze: `token_classification_prerun.csv`.

**Batteries A-D.** Complete 5 x 4 x 130 sheets with found / confidence / root / lang / gloss / residue / notes. Result files: `blind_test_results_rerun_s{seed}.csv`, `_online_`, `_tight_`, `_tight_online_`. Pooled (`NULL_MODEL_RESULTS_RERUN.md`):

| Battery | FPR(C) | TPR(C) any-root | TPR(recovery) |
|---|---|---|---|
| A loose/offline | 0.128 | 0.367 | 0.033 |
| B loose/online | 0.136 | 0.367 | 0.033 |
| C strict/offline | 0.064 | 0.233 | 0.033 |
| D strict/online | 0.068 | 0.233 | 0.033 |

Distinct-string FPR primary: A 64/500, C 32/500, D 34/500. Matched A-then-D any-C: trial p = 0.09494 (35/55 vs 32/64), item p = 0.3069 (7/11 vs 32/64). Recovery-scored matched: trial p = 1, item p = 0.9991. *Otsuks* unscorable (not in `committed_readings.csv`).

**Battery E.** `BATTERY_E_RERUN.md`, `battery_e_rerun_raw.md`. Fresh unique pseudos. *Quecholli* 5/5 recovery, *Ixchel* 5/5 (Cordemex herb-string on the lexeme form), *Panquetzaliztli* 0/5 (not in attached dicts). Controls: *naach* 5/5 recovery, *ek* 0/5 recovery / 5/5 any-C wasp (C, not H), *kutsen* 0/5 recovery / 5/5 any-C, *sakilja* 0/5, *kilya* 0/5. Distractors 1/60 C.

**Gate 1 lexicon.** 78/78 rows in `strict_committed_results_rerun_batch{1-4}.csv` and `gate1_rescore_rerun.csv`. Recovery yes: 7/78 (*k'áak'*, *náach*, *tul*, *xefe*, *pul / puul*, *Quecholli*, *Ixchel*). Protocol-clean the same 7. On the 61-row frame: 4/61. *pul* now has an artifact (no longer `no_artifact`).

**Gate 2.** 78/78 in `adversarial_results_rerun_batch{1-4}.csv` and `gate2_rescore_rerun.csv`. Survive 50 / 75 testable (38/58 on ids 1-61). Same-language competitors on.

**Hardening.** `token_classification.csv` rewritten after both gates (prerun snapshot preserved). H = 3 of 78: *xefe*, *Quecholli* H+L, *Ixchel* H+L. Dual-base: 1/61 and 1/52 on the battery frame; 3/64 and 3/55 enlarged; 3/78 and 3/69 section 9.

**Syntax.** Gloss-blind panel on disk: `SYNTAX_EXPERIMENT_LOG_RERUN.md`. Analyst-level 3/3 vs 0/2, Fisher p = 0.10 (not significant; N = 5). Historical 2026-07 3/3 vs 0/2 p = 0.10 is not gloss-blind.

**Docs.** `STATISTICAL_SUMMARY.md` and master §17 updated from these files only. Stopgap archive numbers stay labelled historical.

## 2026-09-16 syntax panel (gloss-blind)

Protocol: `EXPERIMENT_RERUN_PROTOCOL.md` Syntax panel, `SYNTAX_CONFIRMATION_PROTOCOL.md`. Packets: `syntax_rerun_corpus_real.txt` (51 surface lines, English stripped), `syntax_rerun_tokens_form_only.csv` (no glosses), `syntax_rerun_corpus_scrambled_s1729.txt` (within-line shuffle, seed 1729), `syntax_rerun_brief.md`. Builder: `syntax_rerun_build_packets.py`.

Real panel: analysts A, B, C. Scrambled panel: D, E (not told the corpus was scrambled). Isolation: each pass opened only copies of the three packet files. Sheets: `syntax_rerun_analyst_{A,B,C}_real.md`, `syntax_rerun_analyst_{D,E}_scrambled.md`. Scoring against the six §3 conclusions was done after all sheets existed.

Analyst-level 2x2 (recovered consistent word-order regularities): 3/3 real vs 0/2 scrambled. Fisher one-sided p = 0.10. Small N. Not significant. Qualitative match to §3 is weaker without English (possession undetermined for A and B). Copula and affix findings are order-independent. Historical SYN-1 3/3 vs 0/2 p = 0.10 remains labelled not gloss-blind. Full writeup: `SYNTAX_EXPERIMENT_LOG_RERUN.md`. PPV / sentence bands stay withdrawn as translation confidence.

## 2026-09-16 translation batteries T-M / T-D

Protocol: `TRANSLATION_BATTERY_PROTOCOL.md`. Closed 51-line surface corpus (Texts 1-4 plus Kamasan Smith), same packet as `syntax_rerun_corpus_real.txt`. Seeds 1729, 9001, 271828, 42, 55555. Five independent translators per battery.

T-M: surface + methodology packet (form-first / palette / HARDENING_PROTOCOL / TIGHTENED_LATITUDE) + dictionaries. T-D: surface + dictionaries only. Blind to published English, §9, `committed_readings.csv`, other sheets, §17 answers, and gold. Gold extracted after all ten sheets existed (`translation_battery_extract_gold.py`). Dictionaries never committed.

Headlines are Wilson 95% CIs, not Fisher / 10^-15 tests (`TRANSLATION_BATTERY_RESULTS.md`):

- T-M match 27/255 = 10.6% [7.4, 15.0]; match+partial 75/255 = 29.4% [24.2, 35.3]
- T-D match 22/255 = 8.6% [5.8, 12.7]; match+partial 72/255 = 28.2% [23.1, 34.1]
- T-M minus T-D match +0.020 [-0.031, +0.071]; match+partial +0.012 [-0.067, +0.090] (bootstrap 10,000 line-slots)
- Pairwise no-gold compatibility: T-M 247/510 = 48.4% [44.1, 52.8]; T-D 237/510 = 46.5% [42.2, 50.8]

Methodology did not raise vs-gold match+partial on this corpus. T-M abstains more; T-D clashes more (Spanish-gloss drift on line 9: cacao-tree vs life). PPV / sentence bands stay withdrawn as model-based translation confidence; these CIs are vs-gold / inter-translator agreement under this kit.

## Task status

Re-run Batteries A-E, Gate 1, Gate 2, the gloss-blind syntax panel, and translation batteries T-M / T-D are on disk. Dual-base tables in master §17.5-17.7 and `STATISTICAL_SUMMARY.md` follow the re-run CSVs. Syntax p, if quoted, is analyst-level and gloss-blind: 3/3 vs 0/2, p = 0.10 (`SYNTAX_EXPERIMENT_LOG_RERUN.md`). Line-level translation agreement CIs: `TRANSLATION_BATTERY_RESULTS.md`. PPV / sentence bands remain withdrawn as translation confidence. The 2026-07 files and the 2026-09 stopgap rescore stay as the historical record. Do not mix epochs.

## Reproduce / resume

- Regenerated re-run worksheets: `python3 gen_set.py --rerun <seed>` (default without `--rerun` still writes archive names and will refuse to overwrite them).
- Re-score a re-run battery: `python3 score.py --rerun` or `python3 score.py <rerun results.csv> <rerun key.csv>`.
- Pooled A-D: `python3 rerun_score_pool.py` / `python3 null_honesty.py --rerun`.
- Gate 1+2 lexicon re-run: `python3 run_gates_rerun.py` (writes `*_rerun_*.csv`; does not overwrite 2026-07 batches).
- Battery E re-run: `python3 run_battery_e_rerun.py`.
- Archive stopgap (do not mix): `python3 rescore_gate1.py`, `python3 score_adversarial.py`, `python3 null_honesty.py`.
- Per-token hardening test: `HARDENING_PROTOCOL.md`.
- Protocol: `EXPERIMENT_RERUN_PROTOCOL.md`.
- Gloss-blind syntax packets: `python3 syntax_rerun_build_packets.py`. Log: `SYNTAX_EXPERIMENT_LOG_RERUN.md`.
- Translation batteries T-M / T-D: `python3 translation_battery_extract_gold.py` then `python3 score_translation_battery.py`. Protocol: `TRANSLATION_BATTERY_PROTOCOL.md`. Results: `TRANSLATION_BATTERY_RESULTS.md`.
