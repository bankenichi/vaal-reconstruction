# Null-model results: does the decoder beat noise?

Blind experiment per `NULL_MODEL_PROTOCOL.md`. Each pass mixes 100 pseudo-Vaal strings (no designed meaning) with 30 real committed Vaal tokens, shuffled with labels hidden; a fresh general-purpose agent (blind to the key, no memory of the project) decodes all 130 form-first at the project's own latitude; I then score against the held-out key.

## Metrics: definitions and equations

### The raw ingredients

Every pass produces two populations and, for each item, one label.

- **Population P (pseudo):** the 100 generated noise strings in a pass (500 pooled across 5 passes). These have no designed meaning; any root found for them is by construction a false positive.
- **Population R (real):** the 30 genuine committed Vaal tokens planted in a pass (150 pooled). These are known positives; a root found for them is a true positive.
- **Label** (assigned by the blind decoder to each item, one of three):
  - `C` (committed-quality): an attested root with workable phonology and a sensible gloss.
  - `soft`: a plausible attested root but with one unresolved step.
  - `none`: no attested root plausibly fits.
- **found** = the item got any root, i.e. label is `C` **or** `soft`. (`none` is "not found".)

Counting symbols used below: `P_C` = number of pseudo items labeled `C`; `P_found` = pseudo labeled C or soft; `|P|` = total pseudo (100 per pass, 500 pooled). Likewise `R_C`, `R_found`, `|R|` (30 per pass, 150 pooled).

### The four rate metrics

**FPR(C), false-positive rate at the committed bar.**
Equation: `FPR(C) = P_C / |P|`.
Term by term: `P_C` is how many meaningless noise strings the decoder wrongly certified as committed-quality; `|P|` is the total number of noise strings tested. The ratio is the probability that a pure-noise string gets a `C`. Lower is better; 0 means noise never fools the method at the committed bar.

**FPR(C+soft), false-positive rate at the loosest bar.**
Equation: `FPR(C+soft) = P_found / |P| = (P_C + P_soft) / |P|`.
Same as above but counting any root found (committed or soft) as a positive. This measures how often noise gets *any* reading at all.

**TPR(C), true-positive rate at the committed bar.**
Equation: `TPR(C) = R_C / |R|`.
Term by term: `R_C` is how many genuine tokens the decoder correctly certified as committed-quality; `|R|` is the total number of genuine tokens tested. The ratio is the probability that a real token earns a `C`. Higher is better; 1 means every real token is recovered at the committed bar.

**TPR(found), true-positive rate at the loosest bar.**
Equation: `TPR(found) = R_found / |R| = (R_C + R_soft) / |R|`.
How often a real token gets any reading.

### The two comparison metrics (these are the ones that judge the method)

A rate alone is not meaningful, because a decoder that says `C` to everything scores TPR(C)=1 and FPR(C)=1. What matters is the *gap* between how it treats real tokens and how it treats noise. Two standard ways to express that gap:

**Discrimination(C), the absolute separation.**
Equation: `Discrimination(C) = TPR(C) - FPR(C)`.
Term by term: it subtracts the noise hit-rate from the real hit-rate at the committed bar. Range -1 to +1. `0` means the method certifies noise exactly as often as real tokens, i.e. no ability to tell them apart. Positive means it favors real tokens; the larger, the better the separation. This is the single headline number.

**Enrichment(C), the relative separation.**
Equation: `Enrichment(C) = TPR(C) / FPR(C)`.
Term by term: how many times more likely a `C` label is on a real token than on a noise string. `1x` means a `C` is equally likely on noise as on signal (worthless). `3x` means a real token is three times likelier to earn `C` than noise is. Enrichment is more intuitive when both rates are small (as here), where a difference like 0.20 vs 0.06 looks tiny in absolute terms but is a real 3x effect.

### Worked example (Battery A, pooled)

`P_C = 31`, `|P| = 500`, so `FPR(C) = 31/500 = 0.062`.
`R_C = 31`, `|R| = 150`, so `TPR(C) = 31/150 = 0.207`.
`Discrimination(C) = 0.207 - 0.062 = +0.145`.
`Enrichment(C) = 0.207 / 0.062 = 3.3x`.
Reading: at the committed bar the method certifies about 6% of pure noise and about 21% of real tokens, so a `C` label is 3.3x more likely on signal than on noise, a real but modest separation.

### Why both a strict bar (C) and a loose bar (C+soft)

Reporting FPR/TPR at both the `C` bar and the `C+soft` bar shows how the method behaves as the acceptance threshold is loosened. If the soft tier were adding real signal, dropping to `C+soft` would raise TPR much more than FPR. In practice it raises both almost equally (the discrimination at the found level is only about +0.10), which is the quantitative basis for the finding that soft readings are close to noise.

## Battery A: offline dictionaries (complete, 5 seeds)

Sources available to the decoders: full Yucatec (Cordemex), full K'iche' (Christenson), full Nawat (Campbell), Spanish->Maya wordlist, and a small Nahuatl wordlist. The primary Classical Nahuatl source (Wired Humanities, online) was NOT available. Reproduce any worksheet with `python3 gen_set.py <gen_seed>`.

| Set | Gen seed | Pseudo C / soft / none | Real C / soft / none | FPR(C) | FPR(C+soft) | TPR(C) | TPR(found) | Discrim.(C) |
|---|---|---|---|---|---|---|---|---|
| 1 | 1729 | 4 / 65 / 31 | 6 / 18 / 6 | 0.04 | 0.69 | 0.20 | 0.80 | +0.16 |
| 2 | 9001 | 7 / 49 / 44 | 7 / 14 / 9 | 0.07 | 0.56 | 0.23 | 0.70 | +0.16 |
| 3 | 271828 | 11 / 73 / 16 | 7 / 20 / 3 | 0.11 | 0.84 | 0.23 | 0.90 | +0.12 |
| 4 | 42 | 5 / 67 / 28 | 5 / 16 / 9 | 0.05 | 0.72 | 0.17 | 0.70 | +0.12 |
| 5 | 55555 | 4 / 50 / 46 | 6 / 16 / 8 | 0.04 | 0.54 | 0.20 | 0.73 | +0.16 |

### Battery A pooled (500 pseudo + 150 real)

| Metric | Value |
|---|---|
| Pseudo: C / soft / none | 31 / 304 / 165 |
| Real: C / soft / none | 31 / 84 / 35 |
| FPR(C) | 0.062 |
| FPR(C+soft) | 0.670 |
| TPR(C) | 0.207 |
| TPR(found) | 0.767 |
| Discrimination(C) | +0.145 |
| Enrichment at C (TPR/FPR) | 3.3x |

## What Battery A says

1. **The "soft" tier carries almost no evidential weight.** The method assigned a soft-or-better root to 67% of pure noise, versus 77% of genuine committed tokens: a ten-point gap. "We found a plausible attested root (soft)" happens nearly as readily for random Vaal-shaped strings as for real ones. Soft readings should be relabeled "candidate," not cited as support.

2. **The "committed" tier discriminates, modestly and stably.** A `C` label is about 3.3x more likely on a real token than on noise (20.7% vs 6.2%), and the effect held on every seed (discrimination +0.12 to +0.16, TPR(C) a tight 0.17 to 0.23). The strict, attestation-required, form-first bar is doing real work. But roughly 1 pure-noise string in 16 still earns "committed-quality," so `C` is a positive signal, not proof.

3. **The result is highly reproducible.** Five independent seeds, and the headline numbers barely move. The one volatile figure is FPR(C+soft) (0.54 to 0.84), i.e. how permissive the soft tier is, which is exactly the least trustworthy metric.

## Known bias in Battery A (both directions)

The decoders lacked the primary Classical Nahuatl source (online). A large share of real committed tokens are Nahuatl-sourced (Atziri, Eztli, pochiti, tlayeb, kilya, qexcan), so the agents often could not confirm them and marked soft or none. This depresses TPR and understates true discrimination; the real `C`-tier separation is probably better than +0.145. The same gap also understates FPR (some noise strings that are "really" Nahuatl-shaped went unconfirmed). Battery B corrects this.

## Battery B: online Nahuatl access (complete, 5 seeds)

Identical worksheets (same seeds, same pseudo strings, same real plants), fresh agents, with the one change that decoders may consult the Wired Humanities Nahuatl Dictionary and the Gran Diccionario Nahuatl online in addition to the offline files. This isolates the effect of full Nahuatl access. Expected direction: TPR rises (real Nahuatl tokens now confirmable); FPR may also rise (noise strings now matchable against a far larger Nahuatl lexicon). The quantity that matters is whether discrimination widens or narrows.

Complete, 5 seeds.

| Set | Gen seed | Pseudo C / soft / none | Real C / soft / none | FPR(C) | FPR(C+soft) | TPR(C) | TPR(found) | Discrim.(C) |
|---|---|---|---|---|---|---|---|---|
| 1 | 1729 | 4 / 49 / 47 | 5 / 12 / 13 | 0.04 | 0.53 | 0.17 | 0.57 | +0.13 |
| 2 | 9001 | 6 / 44 / 50 | 5 / 13 / 12 | 0.06 | 0.50 | 0.17 | 0.60 | +0.11 |
| 3 | 271828 | 10 / 48 / 42 | 6 / 16 / 8 | 0.10 | 0.58 | 0.20 | 0.73 | +0.10 |
| 4 | 42 | 7 / 45 / 48 | 5 / 11 / 14 | 0.07 | 0.52 | 0.17 | 0.53 | +0.10 |
| 5 | 55555 | 13 / 62 / 25 | 5 / 20 / 5 | 0.13 | 0.75 | 0.17 | 0.83 | +0.04 |

### Battery B pooled (500 pseudo + 150 real)

| Metric | Value |
|---|---|
| Pseudo: C / soft / none | 40 / 248 / 212 |
| Real: C / soft / none | 26 / 72 / 52 |
| FPR(C) | 0.080 |
| FPR(C+soft) | 0.576 |
| TPR(C) | 0.173 |
| TPR(found) | 0.653 |
| Discrimination(C) | +0.093 |
| Enrichment at C (TPR/FPR) | 2.2x |

Online Nahuatl was used sparingly and was decisive on only a handful of tokens per pass (typically 2 to 6, e.g. confirming *pochtli*, *nochtli*, *azcatl*, *itztli*, *xolotl*, *tlilli*), not a flood of new matches.

## Battery A vs Battery B: the key comparison

| Metric (pooled) | A: offline | B: online Nahuatl | change |
|---|---|---|---|
| FPR(C) | 0.062 | 0.080 | worse (more noise gets C) |
| FPR(C+soft) | 0.670 | 0.576 | lower |
| TPR(C) | 0.207 | 0.173 | lower |
| TPR(found) | 0.767 | 0.653 | lower |
| Discrimination(C) | +0.145 | +0.093 | **narrower** |
| Enrichment at C | 3.3x | 2.2x | **weaker** |

## The holistic finding

Adding a large, verifiable Classical Nahuatl source did **not** improve the method's ability to separate real tokens from noise. It made it slightly worse, and consistently so: discrimination fell on all five seeds (from about +0.15 to about +0.09). Two forces produced this, and both are informative.

First, the bigger, checkable lexicon raised the false-positive rate: with the full Wired Humanities Nahuatl dictionary in hand, more pure-noise strings found a genuine Nahuatl root to land on (FPR(C) 0.062 to 0.080). A larger dictionary is a larger net, and it catches noise too. This is the base-rate problem made concrete: coverage is not the bottleneck, permissive latitude over a vast combined search space is.

Second, with a definitive source the agents could *reject* as well as confirm. Both batteries graded pseudo and real with the same instance, but the online agents said "none" far more often (real none 35% vs 23% offline), because they could verify that a candidate root did not cleanly exist instead of granting a hopeful "soft." That rigor pulled TPR down as well as FPR, which is healthy, but the net effect on the gap between signal and noise was negative.

Both batteries agree on the two conclusions that matter:

- **Soft is not evidence.** Across ten passes the method rooted 58 to 67% of pure noise at soft-or-better, within about ten points of the real-token rate. A soft reading is close to what decoding noise produces.
- **Committed is a real but modest signal.** A `C` label runs 2 to 3x more likely on a real token than on noise, stable across seeds and across the offline/online change. It is a positive indicator, not proof, and better dictionaries do not sharpen it.

The actionable consequence is unchanged and now doubly supported: relabel soft readings as "candidates, not evidence," and make `C` earn its name with something the raw dictionary search cannot give it, an adversarial-survival requirement and a regular sound-correspondence check, rather than more dictionary coverage.

## Battery C: tightened latitude (offline, strict rules)

Per `TIGHTENED_LATITUDE.md`. Same 5 worksheets, seeds, and offline sources as Battery A; the ONLY change is a strict latitude (no cross-grafts, no free vowel raising/lowering, no metathesis, no ad hoc coda drops; loan-phoneme diagnostic kept; a root must match the surface with no unexplained residue).

| Set | Gen seed | Pseudo C / soft / none | Real C / soft / none | FPR(C) | FPR(C+soft) | TPR(C) | TPR(found) | Discrim.(C) |
|---|---|---|---|---|---|---|---|---|
| 1 | 1729 | 4 / 0 / 96 | 4 / 1 / 25 | 0.04 | 0.04 | 0.13 | 0.17 | +0.09 |
| 2 | 9001 | 2 / 1 / 97 | 5 / 1 / 24 | 0.02 | 0.03 | 0.17 | 0.20 | +0.15 |
| 3 | 271828 | 3 / 6 / 91 | 3 / 3 / 24 | 0.03 | 0.09 | 0.10 | 0.20 | +0.07 |
| 4 | 42 | 3 / 2 / 95 | 4 / 0 / 26 | 0.03 | 0.05 | 0.13 | 0.13 | +0.10 |
| 5 | 55555 | 5 / 6 / 89 | 3 / 3 / 24 | 0.05 | 0.11 | 0.10 | 0.20 | +0.05 |

### Battery C pooled (500 pseudo + 150 real)

| Metric | Value |
|---|---|
| Pseudo: C / soft / none | 17 / 15 / 468 |
| Real: C / soft / none | 19 / 8 / 123 |
| FPR(C) | 0.034 |
| FPR(C+soft) | 0.064 |
| TPR(C) | 0.127 |
| TPR(found) | 0.180 |
| Discrimination(C) | +0.093 |
| Enrichment at C | 3.7x |

## Battery D: tightened latitude + online Nahuatl (complete, 5 seeds)

The fourth cell of the latitude x dictionary-access 2x2: the Battery C strict ruleset AND the Battery B online Nahuatl access at once, same five seeded worksheets, fresh blind agents grepping the offline dictionaries plus consulting the Wired Humanities Nahuatl Dictionary and the Gran Diccionario Nahuatl online. Result files `blind_test_results_tight_online_s{seed}.csv`.

Pooled (500 pseudo + 150 real): FPR(C) 0.046 [3.1, 6.8], TPR(C) 0.140 [9.3, 20.5], FPR(C+soft) 0.094, TPR(found) 0.173, discrimination +0.094, enrichment 3.0x. Adding online Nahuatl under the strict rules (D vs C) nudges FPR (0.034 to 0.046) and TPR (0.127 to 0.140) up together, by a handful of Nahuatl confirmations that are genuine (*Eztli*) and spurious (a few Nahuatl-shaped noise strings) in roughly equal measure, so discrimination is unchanged (+0.093 to +0.094). This is exactly the pattern online access showed under the loose rules (B vs A): more coverage, not more separation.

## Four-battery comparison (the 2x2, pooled)

| Metric | A: loose / offline | B: loose / online | C: strict / offline | D: strict / online |
|---|---|---|---|---|
| FPR(C) | 0.062 | 0.080 | **0.034** | **0.046** |
| FPR(C+soft) | 0.670 | 0.576 | **0.064** | **0.094** |
| TPR(C) | 0.207 | 0.173 | 0.127 | 0.140 |
| TPR(found) | 0.767 | 0.653 | **0.180** | **0.173** |
| Discrimination(C) | +0.145 | +0.093 | +0.093 | +0.094 |
| Enrichment(C) | 3.3x | 2.2x | 3.7x | 3.0x |

## The two findings from Battery C

1. **The soft tier's false positives were entirely latitude-driven.** Tightening the rules collapsed FPR(C+soft) from 0.670 to 0.064, a roughly tenfold drop. Under strict rules 94% of pure noise correctly returns "none." This confirms the hypothesis directly: the permissive latitude, not the dictionary coverage, was manufacturing the false positives. The review's diagnosis is now demonstrated, not just argued.

2. **But the committed lexicon is not latitude-robust.** The same tightening dropped TPR(found) from 0.767 to 0.180. Under strict rules only about 18% of genuine committed tokens can be reconstructed at all, and only 13% at `C`. In other words, most committed readings *require* the loose latitude (vowel shifts, cross-grafts, coda drops) to exist. Enrichment stays about 3.7x, so a small real signal remains, but in absolute terms both noise and the bulk of the committed lexicon become undecodable together.

## Overall conclusion (the complete 2x2)

The method's apparent productivity is largely an artifact of latitude. Loosen the rules and it decodes almost everything, noise included (Battery A/B). Tighten them and it decodes almost nothing, the committed lexicon included (Battery C/D). A small hard core, on the order of 13 to 18% of tokens (the likes of *Eztli*, *naach*, *Maax*, *ek*), survives strict-latitude decoding, and that core is where the real, robust signal lives. Everything outside it is latitude-dependent: not necessarily wrong, but standing on rules permissive enough to root random noise about as often. With all four cells filled, the 2x2 reads cleanly: **latitude is the dominant axis** (strict C/D collapse both noise and lexicon; loose A/B inflate both), while **online dictionary access is a minor axis** that lifts FPR and TPR together on either latitude without widening discrimination. Coverage was never the bottleneck; latitude is.

Recommended framing for the project: define a **strict-committed** tier for tokens that survive strict-latitude decoding, hold those to the highest confidence, and honestly label the remaining committed tokens as latitude-dependent. That, plus the adversarial-survival rule (see `ADVERSARIAL_RESULTS.md`), gives the confidence system something the raw dictionary search never could: a floor that noise cannot easily clear.

## Battery E: blind certification of three post-battery names (strict + online, 5 seeds)

After the four-battery program, three onomastic tokens (*Quecholli*, *Panquetzaliztli*, *Ixchel*) were hardened and added to the lexicon; Battery E ran them back through the same blind, strict-plus-online decode so they would be null-tested rather than post-hoc. Each of the five seeds gave a fresh blind agent a shuffled 20-token worksheet (the 3 names + 12 Markov pseudo distractors + 5 real committed controls), with no answer key.

Result: the three names passed strict Gate-1 in all five passes (**15/15**). The controls calibrated to their known tiers (*naach* 5/5 and *ek* 4/5 hardened; *kutsen* 1/5 competitor; *sakilja* 0/5 and *kilya* 0/5 latitude-dependent), confirming the agents applied the same bar as A-D. Gate 2 was corroborated by unanimous single-language assignment (no cross-language competitor). Full detail and raw decodes: `BATTERY_E_RESULTS.md`, `battery_e_raw.md`.

Note on the distractor floor: the small 60-token distractor sample returned 10 false positives (16.7%), all accidental real lexemes the Markov produced by chance (e.g. *noche*, *otli*, *xolo*, *much*). This small, high-variance sample does not replace the Battery D 4.6% floor (measured over 500 pseudo), which the null-rejection test continues to use. Battery E is a target-certification run, not a floor re-measurement.

Effect on the base: the enlarged base (65 tokens / 56 distinct roots; 26 strict Gate-1 passes; 25 Hardened) is now itself null-tested and carries the headline figures in master §17; Batteries A-D (the 62-token run) are retained as the prior epoch.

