# Statistical summary and confidence interval for the translation

Current status after the full-lexicon hardening pass. Proportions carry Wilson 95% confidence intervals (appropriate for small-sample binomial rates). Underlying data: `token_classification.csv`, `NULL_MODEL_RESULTS.md`, `EXPERIMENT_LOG.md`.

**Current headline base (2026-07, after Battery E).** The tables below are the original 62-token run (Batteries A-D), retained as the prior epoch. Three names hardened afterward (*Quecholli*, *Panquetzaliztli*, *Ixchel*) were then blind-certified as plants under the same strict-and-online conditions (Battery E, `BATTERY_E_RESULTS.md`: 15/15 Gate-1 passes, controls calibrated), so the current headline is the enlarged base: **65 tokens, 25 hardened = 38.5% [27.6, 50.6]; 56 distinct roots, 25 hardened = 44.6% [32.4, 57.6]; 26 strict passes vs the 4.6% floor, p about 3 x 10^-18**. Composition caveat (the three are exact attested lexemes, easy plants, not affecting the null rejection) in master §17.5.

## 1. Committed lexicon, current tier distribution

Reported on two bases: per token (every attested surface form the translations use) and per distinct root (morphological relatives collapsed to their shared lemma, §7a). Both are kept; neither supersedes the other.

**Per token (N = 62):**

| Tier | Count | Proportion | 95% CI |
|---|---|---|---|
| Hardened (H) | 22 | 35.5% | [24.7%, 47.9%] |
| Committed + competitor (C\*) | 7 | 11.3% | [5.6%, 21.5%] |
| Committed, latitude-dependent (C) | 33 | 53.2% | [41.0%, 65.1%] |

**Per distinct root (N = 53):**

| Tier | Count | Proportion | 95% CI |
|---|---|---|---|
| Hardened (H) | 22 | 41.5% | [29.3%, 54.9%] |
| Committed + competitor (C\*) | 6 | 11.3% | [5.3%, 22.6%] |
| Committed, latitude-dependent (C) | 25 | 47.2% | [34.6%, 60.2%] |

Gate pass rates on both bases:

| Gate | Per token | Per distinct root |
|---|---|---|
| Gate 1, strict-latitude reconstruction | 23/62 = 37.1% [26.2%, 49.5%] | 22/53 = 41.5% [29.3%, 54.9%] |
| Gate 2, adversarial survival | 55/62 = 88.7% [78.5%, 94.4%] | 48/53 = 90.6% [79.7%, 95.9%] |

Reading: between a third and two-fifths of the committed vocabulary reconstructs under strict rules, and the great majority (88-91%) has no genuine cross-language competitor. Hardened readings (both gates) are 35.5% of the lexicon by token, 41.5% by distinct root; the per-root figure is higher because the collapsed duplicates are almost all non-hardened relatives (§7a).

## 2. Null-model error rates (pooled, 500 pseudo + 150 real per battery), 95% CI

| Battery | FPR(C) | TPR(C) |
|---|---|---|
| A loose / offline | 6.2% [4.4, 8.7] | 20.7% [15.0, 27.8] |
| B loose / online | 8.0% [5.9, 10.7] | 17.3% [12.1, 24.2] |
| C strict / offline | 3.4% [2.1, 5.4] | 12.7% [8.3, 18.9] |
| D strict / online | 4.6% [3.1, 6.8] | 14.0% [9.3, 20.5] |

(The four batteries form a latitude x online-access 2x2. Adding online Nahuatl under the strict rules, D vs C, lifts FPR and TPR together, 3.4 to 4.6% and 12.7 to 14.0%, so discrimination is unchanged; coverage is not the bottleneck, latitude is. Full 2x2 in `NULL_MODEL_RESULTS.md`.)

These are the method's measured error rates: the chance a nonsense string is certified committed-quality (FPR) versus the chance a real token is (TPR). The CIs do not overlap between FPR and TPR in any battery, so the method's discrimination is statistically real, though modest. The same discrimination rejects the "all-noise" hypothesis outright: 23 of the 62 committed tokens reconstruct under strict rules against ~3 expected if each were noise at the 4.6% strict-and-online rate (Battery D, the resources the real decode uses; the offline 3.4% gives an even smaller p) (binomial p ≈ 2 x 10^-15, a ~12.2-sigma departure). Taken over the 53 distinct roots instead of the 62 tokens (correcting for related forms, §7a), it is 22 passes against ~2.4 expected (p ≈ 4 x 10^-16): the rejection is not an artifact of counting shared roots more than once. (These are the original A-D run; on the enlarged headline base with the three Battery-E names it is 26 of 65 tokens, p ≈ 3 x 10^-18, and 25 of 56 roots, p ≈ 5 x 10^-19; see the headline banner above and master §17.7.)

## 3. Confidence in the translation (positive predictive value)

The question "how confident are we the translation is genuine?" is, per reading, the **positive predictive value (PPV)**: given that a token was certified (committed / hardened), the probability it is a genuine root rather than a chance dictionary coincidence.

PPV = (TPR × b) / (TPR × b + FPR × (1 − b)), where **b** is the base rate: the prior probability that any given Vaal token was actually built from a real root (as opposed to invented phonaesthetic filler). **b is the one quantity we cannot measure** (it depends on GGG's undocumented design process), so PPV is reported across a plausible range.

**Hardened tier** (strict bar, Battery D rates TPR = 0.140, FPR = 0.046, strict + online, the resources the real decode uses):

| base rate b | PPV (confidence a hardened reading is genuine) |
|---|---|
| 20% | 43% |
| 30% | 57% |
| 40% | 67% |
| 50% | 75% |
| 60% | 82% |
| 70% | 88% |
| 75% | 90% |

**Whole committed lexicon** (loose bar, Battery A rates TPR = 0.207, FPR = 0.062): PPV runs about 59% (b = 30%) to 89% (b = 70%); ≈82% at the data-anchored b ≈ 58% (77% at the 50% neutral prior).

## 4. Headline confidence interval

Two defensible statements, one assumption-free and one model-based:

1. **Assumption-free (measured):** the hardened core of the committed lexicon is **35.5%, 95% CI [24.7%, 47.9%]** per token, or **41.5%, 95% CI [29.3%, 54.9%]** counted over the 53 distinct roots (§7a). A third to two-fifths of the vocabulary the translations run on is robust to both the strict-latitude and adversarial tests; the rest is latitude-dependent (plausible, but not distinguishable from chance at the strict bar). Note that this is the protocol's certification rate, not a direct measure of gloss correctness; the correctness estimate is the PPV in §3.

2. **Model-based (per-reading confidence), as a pessimistic-to-optimistic range:** a **hardened reading is genuine with probability from ≈43% (pessimistic, b=20%) to ≈90% (optimistic, b=75%)**, with the data-anchored b≈50-58% giving ≈75-81%; a general committed reading ≈45% to ≈91% (anchored ≈77-82%). The dominant uncertainty is b, not the test; readers may pick their own outlook along the range.

## 5. Two honest caveats

- **Sentence-level confidence compounds downward.** Per-token confidence of ~0.77 does not carry to a whole line: a five-token line being entirely genuine is ~0.77^5 ≈ 0.27 under independence. The texts are more fragile than any single token. (And "genuine root" is necessary, not sufficient, for "correct gloss.")
- **PPV is only as good as the base rate.** If GGG built little of Vaal from real roots (low b), even hardened readings are near coin-flips; if they built much of it (high b), the hardened tier is strong. The honest position is a range, and the hardened tier is where that range is highest.

## 6. Per-tier confidence and a worked sentence example

Per-reading confidence (PPV) by tier, using each tier's measured TPR/FPR:

| Tier | Neutral prior (b=50%) | Range b=30-70% | basis |
|---|---|---|---|
| Hardened (H) | 75% | 57-88% | strict bar (TPR 0.140 / FPR 0.046, Battery D strict+online) |
| Committed, latitude-dependent (C) | 77% | 59-89% | loose committed bar (0.207 / 0.062) |
| Committed + competitor (C\*) | ~50% for the specific gloss | root genuine ~77%, split by a comparable competitor | as C, discounted by the logged competitor |
| Soft / candidate (S) | 53% | 33-73% | loose found bar (0.767 / 0.670); near a coin-flip |

Worked sentence example, the Kamasan Smith line *Ti ek tala jare'yantul!* "Into the dark you come; and so, your waning!" (6 tokens). At the data-anchored prior (b ≈ 58%), each scenario is a [floor, ceiling] interval: floor = independence product (pessimistic), ceiling = min token PPV = the Fréchet upper bound (optimistic, syntax forces the rest once the weakest is fixed).

- all Hardened (0.81): **[28%, 81%]**
- all Committed (0.82): **[31%, 82%]**
- all Soft (0.61): **[5%, 61%]**
- actual parse (Ti H, ek H, tala C*, jare' C, yan C*, tul H): **[7%, 41%]** (ceiling set by the two C* at ~0.41)

The product alone is a lower estimate, not the answer (and not an absolute floor: negative correlation could dip below it). Report the interval, not one endpoint.

Best/worst real lines (b≈58%): best case *Tlayeb kifba!* (2 committed) = **[68%, 82%]**; most hardened-heavy line *Atziri, Atziri, ascenada akal!* = **[44%, 81%]**; worst case the Kamasan Smith *Ti ek tala jare'yantul!* (6 tokens, two C*) = **[7%, 41%]**. No short line is purely hardened (hardened tokens almost always share a line with a softer one).

Takeaway: sentence-level confidence is far below token-level because independent uncertain calls multiply. The honest unit of confidence in this work is the token, not the line.

## 7. The base rate b, estimated from data (not assumed)

b (fraction of Vaal built from real palette roots) is the dominant uncertainty in the PPV. Bounding it empirically:

- **Proper-noun proxy (palette-scoped).** The §12 roster is a closed, un-cherry-pickable sample. Four figures are documented out-of-palette borrowings (Apep, Ralakesh, Arakaali, Omnitect) and are out of scope. Among the **33 in-scope names, 19 carry an attested palette root: ≈ 58%.** Many rest on chance-resistant structural markers (the Nahuatl -tl/-tli/-atl absolutives). Clean-parse-only floor ≈ 15-18% (58% is soft-inclusive). Folding the 4 borrowings back into the denominator gives 19/37 ≈ 51%, but that penalizes b for design choices outside the palette's scope and is the wrong denominator.
- **Mixture model b=(O−FPR)/(TPR−FPR): not usable here.** It overflows (b>1) because the null-model TPR (0.140, Battery D, measured on a hard plant subset) understates the committed lexicon's real strict-pass rate (37%); O>TPR has no valid solution.
- **Consequence:** the palette-scoped proxy puts b ≈ 58% (above the 50% neutral prior), so the data-anchored hardened PPV is ≈75% (b=50%) to ≈81% (b=58%). We do not stretch to b=75%.

## 7a. Non-independence of related tokens (distinct-root recount)

The per-token counts treat each committed token as an independent trial, which overstates the evidence where several tokens share a root (e.g. *ik'bala*, *ikba'yucane*, *Ik'eche*, *ik'el* are all reflexes of Yucatec *ik'* "spirit, breath"). Merging tokens that share the same §9 head root (shared affixes like *-ba'* or *-ane* do not merge distinct heads) collapses 16 of the 62 tokens into 7 families, leaving **53 distinct roots**:

| Root | Tokens merged | Gate 1 |
|---|---|---|
| *ik'* "spirit, breath" | ik'bala, ikba'yucane, Ik'eche, ik'el | all fail |
| *aocmo* "no more" | Aiokmo, 'Ayok | all fail |
| *ātl* "water" | atla, Atziri | all fail |
| *el* "burn" | Ela, elba | all fail |
| *muk'* "strength" | mucane, mujuk' | all fail |
| *k'ex* "transform" | Kextal, qexcan | all fail |
| *ti' / te'* relational | te, Ti | both pass |

Only *ti'/te'* held a strict-pass, so collapsing removes one pass (23 to 22) but nine mostly-failing forms from the denominator. Every headline figure holds or improves:

| Metric | Per token (N=62) | Per distinct root (N=53) |
|---|---|---|
| Strict Gate-1 passes | 23 (exp 2.9) | 22 (exp 2.4) |
| Null-rejection p | 2 x 10^-15 | 4 x 10^-16 |
| Hardened tier | 35.5% [24.7, 47.9] | 41.5% [29.3, 54.9] |
| Gate-1 strict | 37.1% [26.2, 49.5] | 41.5% [29.3, 54.9] |
| Gate-2 adversarial | 88.7% [78.5, 94.4] | 90.6% [79.7, 95.9] |
| Tier split H / C\* / C | 22 / 7 / 33 | 22 / 6 / 25 |

The related tokens cluster in the strict-failing families, so the correction prunes the denominator faster than the signal and the hardened fraction rises to 41.5%. Both bases are retained deliberately: the per-token count is the conservative denominator for coverage claims, the per-root count is the correct one for the independence claim. Full derivation and reasoning in master §17.7.

