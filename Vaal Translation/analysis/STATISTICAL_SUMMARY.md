# Statistical summary and confidence interval for the translation

**Status of this file.** The 2026-08/09 audit and recovery rescore are a **STOPGAP**. They retier archived experiments; they are not a full re-run. True remediation is the protocol in `EXPERIMENT_RERUN_PROTOCOL.md` (Batteries A-E with recovery Gate 1, same-language Gate 2, de-duplicated null, syntax gloss-blind and analyst-level). Do not read the withdrawn 10^-15 headlines as "the experiments were invalid, so we are done." The historical batteries remain the record; the stopgap is how those files must now be read; the re-run is what would replace them.

Proportions carry Wilson 95% confidence intervals. Underlying data: `token_classification.csv`, `gate1_rescore.csv`, `gate2_rescore.csv`, `NULL_HONESTY_OUTPUT.md`, `RESCORE_OUTPUT.md`, `EXPERIMENT_LOG.md`.

**Headline (stopgap, post-rescore).** The published all-noise null rejection of about 2 x 10^-15 (and the enlarged-base 3 x 10^-18) is withdrawn as a headline. Those binomials treated any decoder `C` as recovery of the project's reading, and they compared a selected real lexicon to an unselected 4.6% noise floor. The honest, selection-matched range from the same files is **p about 0.005 to 0.06 (marginal)**. Cite `AUDIT_REVIEW_2026-08-18.md` O1 and `NULL_HONESTY_OUTPUT.md`. A recovery-scored, de-duplicated, selection-matched p from a fresh blind battery is **pending re-run**.

Agreed lexicon population: **78 section-9 rows**, each with an H/C/S/O status. L is a tag only. Battery-tested Gate 1 is the **61-row** `strict_committed_results_batch*.csv` set. *pul / puul* has no decode artifact; its old Gate-1 pass is dropped (cell kept: `no_artifact` / pending re-run). Battery E names remain H+L as exact attested lexemes (15/15 in the archived run); folding them into a new null is pending re-run of Battery E under the new protocol.

| Population | N tokens | N distinct roots | Hardened (H) | Share (token) | 95% CI |
|---|---:|---:|---:|---:|---|
| Strict-CSV battery (ids 1-61) | 61 | 52 | 14 | 23.0% | [14.2, 34.9] |
| Battery-tested + Battery E names (enlarged, provisional) | 64 | 55 | 17 | 26.6% | [17.3, 38.5] |
| Section 9 lexicon (agreed; 13 gates pending) | 78 | 69 | 17 | 21.8% | [14.1, 32.2] |

Old headlines (22 H of 62; 25 H of 65; 23/62 and 26/65 strict passes vs a 4.6% floor) do not rebuild from the CSVs. They are retained only as the prior published epoch, not as current results. The 62/65 frame included *pul*; that pass is `no_artifact`.

## 1. Committed lexicon, current tier distribution

Reported on two bases: per token (every attested surface form the translations use) and per distinct root (morphological relatives collapsed to their shared lemma, §7a). Both are kept; neither supersedes the other. Tiers are from `token_classification.csv` after Gate 1 was rescored against the predeclared root, language class, and sense, Gate 2 was extended to same-language homophones, and HARDENING_PROTOCOL violations were demoted out of H.

**Per token (N = 61, battery-tested):**

| Tier | Count | Proportion | 95% CI |
|---|---:|---:|---|
| Hardened (H / H+L) | 14 | 23.0% | [14.2%, 34.9%] |
| Committed + competitor (C*) | 11 | 18.0% | [10.4%, 29.5%] |
| Committed, latitude-dependent (C / C+L) | 36 | 59.0% | [46.5%, 70.5%] |

**Per distinct root (N = 52, same 61 tokens, §7a grouping):**

| Tier | Count | Proportion | 95% CI |
|---|---:|---:|---|
| Hardened (H / H+L) | 14 | 26.9% | [16.8%, 40.3%] |
| Committed + competitor (C*) | 10 | 19.2% | [10.8%, 31.9%] |
| Committed, latitude-dependent (C / C+L) | 28 | 53.8% | [40.5%, 66.7%] |

The per-root H count stays 14 because no hardened token was a duplicate of another hardened token; *te* (C*) collapses into the *Ti* (H) family, so C* drops by one. The 13 former L-only section-9 rows and *pul* are not in this 61/52 battery frame (see §7a and the third-base table).

**Section 9, N = 78 (the table a reader consults):**

| Tier | Count | Notes |
|---|---:|---|
| Hardened (H / H+L) | 17 | both gates, protocol-clean (14 battery + 3 Battery E names) |
| Committed + competitor (C* / C+L*) | 11 | Gate 2 fall (including same-language homophones) |
| Committed, latitude-dependent or pending (C / C+L) | 49 | includes 13 former L-only rows now C+L, hardening pending re-run; *pul* C with no artifact |
| Soft (S+L) | 1 | *Xatlene* (own note: one unresolved vowel step) |

L is never a lone tier. The 13 rows that were L-only are C+L (pending re-run) except *Xatlene* (S+L). Per distinct root on this frame: **17 H of 69 = 24.6% [16.0, 36.0]** (same grouping; the 13 pending rows and *pul* each add a distinct root).

Gate pass rates on both bases (61-row strict CSV, recovery scoring, not legacy any-C):

| Gate | Per token (N = 61) | Per distinct root (N = 52) |
|---|---|---|
| Gate 1, legacy any-C (the F1 hole) | 21/61 = 34.4% [23.7, 47.0] | pending re-run (any-C collapse not rebuilt as a headline) |
| Gate 1, committed-root/lang/sense recovery | 16/61 = 26.2% [16.8, 38.4] (includes *Eztli Pilli* Battery D override; includes *k'ux* and *ma*, which then fail protocol) | 16/52 = 30.8% [19.9, 44.3] |
| Gate 1, protocol-clean recovery | 14/61 = 23.0% [14.2, 34.9] | 14/52 = 26.9% [16.8, 40.3] |
| Gate 2, different-meaning competitor (any language) | 47 survive / 58 testable = 81.0% [69.1, 89.1] (3 names N/A) | 39 survive / 49 testable = 79.6% [66.4, 88.5] |

Reading: between about a fifth and a quarter of the battery-tested vocabulary reconstructs under recovery-scored strict rules, and the great majority (about 80-81%) has no recorded different-meaning competitor in the archived adversarial CSVs. Hardened readings (both gates, protocol-clean) are 23.0% of the 61-row lexicon by token, 26.9% by distinct root; the per-root figure is higher because the collapsed duplicates are almost all non-hardened relatives (§7a). This is the protocol's certification rate after the stopgap rescore, not a direct measure of gloss correctness. A full-lexicon rate including the 13 pending rows is **pending re-run**.

Hardened readings that survive both gates and the protocol, 17 of 78: *ascensionada, che', -en, Eztli Pilli, ich, k'áak', ki', kujkuali, máax, náach, Ti, u, waaj, xefe, Quecholli, Panquetzaliztli, Ixchel*.

Demoted from H (not new etymologies; decoder mismatch or protocol): *akal* (quarrel vs pond), *ek* (wasp vs star/dark), *tul* (K'iche' reed vs Maya wane; also same-language classifier), *uch'* (K'iche' opossum vs drink/crush; dual readings), *xi* (Yucatec go vs claimed Nahuatl do/make), *k'ux* (unexplained *-zeh* residue), *ma* (bundled Maya negation and Nahuatl optative), *pul / puul* (no decode artifact).

## 2. Null-model error rates (pooled, 500 pseudo + 150 real per battery), 95% CI

Pooled Batteries A-D still reproduce as any-C rates (`NULL_MODEL_RESULTS.md`, `NULL_HONESTY_OUTPUT.md`). These are the method's measured error rates for **any** committed-quality dictionary match, not for recovery of a predeclared gloss.

| Battery | FPR(C) | TPR(C), any-root |
|---|---|---|
| A loose / offline | 6.2% [4.4, 8.7] | 20.7% [15.0, 27.8] |
| B loose / online | 8.0% [5.9, 10.7] | 17.3% [12.1, 24.2] |
| C strict / offline | 3.4% [2.1, 5.4] | 12.7% [8.3, 18.9] |
| D strict / online | 4.6% [3.1, 6.8] | 14.0% [9.3, 20.5] |

(The four batteries form a latitude x online-access 2x2. Adding online Nahuatl under the strict rules, D vs C, lifts FPR and TPR together, 3.4 to 4.6% and 12.7 to 14.0%, so discrimination is unchanged; coverage is not the bottleneck, latitude is. Full 2x2 in `NULL_MODEL_RESULTS.md`.)

The CIs do not overlap between FPR and TPR in any battery, so any-C discrimination is statistically real, though modest. `score.py` now prints both the legacy any-C TPR and a committed-recovery TPR when root/lang/gloss columns exist. Battery D online rows often leave those columns empty and are labelled unscorable for recovery. **Recovery TPR/FPR from a complete blind 2x2 is pending re-run.**

**Withdrawn as a headline (not as a historical record).** The claim that 23 of 62 (or 26 of 65) strict passes against a 4.6% floor gives p about 2 x 10^-15 (quoted as ~12.2 sigma) is invalid on three independent grounds:

1. Gate 1 counted any `C`, not the project's root (F1). Rebuildable any-C in the strict CSV is **21/61**, not 23/62. *pul* is missing; *Eztli Pilli* is `soft` in that CSV (the Battery D override is documented in `RESCORE_OUTPUT.md`).
2. The 4.6% floor is not conditioned on the same loose-commitment filter that created the real lexicon (F2 / O1).
3. The quoted sigma values were count z-scores, not normal-tail equivalents of the binomial p. The sigma column is removed.

**Stopgap replacement, selection-matched, from `NULL_HONESTY_OUTPUT.md`:**

| Comparison | Real | Pseudo | Fisher one-sided p |
|---|---|---|---:|
| Audit's mismatched pairing (published 23/62 vs 8/31) | 23/62 | 8/31 | 0.197 |
| Same pairing, CSV-verified | 21/61 | 8/31 | 0.275 |
| Matched A-then-D, trial level | 19/31 | 8/31 | **0.0049** |
| Matched A-then-C offline, trial level | 17/31 | 8/31 | 0.019 |
| Matched, de-pseudoreplicated to item level | 6/9 | 8/27 | **0.058** |
| Recovery-scored matched test, trial and item | pending re-run | pending re-run | pending re-run |
| Distinct-root matched test | pending re-run | pending re-run | pending re-run |

Conditioning on selection collapses the claimed 10^-15 to roughly **p = 0.005 to 0.06** on the archived any-C arms. The signal is marginal, not overwhelming. (`AUDIT_REVIEW` O1.) That range is the stopgap headline. It is still any-C, still on a pseudoreplicated noise arm (426 distinct of 500). The de-duplicated recovery-scored replacement is the re-run, not a further edit of these cells.

## 3. Confidence in the translation (positive predictive value)

**Withdrawn as translation confidence / stopgap pending re-run.** The PPV formula is algebraically fine. What fails is the input: TPR/FPR from any-C scoring do not estimate gloss correctness, and the H row was wired to Battery D rates while the C row used Battery A rates (N2: the top tier scored with a weaker likelihood ratio than the tier beneath it). The tables are kept so the method and the wiring error stay visible. Do not read them as "probability the English gloss is right." A replacement PPV that uses recovery TPR/FPR is **pending re-run**.

The question the formula answers, per reading, is the **positive predictive value (PPV)**: given that a token was certified (committed / hardened), the probability it is a genuine root rather than a chance dictionary coincidence.

PPV = (TPR x b) / (TPR x b + FPR x (1 - b)), where **b** is the base rate: the prior probability that any given Vaal token was actually built from a real root (as opposed to invented phonaesthetic filler). **b is the one quantity we cannot measure** (it depends on GGG's undocumented design process), so PPV is reported across a plausible range.

**Hardened tier** (strict bar, Battery D rates TPR = 0.140, FPR = 0.046, strict + online, **legacy any-C**, the resources the real decode uses). **Withdrawn as translation confidence / stopgap pending re-run:**

| base rate b | PPV (diagnostic only; not current gloss confidence) |
|---|---|
| 20% | 43% |
| 30% | 57% |
| 40% | 67% |
| 50% | 75% |
| 60% | 82% |
| 70% | 88% |
| 75% | 90% |

**Whole committed lexicon** (loose bar, Battery A rates TPR = 0.207, FPR = 0.062): PPV runs about 59% (b = 30%) to 89% (b = 70%); about 82% at the data-anchored b about 58% (77% at the 50% neutral prior). **Withdrawn as translation confidence / stopgap pending re-run.**

The C > H inversion at the same prior is a specification error, not a finding about the language.

## 4. Headline confidence interval

Two defensible statements, one assumption-free and one model-based:

1. **Assumption-free (measured, stopgap post-rescore):** the hardened core of the battery-tested lexicon is **23.0%, 95% CI [14.2%, 34.9%]** per token (14 of 61), or **26.9%, 95% CI [16.8%, 40.3%]** counted over the 52 distinct roots (§7a). On the section-9 table a reader consults it is **21.8% [14.1, 32.2]** (17 of 78) per token, or **24.6% [16.0, 36.0]** (17 of 69) per distinct root. On the provisional enlarged base (61 + three Battery E names) it is **26.6% [17.3, 38.5]** (17 of 64) per token, or **30.9% [20.3, 44.0]** (17 of 55) per distinct root. A fifth to a quarter of the vocabulary the translations run on is robust to both the recovery-scored strict-latitude and adversarial tests; the rest is latitude-dependent, pending, or competitor-flagged. Note that this is the protocol's certification rate, not a direct measure of gloss correctness; the correctness estimate is the PPV in §3, which remains withdrawn as translation confidence until a recovery-scored TPR exists.

2. **Model-based (per-reading confidence), as a pessimistic-to-optimistic range: withdrawn as translation confidence / stopgap pending re-run.** The archived any-C diagnostic said a hardened reading would be genuine with probability from about 43% (pessimistic, b=20%) to about 90% (optimistic, b=75%), with the data-anchored b about 50-58% giving about 75-81%; a general committed reading about 45% to about 91% (anchored about 77-82%). Those bands used the mis-wired TPR/FPR of §3. They are not deleted; they are not current translation confidence. Recompute after the re-run, or leave pending.

## 5. Two honest caveats

- **Sentence-level confidence compounds downward.** Per-token confidence of ~0.77 does not carry to a whole line: a five-token line being entirely genuine is ~0.77^5 about 0.27 under independence. The texts are more fragile than any single token. (And "genuine root" is necessary, not sufficient, for "correct gloss.") **Independence products are withdrawn as a reported floor** (they are not a Frechet lower bound: that bound is max(0, sum p_i - n + 1)). The Kamasan example also assigned a C* probability to *yan*, which has no section-9 row and no CSV row. Keep the worked structure in §6 with those labels; do not quote the percentages as current results. (`AUDIT_REVIEW` O3 / F7.)
- **PPV is only as good as the base rate, and only as good as the question.** If GGG built little of Vaal from real roots (low b), even hardened readings are near coin-flips; if they built much of it (high b), the hardened tier is strong. Any-C TPR answers "did some root attach," not "is this the gloss." Until an exact-root validation set exists (the re-run), do not convert those rates into translation confidence.

## 6. Per-tier confidence and a worked sentence example

**Withdrawn as translation confidence / stopgap pending re-run.** Structure retained; inputs are the legacy any-C rates of §3.

Per-reading confidence (PPV) by tier, using each tier's measured TPR/FPR:

| Tier | Neutral prior (b=50%) | Range b=30-70% | basis |
|---|---|---|---|
| Hardened (H) | 75% | 57-88% | strict bar (TPR 0.140 / FPR 0.046, Battery D strict+online), **legacy any-C** |
| Committed, latitude-dependent (C) | 77% | 59-89% | loose committed bar (0.207 / 0.062) |
| Committed + competitor (C*) | ~50% for the specific gloss | root genuine ~77%, split by a comparable competitor | as C, discounted by the logged competitor |
| Soft / candidate (S) | 53% | 33-73% | loose found bar (0.767 / 0.670); near a coin-flip |

Worked sentence example, the Kamasan Smith line *Ti ek tala jare'yantul!* "Into the dark you come; and so, your waning!" (6 tokens). At the data-anchored prior (b about 58%), each scenario is a [floor, ceiling] interval: floor was reported as the independence product (this is **not** a Frechet lower bound; correct lower bound pending re-run), ceiling = min token PPV = the Frechet upper bound (optimistic, syntax forces the rest once the weakest is fixed).

- all Hardened (0.81): **[28%, 81%]** (withdrawn as translation confidence / stopgap pending re-run)
- all Committed (0.82): **[31%, 82%]** (withdrawn as translation confidence / stopgap pending re-run)
- all Soft (0.61): **[5%, 61%]** (withdrawn as translation confidence / stopgap pending re-run)
- actual parse as previously published (Ti H, ek H, tala C*, jare' C, yan C*, tul H): **[7%, 41%]** (ceiling set by the two C* at ~0.41). **Withdrawn:** *ek* and *tul* are no longer H after the stopgap rescore; *yan* is not a lexicon row (it sits inside the *A'te / U'Te / Yatle* source note) and must not be scored as a committed token.

The product alone is a lower estimate, not the answer (and not an absolute floor: negative correlation could dip below it). Report the interval, not one endpoint. After the re-run, replace the product with the Frechet lower bound if token PPVs are reinstated.

Best/worst real lines (b about 58%), **withdrawn as translation confidence / stopgap pending re-run**: best case *Tlayeb kifba!* (2 committed) = **[68%, 82%]**; most hardened-heavy line *Atziri, Atziri, ascenada akal!* = **[44%, 81%]** (*akal* is no longer H); worst case the Kamasan Smith *Ti ek tala jare'yantul!* (6 tokens, two C*) = **[7%, 41%]**. No short line is purely hardened (hardened tokens almost always share a line with a softer one).

Takeaway: sentence-level confidence is far below token-level because independent uncertain calls multiply. The honest unit of confidence in this work is the token, not the line. Tokens that remain H are mostly short function words, transparent loans, or exact attested names (*che'*, *Ti*, *u*, *xefe*, *Eztli Pilli*, Battery E names).

## 7. The base rate b, estimated from data (not assumed)

b (fraction of Vaal built from real palette roots) is the dominant uncertainty in the PPV. Bounding it empirically. The name-roster proxy is unchanged as a descriptive count of naming behaviour. It is circular as an input to a PPV that already uses the same method, and it is not used here to produce a current translation-confidence interval.

- **Proper-noun proxy (palette-scoped).** The §12 roster is a closed, un-cherry-pickable sample. Four figures are documented out-of-palette borrowings (Apep, Ralakesh, Arakaali, Omnitect) and are out of scope. Among the **33 in-scope names, 19 carry an attested palette root: about 58%.** Many rest on chance-resistant structural markers (the Nahuatl -tl/-tli/-atl absolutives). Clean-parse-only floor about 15-18% (58% is soft-inclusive). Folding the 4 borrowings back into the denominator gives 19/37 about 51%, but that penalizes b for design choices outside the palette's scope and is the wrong denominator.
- **Mixture model b=(O - FPR)/(TPR - FPR): not usable here.** It overflows (b>1) because the null-model TPR (0.140, Battery D, any-C, measured on a hard plant subset) is not the same diagnostic as the lexicon's recovery-clean Gate 1 rate (14/61); O and TPR answer different questions.
- **Consequence:** the palette-scoped proxy puts b about 58% (above the 50% neutral prior). The old conversion into a 75-81% hardened PPV is **withdrawn as translation confidence / stopgap pending re-run**. We do not stretch to b=75%.

## 7a. Non-independence of related tokens (distinct-root recount)

The per-token counts treat each committed token as an independent trial, which overstates the evidence where several tokens share a root (e.g. *ik'bala*, *ikba'yucane*, *Ik'eche*, *ik'el* are all reflexes of Yucatec *ik'* "spirit, breath"). Merging tokens that share the same §9 head root (shared affixes like *-ba'* or *-ane* do not merge distinct heads) collapses 16 of the 61 battery tokens into 7 families, leaving **52 distinct roots**. (The old 62-to-53 recount included *pul*; that row is `no_artifact` and is not in this battery frame.)

| Root | Tokens merged | Gate 1 (recovery, stopgap) |
|---|---|---|
| *ik'* "spirit, breath" | ik'bala, ikba'yucane, Ik'eche, ik'el | all fail |
| *aocmo* "no more" | Aiokmo, 'Ayok | all fail |
| *ātl* "water" | atla, Atziri | all fail |
| *el* "burn" | Ela, elba | all fail |
| *muk'* "strength" | mucane, mujuk' | all fail |
| *k'ex* "transform" | Kextal, qexcan | all fail |
| *ti' / te'* relational | te, Ti | Ti pass, te fail (sense: locative/tree vs relational) |

Only *Ti* held a protocol-clean strict-pass in these families, so collapsing removes no protocol-clean pass (14 stays 14) but nine mostly-failing forms from the denominator. *te* is C* and is absorbed into the H family headed by *Ti*.

**Results on both bases.**

| Metric | Per token (N=61) | Per distinct root (N=52) |
|---|---|---|
| Strict Gate-1 protocol-clean | 14 | 14 |
| Strict Gate-1 recovery (incl. protocol-flagged) | 16 | 16 |
| Null-rejection p (unconditional vs 4.6% floor) | withdrawn as headline; pending re-run | pending re-run |
| Null-rejection p (selection-matched, any-C stopgap) | about 0.005 to 0.06 (`NULL_HONESTY_OUTPUT.md`) | pending re-run |
| Hardened tier | 23.0% [14.2, 34.9] | 26.9% [16.8, 40.3] |
| Gate-1 protocol-clean | 23.0% [14.2, 34.9] | 26.9% [16.8, 40.3] |
| Gate-2 adversarial | 81.0% [69.1, 89.1] (47/58) | 79.6% [66.4, 88.5] (39/49) |
| Tier split H / C* / C | 14 / 11 / 36 | 14 / 10 / 28 |

**Reading.** The dependency correction does not weaken the coverage claim; it slightly strengthens it. The related tokens are concentrated in the strict-failing families (*ik'-*, *el-*, *muk'-*, *aocmo-*, *ātl-*, *k'ex-*), so removing the duplicates prunes the denominator faster than the signal: all 14 protocol-clean passes survive as distinct roots, now over a count of 52 rather than 61. The hardened fraction therefore rises from 23.0% to 26.9% on the battery frame (21.8% to 24.6% on the 78-row section-9 table; 26.6% to 30.9% on the provisional enlarged base, third-base table in master §17.7). The recount is defensive, not promotional: non-independence of related forms is a standard objection, and here it overturns none of the stopgap conclusions. It also does not restore a 10^-15 unconditional floor test, because that comparison is the wrong test.

**Both bases are kept on purpose.** The per-token figures are not superseded. They are the honest raw account of how the committed lexicon behaves form by form; the per-root figures are the honest account of how it behaves lemma by lemma. Neither is privileged. The per-token base is the more conservative denominator for the *coverage* claims (it counts every attested form the translations actually use), the per-root base is the correct one for the *independence* claim (it counts each lexical bet once). Where a single headline number is needed, the per-token figure is quoted first with the per-root figure beside it.

The 500-trial pseudo arm itself is pseudoreplicated: **426 distinct strings of 500**, with 53 strings repeating across seeds (*ko'ja* x5, *noche* / *noch* / *fuks* x4). Some "noise" hits are palette substrings (*eztl* of *Eztli*) or ordinary Spanish (*noche*). Distinct-string Battery D FPR is 21/426 = 4.9%. Binomial intervals that treat n=500 as independent are too narrow. Full-pipeline simulation on unique strings was not re-run; the matched A-then-D comparison is the stopgap correction the archived files support. (`NULL_HONESTY_OUTPUT.md`, AUDIT_REVIEW N1.) De-duplicated generator: **pending re-run**.

## 8. Syntax (analyst-level)

The published 12/12 vs 0/8 Fisher (p about 7.9 x 10^-6) treats four correlated rules per analyst as independent trials. At the experimental unit (analyst by corpus) the table is **3/3 vs 0/2, Fisher p = 0.10**, not significant. Analysts received surface lines, English translations, and a token glossary; they were not blind to the project's readings. Reproducibility of surface order on the supplied alignment is qualitative. The design cannot support a significance claim. (`SYNTAX_EXPERIMENT_LOG.md`, AUDIT_REVIEW F8.)

A replacement panel, analysts blinded to project English glosses and scored at analyst level from the start, is **pending re-run** (`EXPERIMENT_RERUN_PROTOCOL.md`).

## 9. Reproduce (stopgap archives)

```
python3 rescore_gate1.py
python3 score_adversarial.py
python3 null_honesty.py
python3 score.py blind_test_results_tight_s42.csv blind_test_key_s42.csv
```

Re-run plan, batteries A-E, blinding, success criteria, and artifacts: `EXPERIMENT_RERUN_PROTOCOL.md`. Do not mix rerun files with these archives.
