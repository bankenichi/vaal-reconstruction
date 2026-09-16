# Statistical summary and confidence interval for the translation

Current status after the 2026-09 audit remediation (`AUDIT_REVIEW_2026-08-18.md`, `FULL_AUDIT_2026-08-18.md`). Proportions carry Wilson 95% confidence intervals. Underlying data: `token_classification.csv`, `gate1_rescore.csv`, `NULL_HONESTY_OUTPUT.md`, `RESCORE_OUTPUT.md`, `EXPERIMENT_LOG.md`.

**Headline (post-rescore).** The published all-noise null rejection of about 2 x 10^-15 (and the enlarged-base 3 x 10^-18) is withdrawn. Those binomials treated any decoder `C` as recovery of the project's reading, and they compared a selected real lexicon to an unselected 4.6% noise floor. The honest, selection-matched range from the same files is **p ≈ 0.005 to 0.06 (marginal)**. Cite `AUDIT_REVIEW_2026-08-18.md` O1 and `NULL_HONESTY_OUTPUT.md`.

Agreed lexicon population: **78 section-9 rows**, each with an H/C/S/O status. L is a tag only. Battery-tested Gate 1 is the **61-row** `strict_committed_results_batch*.csv` set. *pul / puul* has no decode artifact; its old Gate-1 pass is dropped.

| Population | N | Hardened (H) | Share | 95% CI |
|---|---:|---:|---:|---|
| Section 9 lexicon (agreed) | 78 | 17 | 21.8% | [14.1, 32.2] |
| Strict-CSV battery (ids 1-61) | 61 | 14 | 23.0% | [14.2, 34.9] |
| Battery-tested + Battery E names | 64 | 17 | 26.6% | [17.3, 38.5] |

Old headlines (22 H of 62; 25 H of 65; 23/62 and 26/65 strict passes vs a 4.6% floor) do not rebuild from the CSVs and are not repeated as current results.

## 1. Committed lexicon, current tier distribution

Tiers from `token_classification.csv` after Gate 1 was rescored against the predeclared root, language class, and sense, Gate 2 was extended to same-language homophones, and HARDENING_PROTOCOL violations were demoted out of H.

**Section 9, N = 78 (the table a reader consults):**

| Tier | Count | Notes |
|---|---:|---|
| Hardened (H / H+L) | 17 | both gates, protocol-clean |
| Committed + competitor (C* / C+L*) | 11 | Gate 2 fall (including same-language homophones) |
| Committed, latitude-dependent or pending (C / C+L) | 49 | includes 13 former L-only rows now C+L, hardening pending |
| Soft (S+L) | 1 | *Xatlene* (own note: one unresolved vowel step) |

L is never a lone tier. The 13 rows that were L-only are C+L (pending) except *Xatlene* (S+L).

**Battery-tested subset, N = 61:**

| Tier | Count | Proportion | 95% CI |
|---|---:|---:|---|
| Hardened (H) | 14 | 23.0% | [14.2%, 34.9%] |
| Committed + competitor (C*) | 11 | 18.0% | [10.4%, 29.5%] |
| Committed (C / C+L) | 36 | 59.0% | [46.5%, 70.5%] |

Gate pass rates on the 61-row strict CSV, after recovery scoring (not legacy any-C):

| Gate | Count | Rate |
|---|---|---|
| Gate 1, legacy any-C (the F1 hole) | 21/61 | 34.4% [23.7, 47.0] |
| Gate 1, committed-root/lang/sense recovery | 16/61 | 26.2% [16.8, 38.4] (includes *Eztli Pilli* Battery D override; includes *k'ux* and *ma*, which then fail protocol) |
| Gate 1, protocol-clean recovery | 14/61 | 23.0% [14.2, 34.9] |
| Gate 2, different-meaning competitor (any language) | 47 survive / 58 testable | 81.0% (3 names N/A). Was 51/58 effective under the old cross-language-only filter. |

Hardened readings that survive both gates and the protocol, 17 of 78: *ascensionada, che', -en, Eztli Pilli, ich, k'áak', ki', kujkuali, máax, náach, Ti, u, waaj, xefe, Quecholli, Panquetzaliztli, Ixchel*.

Demoted from H (not new etymologies; decoder mismatch or protocol): *akal* (quarrel vs pond), *ek* (wasp vs star/dark), *tul* (K'iche' reed vs Maya wane; also same-language classifier), *uch'* (K'iche' opossum vs drink/crush; dual readings), *xi* (Yucatec go vs claimed Nahuatl do/make), *k'ux* (unexplained *-zeh* residue), *ma* (bundled Maya negation and Nahuatl optative), *pul / puul* (no decode artifact).

## 2. Null-model error rates, and what they may be used for

Pooled Batteries A-D still reproduce as any-C rates (`NULL_MODEL_RESULTS.md`, `NULL_HONESTY_OUTPUT.md`):

| Battery | FPR(C) | TPR(C), any-root |
|---|---|---|
| A loose / offline | 6.2% [4.4, 8.7] | 20.7% [15.0, 27.8] |
| B loose / online | 8.0% [5.9, 10.7] | 17.3% [12.1, 24.2] |
| C strict / offline | 3.4% [2.1, 5.4] | 12.7% [8.3, 18.9] |
| D strict / online | 4.6% [3.1, 6.8] | 14.0% [9.3, 20.5] |

These rates measure whether a surface string receives *any* committed-quality dictionary match. They do **not** measure recovery of a predeclared gloss. `score.py` now prints both the legacy any-C TPR and a committed-recovery TPR when root/lang/gloss columns exist. Battery D online rows often leave those columns empty and are labelled unscorable for recovery.

**Withdrawn headline.** The claim that 23 of 62 (or 26 of 65) strict passes against a 4.6% floor gives p ≈ 2 x 10^-15 (quoted as ~12.2 sigma) is invalid on three independent grounds:

1. Gate 1 counted any `C`, not the project's root (F1). Rebuildable any-C in the strict CSV is **21/61**, not 23/62. *pul* is missing; *Eztli Pilli* is `soft` in that CSV (the Battery D override is documented in `RESCORE_OUTPUT.md`).
2. The 4.6% floor is not conditioned on the same loose-commitment filter that created the real lexicon (F2 / O1).
3. The quoted sigma values were count z-scores, not normal-tail equivalents of the binomial p. The sigma column is removed.

**Honest replacement, selection-matched, from `NULL_HONESTY_OUTPUT.md`:**

| Comparison | Real | Pseudo | Fisher one-sided p |
|---|---|---|---:|
| Audit's mismatched pairing (published 23/62 vs 8/31) | 23/62 | 8/31 | 0.197 |
| Same pairing, CSV-verified | 21/61 | 8/31 | 0.275 |
| Matched A-then-D, trial level | 19/31 | 8/31 | **0.0049** |
| Matched A-then-C offline, trial level | 17/31 | 8/31 | 0.019 |
| Matched, de-pseudoreplicated to item level | 6/9 | 8/27 | **0.058** |

Conditioning on selection collapses the claimed 10^-15 to roughly **p = 0.005 to 0.06**. The signal is marginal, not overwhelming. (`AUDIT_REVIEW` O1.)

## 3. PPV: retained as a method diagnostic, not as translation confidence

The PPV formula is algebraically fine and the Frechet upper bound on a line is fine. What fails is the input: TPR/FPR from any-C scoring do not estimate gloss correctness, and the H row was wired to Battery D rates while the C row used Battery A rates (N2: the top tier scored with a weaker likelihood ratio than the tier beneath it). Sentence-level independence products are withdrawn (section 5).

Do not read the table below as "probability the English gloss is right." It is the old matchability diagnostic, kept so the wiring error is visible, and it should not be used as a translation confidence.

| Tier | Neutral prior (b=50%) | basis (legacy any-C rates) |
|---|---|---|
| Hardened (H) | 75% | Battery D TPR 0.140 / FPR 0.046 |
| Committed (C) | 77% | Battery A TPR 0.207 / FPR 0.062 |
| Soft (S) | 53% | loose found bar |

The C > H inversion at the same prior is a specification error, not a finding about the language.

## 4. Headline confidence interval

Assumption-free (measured, post-rescore): **17 of 78 section-9 rows are hardened, 21.8% [14.1, 32.2]**. On the 61-row battery, 14 of 61 = 23.0% [14.2, 34.9]. This is the protocol's certification rate after recovery scoring, not a probability that a gloss is the designers' meaning.

Model-based per-reading translation PPVs are not reported as current results.

## 5. Two honest caveats (replaces sentence-level percentages)

- **Sentence-level probability percentages are withdrawn.** Independence products (for example 0.77^5 ≈ 0.27) are not a floor, and the Kamasan example assigned a C* probability to *yan*, which has no section-9 row and no CSV row. The honest statement is a weakest-link qualitative: a line is no stronger than its least-secure token, and many lines mix H with C, C*, S, or pending rows. Report uncertainty token by token. (`AUDIT_REVIEW` O3 / F7.)
- **PPV is only as good as the question.** Any-C TPR answers "did some root attach," not "is this the gloss." Until an exact-root validation set exists, do not convert those rates into translation confidence.

## 6. Per-tier notes, without sentence arithmetic

Worked lines are not given percentages. For orientation only:

- Tokens that remain H are mostly short function words, transparent loans, or exact attested names (*che'*, *Ti*, *u*, *xefe*, *Eztli Pilli*, Battery E names).
- *yan* in the Kamasan Smith line is not a lexicon row; it sits inside the *A'te / U'Te / Yatle* source note. It is not a committed token and must not be scored as one.
- *ek* and *tul* in that line are no longer H.

## 7. The base rate b

The name-roster proxy (about 58% of in-scope names carrying a palette root) is unchanged as a descriptive count of naming behaviour. It is circular as an input to a PPV that already uses the same method, and it is not used here to produce a translation-confidence interval. The mixture-model formula still overflows because O and TPR are not the same diagnostic.

## 7a. Non-independence of related tokens

The old distinct-root recount (62 tokens to 53 roots, 23 passes to 22) was computed on the withdrawn any-C / 23-of-62 figures. It is not rebuilt as a headline. Related forms still cluster in the failing families (*ik'*, *el*, *muk'*, *aocmo*, *atl*, *k'ex*); collapsing them would not restore a 10^-15 result, because the unconditional floor comparison is the wrong test.

The 500-trial pseudo arm itself is pseudoreplicated: **426 distinct strings of 500**, with 53 strings repeating across seeds (*ko'ja* x5, *noche* / *noch* / *fuks* x4). Some "noise" hits are palette substrings (*eztl* of *Eztli*) or ordinary Spanish (*noche*). Distinct-string Battery D FPR is 21/426 = 4.9%. Binomial intervals that treat n=500 as independent are too narrow. Full-pipeline simulation on unique strings was not re-run; the matched A-then-D comparison is the correction the archived files support. (`NULL_HONESTY_OUTPUT.md`, AUDIT_REVIEW N1.)

## 8. Syntax (analyst-level)

The published 12/12 vs 0/8 Fisher (p ≈ 7.9 x 10^-6) treats four correlated rules per analyst as independent trials. At the experimental unit (analyst by corpus) the table is **3/3 vs 0/2, Fisher p = 0.10**, not significant. Analysts received surface lines, English translations, and a token glossary; they were not blind to the project's readings. Reproducibility of surface order on the supplied alignment is qualitative. The design cannot support a significance claim. (`SYNTAX_EXPERIMENT_LOG.md`, AUDIT_REVIEW F8.)

## 9. Reproduce

```
python3 rescore_gate1.py
python3 score_adversarial.py
python3 null_honesty.py
python3 score.py blind_test_results_tight_s42.csv blind_test_key_s42.csv
```
