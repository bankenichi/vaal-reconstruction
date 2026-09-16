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

Scorers: `score.py` (null model), `score_adversarial.py` (adversarial). Classification: `token_classification.csv`.

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

Adversarial pass: 51/58 testable committed tokens (88%) have no genuine cross-language competitor; 7 do (master §10.12), strongest is itsok vs Nahuatl itztli "obsidian."

## Hardening outcome (master §8 tiers)

Of 62 committed tokens: **22 Hardened (H)** (pass strict decode + adversarial), **7 committed-with-competitor (C\*)**, **33 committed latitude-dependent (C)**. Hardened set: akal, ascensionada, che', ek, -en, Eztli (Pilli), ich, k'áak', ki', kujkuali, k'ux, ma, máax, náach, pul, Ti, tul, u, uch', waaj, xefe, xi. (The battery first covered 61 tokens; *pul* "to throw, cast" was restored from the pre-import copy and run through both gates, passing as Hardened, giving 62/22.)

Correcting for non-independence: 16 of the 62 tokens are morphological relatives sharing 7 roots, so the effective count is **53 distinct roots** (master §17.7 / `STATISTICAL_SUMMARY.md` §7a). On that basis the split is 22 H / 6 C* / 25 C, the strict-null rejection is 22 passes of 53 (p ≈ 4 x 10^-16, against the Battery D strict-and-online noise floor of 4.6%), and the hardened fraction is 41.5% [29.3, 54.9] versus 35.5% [24.7, 47.9] per token. Both bases are retained.

## Orthographic hardening of the correspondence rules

The §2.6 stylization rules were hardened as spelling correspondences (no audio; phonetic phonology is out of scope, master §2.6 scope note). This introduces no new run: the strict-versus-loose latitude the null model already varies IS the permissiveness of these rules. Reading the existing result at the rule level: strict-safe correspondences (u->/o/, silent g, Gua-/Gue- for /kw/, -tzin->-tzi, ejective marking) versus permissive ones (-tl->-to, terminal-vowel padding, -uks/-s codas, -che/-zeh tails). 23/62 committed tokens (37.1% [26.2, 49.5]) derive using strict-safe rules only (= the Gate 1 pass set); the rest need >=1 permissive rule. Permissive-rule specificity is the null FPR: 3.4% strict (Battery C) vs 67% loose (Battery A found-rate). Full writeup: master §17.9.

## Hardening of post-battery onomastic tokens (2026-07)

Three onomastic tokens added after the null-model battery were run through both gates per `HARDENING_PROTOCOL.md`:

| Token | Gate 1 (strict) | Gate 2 (adversarial) | Tier |
|---|---|---|---|
| Quecholli | pass (surface = attested Nah. *quecholli*, 14th veintena; no residue) | pass (no cross-language competitor) | H+L |
| Panquetzaliztli | pass (surface = attested Nah. *panquetzaliztli* = *pan* + *quetza* + *-liztli*; no residue) | pass | H+L |
| Ixchel | pass (Yuc. *Ix-* + *Chel* "rainbow"; the attested theonym Ix Chel; no residue) | pass (no equal-or-stronger different-language root; Nah. *ix-* "eye/face" has no source for *chel*) | H+L |

These three are onomastic (item and figure names), not corpus-text tokens, and they entered after the battery, so they are recorded beside the 62-token statistical base of master §17 rather than folded into its counts; the 62/22 figures and the null-rejection p-values are unchanged. A full re-baseline is the versioning trigger (master §14 and README).

The other new terms did not earn H: the strongbox artisans *Ixtolatl* and *Mahuatzi* and the pre-existing *Mahuxotl* fail Gate 1 (an unresolved medial or a contraction with residue), so they stay Soft (master §12.7); the Vaal Temple trio *K'aj Y'ara'az / K'aj Q'ura / K'aj A'alai* has no clean whole-name attested root and stays Open (master §12.8).

**Enlarged-base figures (tracked, not headline).** If the three hardened names are folded into the committed base, the per-token hardened fraction moves from 22/62 = 35.5% [24.7, 47.9] to 25/65 = 38.5% [27.6, 50.6]; per distinct root from 22/53 = 41.5% [29.3, 54.9] to 25/56 = 44.6% [32.4, 57.6] (25/55 = 45.5% if *quetza* is treated as an already-present root). The strict-latitude null rejection strengthens from 23/62 (p about 2 x 10^-15, ~12.2 sigma) to 26/65 (p about 3 x 10^-18, ~13.6 sigma) against the 4.6% Battery D floor; per distinct root from 22/53 to 25/56 (p about 5 x 10^-19, ~14.3 sigma). The PPV band (about 75-81% for hardened readings) does not move materially, since three confirmed-real names cannot shift the base-rate estimate by more than a point. The headline master §17 statistics remain the original battery-tested 62-token figures; these enlarged-base numbers are retained so the record stays honest and updatable as the corpus grows (master §14 versioning). The two bases are complementary, not exclusive: the original is the figure that was actually null-tested, the enlarged is where it trends as verified material accrues.

**Update (Battery E, 2026-07).** The three names were then run as blind plants under the same strict-and-online conditions across all five seeds (`BATTERY_E_RESULTS.md`): 15/15 Gate-1 passes (Quecholli 5/5, Panquetzaliztli 5/5, Ixchel 5/5), with the real controls calibrating to their known tiers (naach 5/5, ek 4/5, kutsen 1/5, sakilja 0/5, kilya 0/5) and Gate-2 survival confirmed by unanimous single-language assignment. The enlarged base is therefore now itself null-tested, not merely null-adjacent, and carries the headline figures; Batteries A-D (the 62-token run) are retained as the prior epoch. The small-sample distractor false-positive rate (10/60) is logged in `BATTERY_E_RESULTS.md` for transparency but does not replace the Battery D 4.6% floor, which the null-rejection test still uses.

## Task status

All experiment (E1.*, E2.*) and implementation (I1-I7) tasks complete, including Battery D (strict + online, the fourth 2x2 cell; full results in `NULL_MODEL_RESULTS.md`). Remaining optional work: extend the null-model battery to more seeds; apply the hardening protocol to §10 soft tokens if any are promoted.

## Reproduce / resume

- Regenerate any null-model worksheet: `python3 gen_set.py <seed>` (seeds above).
- Re-score: `python3 score.py <results.csv> <key.csv>`.
- Per-token hardening test for future tokens: `HARDENING_PROTOCOL.md`.
