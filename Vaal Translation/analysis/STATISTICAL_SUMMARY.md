# Statistical summary and confidence interval for the translation

**Status of this file.** Headlines below are from the 2026-09-16 experimental pass. They match master §1 and §17. Older 2026-07 files, and a 2026-08/09 rereading of those files, stay on disk as history; they are not mixed into these counts.

**Headline (live only).** Texts and transcriptions are stable. Interpretive confidence is thin.

Pessimistic: 0.7% of the lexicon hardened (lower 95% bound); declared-sense chance test p = 1. Average: **2 of 78 hardened (2.6%)**, *xefe* and *Quecholli*. Optimistic: 8.9% hardened (upper 95% bound). Exact match, both arms (method-notes / dictionaries-only): pessimistic 7.4% / 5.8%; average 10.6% / 8.6%; optimistic 15.0% / 12.7%. Match or partial: pessimistic 24.2% / 23.1%; average 29.4% / 28.2% (about 29%); optimistic 35.3% / 34.1%. Secure: pessimistic and average 0/51 = 0.0%; optimistic 7.0%. Working: pessimistic 14.0%; average 23.5%; optimistic 36.8%. Chance tests are a yes/no result: even any-hit fails to reject at 0.05 (p = 0.09494 trial / 0.3069 item). Grammar is a single small-sample test (3/3 vs 0/2, p = 0.10), not a range. *Ixchel* is C+L (herb string, approved Godstealer gloss unchanged). Historical / withdrawn displays (10^-15 headlines, PPV tables, per-line bands) are not current; see master §17.10.

Proportions carry Wilson 95% confidence intervals. Underlying data: `token_classification.csv`, `gate1_rescore_rerun.csv`, `gate2_rescore_rerun.csv`, `NULL_MODEL_RESULTS_RERUN.md`, `BATTERY_E_RERUN.md`, `EXPERIMENT_LOG.md`, `SYNTAX_EXPERIMENT_LOG_RERUN.md`, `TRANSLATION_BATTERY_RESULTS.md`, `SECURE_LINE_TAGS.md`, `LEAVE_ONE_TEXT_OUT.md`.

Agreed lexicon population: **78 section-9 rows**, each with an H/C/S/O status. L is a tag only. Battery-tested Gate 1 is the **61-row** `strict_committed_results_rerun_batch*.csv` set. *pul / puul* now has a decode artifact (Gate 1 recovery yes, Gate 2 fall, tier C*). Battery E: *Quecholli* 5/5 recovery (H+L), *Ixchel* 5/5 on the Cordemex herb string (not the approved theonym; Gate 1 miss, now C+L), *Panquetzaliztli* 0/5 (absent from attached dicts). *ek* is a C control, not H.

| Population | N tokens | N distinct roots | Hardened (H) | Share (token) | 95% CI |
|---|---:|---:|---:|---:|---|
| Strict-CSV battery (ids 1-61) | 61 | 52 | 1 | 1.6% | [0.3, 8.7] |
| Battery-tested + Battery E names (enlarged) | 64 | 55 | 2 | 3.1% | [0.9, 10.7] |
| Section 9 lexicon (agreed, all 78 gated) | 78 | 69 | 2 | 2.6% | [0.7, 8.9] |

Old headlines (22 H of 62; 17 H of 78 stopgap; 23/62 vs a 4.6% floor) do not rebuild from the re-run CSVs. They are retained only as prior epochs.

## 1. Committed lexicon, current tier distribution

Reported on two bases: per token (every attested surface form the translations use) and per distinct root (morphological relatives collapsed to their shared lemma, §7a). Both are kept; neither supersedes the other. Tiers are from `token_classification.csv` after the re-run Gate 1 (recovery against the predeclared root, language class, and sense) and Gate 2 (different-meaning competitor, including same-language homophones). HARDENING_PROTOCOL violations stay out of H (*k'ux* residue, *ma* dual bundle, *uch'* dual readings).

**Per token (N = 61, battery-tested):**

| Tier | Count | Proportion | 95% CI |
|---|---:|---:|---|
| Hardened (H / H+L) | 1 | 1.6% | [0.3%, 8.7%] |
| Committed + competitor (C*) | 24 | 39.3% | [28.1%, 51.9%] |
| Committed, latitude-dependent (C / C+L) | 36 | 59.0% | [46.5%, 70.5%] |

**Per distinct root (N = 52, same 61 tokens, §7a grouping):**

| Tier | Count | Proportion | 95% CI |
|---|---:|---:|---|
| Hardened (H / H+L) | 1 | 1.9% | [0.3%, 10.1%] |
| Committed + competitor (C*) | 23 | 44.2% | [31.6%, 57.7%] |
| Committed, latitude-dependent (C / C+L) | 28 | 53.8% | [40.5%, 66.7%] |

The per-root H count stays 1 because *xefe* is not in a merge family. *te* (C*) and *Ti* (C*) collapse into one C* family, so C* drops by one. After the 2026-09-16 tournaments, four of the five new stars sit in the 61-row frame (*ik'el, 'Ibil, mucane, kifba*); *Tzokan'te* is outside it (id 75).

**Section 9, N = 78 (the table a reader consults):**

| Tier | Count | Notes |
|---|---:|---|
| Hardened (H / H+L) | 2 | both gates, protocol-clean (*xefe*; *Quecholli* H+L) |
| Committed + competitor (C* / C+L*) | 30 | Gate 2 fall plus 2026-09-16 tournaments (five new stars: *ik'el, 'Ibil, mucane, kifba, Tzokan'te*) |
| Committed, latitude-dependent (C / C+L) | 45 | includes former L-only rows now gated; *Ixchel* C+L after Gate 1 sense miss; *pul* is C* |
| Soft (S+L) | 1 | *Xatlene* (own note: one unresolved vowel step) |

L is never a lone tier. Per distinct root on this frame: **2 H of 69 = 2.9% [0.8, 10.0]** (same grouping; *pul* and the 13 former L-only rows each add a distinct root; the three Battery E names each add a distinct root).

Gate pass rates on both bases (61-row strict CSV, recovery scoring, not legacy any-C):

| Gate | Per token (N = 61) | Per distinct root (N = 52) |
|---|---|---|
| Gate 1, legacy any-C | 22/61 = 36.1% [25.2, 48.6] | not used as a headline |
| Gate 1, committed-root/lang/sense recovery | 4/61 = 6.6% [2.6, 15.7] (*k'áak'*, *náach*, *tul*, *xefe*) | 4/52 = 7.7% [3.0, 18.2] |
| Gate 1, protocol-clean recovery | 4/61 = 6.6% [2.6, 15.7] (the three protocol flags are recovery-no) | 4/52 = 7.7% [3.0, 18.2] |
| Gate 2, different-meaning competitor (any language) | 38 survive / 58 testable = 65.5% [52.7, 76.4] (3 names N/A) | 30 survive / 49 testable = 61.2% [47.2, 73.6] |

On the 78-row frame: Gate 1 recovery **6/78 = 7.7% [3.6, 15.8]** (adds *pul*, *Quecholli*; *Ixchel* is a sense miss); protocol-clean the same 6. Gate 2: **50 survive / 75 testable = 66.7% [55.4, 76.3]** per token, **42/66 = 63.6% [51.6, 74.2]** per distinct root.

Reading: a handful of rows reconstruct under recovery-scored strict rules. About two thirds of testable rows have no different-meaning competitor **written by this lookup**. That is the protocol's certification rate after the re-run, not a direct measure of gloss correctness. Decoder C labels often attach a different sense or language than `committed_readings.csv` (the F1 hole, re-measured).

Hardened readings that survive both gates and the protocol, 2 of 78: *xefe, Quecholli*.

Demoted from the stopgap H list (not new etymologies; decoder mismatch, Gate 2 fall, or coverage miss): *ascensionada, che', -en, Eztli Pilli, ich, k'áak', ki', kujkuali, máax, náach, Ti, u, waaj, Panquetzaliztli*. *pul / puul* now has an artifact (C*). Stopgap demotions that remain demoted: *akal, ek, tul, uch', xi, k'ux, ma*.

*Ixchel* demotion: attached Cordemex prints a medicinal-herb gloss on the string *ix chel*. The approved frozen sense is the theonym / Godstealer reading. Herb ≠ that sense, so Gate 1 fails. Tier C+L. Gloss text unchanged.

## 2. Null-model error rates (pooled, 500 pseudo + 150 real per battery), 95% CI

Pooled Batteries A-D re-run (`NULL_MODEL_RESULTS_RERUN.md`). Distinct strings = 500 trials. Decoder: form-first lookup (`dict_lookup.py`, `decode_blind.py`) over attached Maya / Spanish-Maya dictionaries, plus Nahuatl/Nawat wordlists as the B/D extra lexicon. No live web.

**Legacy any-C** (any committed-quality dictionary match):

| Battery | FPR(C) | TPR(C), any-root |
|---|---|---|
| A loose / offline | 12.8% [10.2, 16.0] | 36.7% [29.4, 44.6] |
| B loose / online | 13.6% [10.9, 16.9] | 36.7% [29.4, 44.6] |
| C strict / offline | 6.4% [4.6, 8.9] | 23.3% [17.3, 30.7] |
| D strict / online | 6.8% [4.9, 9.4] | 23.3% [17.3, 30.7] |

**Recovery TPR** (real arm must match `committed_readings.csv` on root, language class, and sense). Pseudo C remains a false positive.

| Battery | Recovery TPR | n real (5 unscorable *Otsuks*) |
|---|---|---|
| A, B, C, D | 5/150 = 3.3% | *Otsuks* has no committed_readings row |

Distinct-string FPR (primary noise floor): A 64/500 = 0.128; C 32/500 = 0.064; D 34/500 = 0.068. Cross-seed nonce repeats: none.

The four batteries form a latitude x online-access 2x2. Adding the Nahuatl extra lexicon under strict rules (D vs C) moves FPR 6.4 to 6.8% and leaves TPR flat at 23.3% any-C / 3.3% recovery. Discrimination does not widen. Latitude still dominates.

**Withdrawn as a headline (not as a historical record).** The claim that 23 of 62 (or 26 of 65) strict passes against a 4.6% floor gives p about 2 x 10^-15 (quoted as ~12.2 sigma) is invalid on three independent grounds, as in the stopgap writeup. Sigma labels stay removed.

**Selection-matched, from this re-run (`NULL_MODEL_RESULTS_RERUN.md`):**

| Comparison | Real | Pseudo | Fisher one-sided p |
|---|---|---|---:|
| Matched A-then-D, trial level (any-C) | 35/55 | 32/64 | **0.09494** |
| Matched A-then-C offline, trial level | 35/55 | 32/64 | 0.09494 |
| Matched, item level (any-C) | 7/11 | 32/64 | **0.3069** |
| Recovery-scored matched, trial | 5/55 | 32/64 | **1** |
| Recovery-scored matched, item | 1/11 | 32/64 | **0.9991** |
| Stopgap matched range (2026-07 any-C files) | see `NULL_HONESTY_OUTPUT.md` |  | about 0.005 to 0.06 (historical) |

Conditioning on selection, this epoch does not reject the null at conventional 0.05. Recovery scoring removes the remaining apparent signal. The method finds dictionary strings; it does not recover the project's glosses at a rate that beats the same-filter noise arm.

## 3. Confidence in the translation (positive predictive value)

**Withdrawn / not for interpretation.** These PPV tables are archived so the old method stays inspectable. They are not current translation confidence. Do not quote them as the probability that an English gloss is right. Live figures are the hardened-share counts, the chance-check p-values, the translation-battery Wilson intervals, the secure-line grades, and the leave-one-text-out grades in master §17.

**Separate quantity: inter-translator / vs-gold agreement.** Blind line translations of the 51-line closed corpus (Texts 1-4 plus Kamasan Smith) under methodology-on (T-M) versus dictionaries-only (T-D) are scored in `TRANSLATION_BATTERY_RESULTS.md`. Those Wilson CIs are not PPV and are not the withdrawn sentence bands. T-M match 27/255 = 10.6% [7.4, 15.0]; T-D 22/255 = 8.6% [5.8, 12.7]. Match+partial 75/255 = 29.4% [24.2, 35.3] versus 72/255 = 28.2% [23.1, 34.1]. T-M minus T-D match+partial bootstrap CI includes zero. Methodology is not moving the needle on vs-gold line agreement. It cuts clash (T-M 54.5% vs T-D 67.5%) and raises abstain (16.1% vs 4.3%). Clash/abstain CIs and labeled exploratory tables (per-text, hotspots, kappa) are in the same results file. Post-hoc rival-reading tournaments on the 16 dual 5/5-clash lines: `RIVAL_READING_TOURNAMENTS.md` (five new C* stars; H is 2 of 78 after the Ixchel Gate 1 honesty pass). Particle probes: `PARTICLE_PROBES_3_7.md`. Secure-line grades on the same 51 published English lines (editorial stress test, not PPV): 0/51 secure (0.0% [0.0, 7.0]), 12/51 working = 23.5% [14.0, 36.8], 38/51 fragile = 74.5% [61.1, 84.5], 1/51 opaque-blocked (`SECURE_LINE_TAGS.md`). Leave-one-text-out: ok 12/51 = 23.5% [14.0, 36.8], ok or partial 33/51 = 64.7% [51.0, 76.4], T3 0/13 ok (`LEAVE_ONE_TEXT_OUT.md`). Family-audit grouping footnotes: `MORPHOLOGICAL_FAMILY_AUDIT.md` (headline distinct-root N unchanged). *Panquetzaliztli* compound pass: missing whole form, stays C+L (`ONOMATIC_COMPOUND_PASS.md`). *Ixchel* is C+L (herb ≠ approved theonym). Transcriptions and corpus documentation are stable; these line-level rates are the current measured statements about translation confidence.

The question the formula answers, per reading, is the **positive predictive value (PPV)**: given that a token was certified (committed / hardened), the probability it is a genuine root rather than a chance dictionary coincidence.

PPV = (TPR x b) / (TPR x b + FPR x (1 - b)), where **b** is the base rate: the prior probability that any given Vaal token was actually built from a real root (as opposed to invented phonaesthetic filler). **b is the one quantity we cannot measure** (it depends on GGG's undocumented design process), so PPV is reported across a plausible range.

**Hardened tier** (strict bar, Battery D rates TPR = 0.140, FPR = 0.046, strict + online, **legacy any-C from the 2026-07 archive**). **Withdrawn as translation confidence:**

| base rate b | PPV (diagnostic only; not current gloss confidence) |
|---|---|
| 20% | 43% |
| 30% | 57% |
| 40% | 67% |
| 50% | 75% |
| 60% | 82% |
| 70% | 88% |
| 75% | 90% |

**Whole committed lexicon** (loose bar, Battery A rates TPR = 0.207, FPR = 0.062, archive): PPV runs about 59% (b = 30%) to 89% (b = 70%). **Withdrawn as translation confidence.**

The C > H inversion at the same prior is a specification error, not a finding about the language.

## 4. Headline confidence interval

Two defensible statements, one assumption-free and one model-based:

1. **Assumption-free (measured, re-run 2026-09-16, Ixchel honesty):** the hardened core of the battery-tested lexicon is **1.6%, 95% CI [0.3%, 8.7%]** per token (1 of 61), or **1.9%, 95% CI [0.3%, 10.1%]** counted over the 52 distinct roots (§7a). On the section-9 table a reader consults it is **2.6% [0.7, 8.9]** (2 of 78) per token, or **2.9% [0.8, 10.0]** (2 of 69) per distinct root. On the enlarged base (61 + three Battery E names) it is **3.1% [0.9, 10.7]** (2 of 64) per token, or **3.6% [1.0, 12.3]** (2 of 55) per distinct root. This is the protocol's certification rate, not a direct measure of gloss correctness. The stopgap 17/78 figure is historical.

2. **Model-based (per-reading confidence): withdrawn as translation confidence.** Recompute only if a non-circular b and recovery-scored PPV are both accepted; until then leave pending.

3. **Inter-translator / vs-gold (measured, not PPV):** see `TRANSLATION_BATTERY_RESULTS.md`. Do not mix that table with the certification rates in (1) or the withdrawn PPV in (2).

## 5. Two honest caveats

- **Sentence-level confidence compounds downward.** Independence products are **withdrawn as a reported floor** (they are not a Frechet lower bound: that bound is max(0, sum p_i - n + 1)). Keep the worked structure in §6 with those labels; do not quote the percentages as current results. (`AUDIT_REVIEW` O3 / F7.)
- **PPV is only as good as the base rate, and only as good as the question.** This re-run's recovery TPR (3.3%) answers "did the form-first lookup recover this row's declared gloss," not "is Vaal built from palette roots." Until an exact-root validation set with a non-circular b exists, do not convert those rates into translation confidence.

## 6. Per-tier confidence and a worked sentence example

**Withdrawn as translation confidence.** Structure retained; inputs are the legacy any-C rates of §3 (archive).

Per-reading confidence (PPV) by tier, using each tier's measured TPR/FPR:

| Tier | Neutral prior (b=50%) | Range b=30-70% | basis |
|---|---|---|---|
| Hardened (H) | 75% | 57-88% | strict bar (TPR 0.140 / FPR 0.046, Battery D strict+online), **legacy any-C archive** |
| Committed, latitude-dependent (C) | 77% | 59-89% | loose committed bar (0.207 / 0.062) |
| Committed + competitor (C*) | ~50% for the specific gloss | root genuine ~77%, split by a comparable competitor | as C, discounted by the logged competitor |
| Soft / candidate (S) | 53% | 33-73% | loose found bar (0.767 / 0.670); near a coin-flip |

Worked sentence example, the Kamasan Smith line *Ti ek tala jare'yantul!* "Into the dark you come; and so, your waning!" (6 tokens). **Withdrawn as translation confidence.** After this re-run none of *Ti, ek, tul* is H; *yan* is not a lexicon row.

Best/worst real lines remain **withdrawn as translation confidence**. Tokens that remain H are a Spanish loan (*xefe*) and one exact attested name-string (*Quecholli*). *Ixchel* is C+L.

## 7. The base rate b, estimated from data (not assumed)

b (fraction of Vaal built from real palette roots) is the dominant uncertainty in the PPV. Bounding it empirically. The name-roster proxy is unchanged as a descriptive count of naming behaviour. It is circular as an input to a PPV that already uses the same method, and it is not used here to produce a current translation-confidence interval.

- **Proper-noun proxy (palette-scoped).** The §12 roster is a closed, un-cherry-pickable sample. Four figures are documented out-of-palette borrowings (Apep, Ralakesh, Arakaali, Omnitect) and are out of scope. Among the **33 in-scope names, 19 carry an attested palette root: about 58%.** Many rest on chance-resistant structural markers (the Nahuatl -tl/-tli/-atl absolutives). Pessimistic: clean-parse-only floor about 15-18%. Average: 19 of 33 = about 58% (soft-inclusive). Optimistic: the upper 95% bound on that same 19/33 count is 72.8%; the roster is not stretched to 75%. Folding the 4 borrowings back into the denominator gives 19/37 about 51%, but that penalizes b for design choices outside the palette's scope and is not used as any of the three readings.
- **Mixture model b=(O - FPR)/(TPR - FPR): not usable here.** Using re-run recovery TPR (0.033) and D FPR (0.068) with O = 2/78 also fails as a translation diagnostic: O and TPR still answer overlapping questions once the same lookup writes both the lexicon and the plants.
- **Consequence:** the palette-scoped proxy puts b about 58% (above the 50% neutral prior). Conversion into a hardened PPV is **withdrawn as translation confidence**. Optimistic on the roster count is the 72.8% upper bound on 19/33, not a stretch to 75%.

## 7a. Non-independence of related tokens (distinct-root recount)

The per-token counts treat each committed token as an independent trial, which overstates the evidence where several tokens share a root (e.g. *ik'bala*, *ikba'yucane*, *Ik'eche*, *ik'el* are all reflexes of Yucatec *ik'* "spirit, breath"). Merging tokens that share the same §9 head root (shared affixes like *-ba'* or *-ane* do not merge distinct heads) collapses 16 of the 61 battery tokens into 7 families, leaving **52 distinct roots**. *pul* is now in the 78-row frame as a distinct head (C*).

| Root | Tokens merged | Gate 1 (recovery, re-run) |
|---|---|---|
| *ik'* "spirit, breath" | ik'bala, ikba'yucane, Ik'eche, ik'el | all fail |
| *aocmo* "no more" | Aiokmo, 'Ayok | all fail |
| *ātl* "water" | atla, Atziri | all fail |
| *el* "burn" | Ela, elba | all fail |
| *muk'* "strength" | mucane, mujuk' | all fail |
| *k'ex* "transform" | Kextal, qexcan | all fail |
| *ti' / te'* relational | te, Ti | both fail (Gate 2 fall; Gate 1 sense/lang mismatch) |

Only *xefe* is protocol-clean H in the 61-row frame, and it is not in these families, so collapsing removes no H (1 stays 1) but nine mostly-failing forms from the denominator. *te* and *Ti* are both C* and collapse to one C* family.

**Results on both bases (re-run).**

| Metric | Per token (N=61) | Per distinct root (N=52) |
|---|---|---|
| Strict Gate-1 protocol-clean | 4 | 4 |
| Strict Gate-1 recovery (incl. protocol-flagged) | 4 | 4 |
| Null-rejection p (unconditional vs 4.6% floor) | withdrawn as headline | withdrawn as headline |
| Null-rejection p (selection-matched, any-C re-run) | trial 0.09494; item 0.3069 | not a separate distinct-root Fisher (A-D items already unique strings) |
| Null-rejection p (recovery-scored matched) | trial p = 1; item p = 0.9991 | same |
| Hardened tier | 1.6% [0.3, 8.7] | 1.9% [0.3, 10.1] |
| Gate-1 protocol-clean | 6.6% [2.6, 15.7] | 7.7% [3.0, 18.2] |
| Gate-2 adversarial | 65.5% [52.7, 76.4] (38/58) | 61.2% [47.2, 73.6] (30/49) |
| Tier split H / C* / C | 1 / 24 / 36 | 1 / 23 / 28 |

**Reading.** The dependency correction does not restore a large hardened core. Related tokens are concentrated in failing families, so the per-root H share rises only from 1.6% to 1.9%. The recount is defensive, not promotional. It does not restore a 10^-15 unconditional floor test.

**Both bases are kept on purpose.** The per-token figures are not superseded. They are the honest raw account of how the committed lexicon behaves form by form; the per-root figures are the honest account of how it behaves lemma by lemma. Neither is privileged. Where a single headline number is needed, the per-token figure is quoted first with the per-root figure beside it.

The 500-trial pseudo arm in this epoch is de-duplicated: **500 distinct strings of 500**. Ordinary Spanish exact hits on the loan palette are labelled Spanish C, not pure noise; the generator also excluded those strings from the pseudo arm. Distinct-string Battery D FPR is 34/500 = 6.8%.

**Grouping appendix (family audit 2026-09-16).** Shared pieces that are not both rows' heads are footnotes, not merges (`MORPHOLOGICAL_FAMILY_AUDIT.md`). *tul* / *pul* stay two roots. Forcing *Tzokan'te* into *cha'tsoke* would move 69 to 68; not adopted. Headline N stays 52 / 55 / 69. *ikba'yucane* leftover *yuc* is residue, still in the *ik'* family.

## 8. Syntax (analyst-level)

**Current (gloss-blind, 2026-09-16).** Three real-panel analysts vs two scrambled-panel analysts (seed 1729). Packets: surface lines only plus a form-only token list (no English glosses). Recovery rule: consistent linear order at medium or high confidence on at least two of the four word-order questions. Table: **3/3 vs 0/2, Fisher one-sided p = 0.10**, not significant. N = 5; small N. Do not publish a rule-level table as the p-value. Qualitative match to the six §3 conclusions is weaker than SYN-1 (possession undetermined for two of three real analysts). Copula and affix-edge findings are order-independent, not linear-syntax evidence. Full run: `SYNTAX_EXPERIMENT_LOG_RERUN.md`. Particle/order probes on the six §3.7 items: `PARTICLE_PROBES_3_7.md` (leaning or still open; possession not upgraded).

**Historical 2026-07 (not gloss-blind).** The published 12/12 vs 0/8 Fisher (p about 7.9 x 10^-6) treats four correlated rules per analyst as independent trials. At the experimental unit the table is **3/3 vs 0/2, Fisher p = 0.10**, not significant. Analysts received surface lines, English translations, and a token glossary. (`SYNTAX_EXPERIMENT_LOG.md`, AUDIT_REVIEW F8.) Same counts as the gloss-blind table do not make that panel gloss-blind.

## 9. Reproduce (re-run files; archives unchanged)

```
python3 score.py --rerun
python3 null_honesty.py --rerun
python3 rerun_score_pool.py
python3 run_gates_rerun.py
python3 run_battery_e_rerun.py
python3 score_loto_secure.py
```

Default `score.py`, `rescore_gate1.py`, `score_adversarial.py`, and `null_honesty.py` still point at the 2026-07 archives unless `--rerun` is passed. Do not mix epochs. Re-run plan: `EXPERIMENT_RERUN_PROTOCOL.md`.
