# Translation battery results (T-M vs T-D)

Protocol: `TRANSLATION_BATTERY_PROTOCOL.md`. Gold key: `translation_battery_gold.csv` (extracted after all ten sheets existed). Scorer: `score_translation_battery.py`. This file is the headline home for **inter-translator and vs-gold agreement**. It is not a PPV, not a sentence-band product, and not a Fisher / 10^-15 null test.

**Do not read these rates as "probability the published English is the designer's intent."** Shared dictionaries imply shared bias. The CIs measure reproducibility under this kit.

## Headlines (Wilson 95% unless noted)

N per battery = 5 translators x 51 lines = **255 line-slots**.

### 1. Agreement with the project's published English

| Battery | Match | Match+partial |
|---|---|---|
| T-M (methodology on) | 27/255 = **10.6% [7.4, 15.0]** | 75/255 = **29.4% [24.2, 35.3]** |
| T-D (dictionaries only) | 22/255 = **8.6% [5.8, 12.7]** | 72/255 = **28.2% [23.1, 34.1]** |

Per-line match rate across the five translators (descriptive; the inferential unit for the table above is the 255 line-slots):

| Battery | Mean | Median | IQR |
|---|---:|---:|---|
| T-M | 0.106 | 0.000 | [0.000, 0.000] |
| T-D | 0.086 | 0.000 | [0.000, 0.000] |

Matches concentrate on a few lines (the vocative *Atziri!* lines 39/41/47 in both batteries; T-M *Kuxte' kíimil'* "life and death" 5/5). Most lines are 0/5 match.

Line-slot bins:

| Battery | match | partial | clash | abstain |
|---|---:|---:|---:|---:|
| T-M | 27 | 48 | 139 | 41 |
| T-D | 22 | 50 | 172 | 11 |

T-M abstains more (41/255 vs 11/255). T-D clashes more (172 vs 139). That is the anti-forcing contrast. It does not, by itself, raise vs-gold match+partial.

### 2. Inter-translator reproducibility (no gold)

Two translations of the same line are **compatible** if both abstain, or if neither abstains and their content-lemma Jaccard (synonym-folded, opaque bracket text dropped) is at least 0.30. Name-only empty remainder is compatible with another empty remainder.

| Battery | Pairwise compatible (10 pairs x 51 lines) | Lines with a 4/5 compatible clique |
|---|---|---|
| T-M | 247/510 = **48.4% [44.1, 52.8]** | 18/51 = **35.3% [23.6, 49.0]** |
| T-D | 237/510 = **46.5% [42.2, 50.8]** | 19/51 = **37.3% [25.3, 51.0]** |

Translators often agree with each other on dictionary-gloss salad that is not the published English. Pairwise reproducibility is about half; 4/5 cliques are about one third of lines. The two batteries are similar on this axis.

### 3. Methodology effect (T-M minus T-D)

Nonparametric bootstrap of the 255 line-slots per battery, 10,000 resamples, 95% percentile interval.

| Rate | Point (T-M - T-D) | 95% percentile CI |
|---|---:|---|
| Match | +0.020 | **[-0.031, +0.071]** |
| Match+partial | +0.012 | **[-0.067, +0.090]** |

Both intervals include zero. **Methodology is not moving the needle on vs-gold line agreement on this corpus.** The non-binding hypothesis that T-M would raise match+partial is not supported at this N. T-D did produce more clashes and more Spanish-gloss drift (clear on line 9: T-M 5/5 life+death, T-D 5/5 cacao-tree+death). That shows up as extra clash and extra abstain on T-M, not as a detectable lift in match+partial.

### 4. Secondary: load-bearing token glosses offered in notes

Particles excluded: a'te, u'te, le, le', ti, ti', ka, ta', u, ma, ma', na', en. Unchanged names Atziri / Zerphi / Vaal excluded. Tokens with no offered gloss are unscored, not abstain.

| Battery | Token match | Token match+partial |
|---|---|---|
| T-M | 103/512 = **20.1% [16.9, 23.8]** | 104/512 = **20.3% [17.1, 24.0]** |
| T-D | 71/528 = **13.4% [10.8, 16.6]** | 73/528 = **13.8% [11.1, 17.0]** |

The token-level Wilson intervals do not overlap. Form-first / palette search raises agreement of **offered** glosses with the gold line's content words, even when the composed English sentence still clashes. This is not PPV. Notes-parsing is coarser than the line rubric.

## Secondary (hypothesis-aligned, not the translation-confidence headline)

The protocol's non-binding hypothesis said T-D may clash more or drift to Spanish glosses, and that T-M should abstain when opaque. Those contrasts are measured here. They are **not** vs-gold match rates.

| Battery | Clash | Abstain |
|---|---|---|
| T-M | 139/255 = **54.5% [48.4, 60.5]** | 41/255 = **16.1% [12.1, 21.1]** |
| T-D | 172/255 = **67.5% [61.5, 72.9]** | 11/255 = **4.3% [2.4, 7.6]** |

Bootstrap T-M minus T-D (10,000 line-slots):

| Rate | Point | 95% percentile CI |
|---|---:|---|
| Clash | -0.129 | **[-0.212, -0.043]** |
| Abstain | +0.118 | **[+0.067, +0.169]** |

Neither interval includes zero. Methodology **does** change decoder behavior: T-M withholds more, T-D asserts a wrong English line more often. That behavioral split does not show up as a detectable lift in match or match+partial (section 3). Shared dictionaries still pull both batteries into the same false friends when they do assert.

## Exploratory (labeled; not headlines)

Computed from the same scored sheets (`explore_translation_battery.py`, `translation_battery_explore.csv`). Small-N CIs are wide on purpose. No Fisher / 10^-15 test. No PPV.

### Per-text match+partial

Line counts: T1 8, T2 16, T3 13, T4 12, T5 2. Slot totals are those counts times 5.

| Text | T-M match+partial | T-D match+partial | Bootstrap TM-TD mp |
|---|---|---|---|
| T1 chant | 10/40 = 25.0% [14.2, 40.2] | 12/40 = 30.0% [18.1, 45.4] | -0.05 [-0.25, +0.15] |
| T2 litany | 13/80 = 16.2% [9.7, 25.8] | 12/80 = 15.0% [8.8, 24.4] | +0.01 [-0.10, +0.13] |
| T3 commander | 12/65 = 18.5% [10.9, 29.6] | 10/65 = 15.4% [8.6, 26.1] | +0.03 [-0.09, +0.15] |
| T4 drill | 35/60 = 58.3% [45.7, 69.9] | 35/60 = 58.3% [45.7, 69.9] | +0.00 [-0.17, +0.17] |
| T5 Kamasan | 5/10 = 50.0% [23.7, 76.3] | 3/10 = 30.0% [10.8, 60.3] | +0.20 [-0.20, +0.60] |

T4 looks easier only because three vocative *Atziri!* lines contribute 15/15 matches in each battery. T3 has **zero** matches in both batteries. Per-text difference CIs all include zero. Heterogeneity is real (T3 vs T4), but it is not a methodology-by-text interaction that this N can pin down.

### Vocative-name sensitivity

Drop lines 39, 41, 47 (*Atziri!* only). Remaining N = 240.

| Battery | Match | Match+partial |
|---|---|---|
| T-M | 12/240 = 5.0% [2.9, 8.5] | 60/240 = 25.0% [19.9, 30.8] |
| T-D | 7/240 = 2.9% [1.4, 5.9] | 57/240 = 23.8% [18.8, 29.5] |

TM-TD match+partial remains +0.013 [-0.067, +0.088]. The vocatives inflate the headline match rate by about six points in both batteries equally. They do not create a fake methodology effect.

### Clash hotspots

Sixteen lines are 5/5 clash in **both** batteries (16/51 = 31.4% of the corpus). Shared misses, not methodology: lines 3, 6, 10, 11, 15, 16, 18, 21, 24, 27, 36, 37, 38, 43, 45, 49. Recurring false friends include *ik'el* as breath/bug/virus rather than spirit, *kutsen* as turkey/brush rather than offering, *'Ibil* as shake rather than flesh, and *mucane* as buried rather than mighty.

Largest T-M vs T-D split on match+partial: **line 9** (*Life and death!*): T-M 5/5 match, T-D 5/5 clash (cacao-tree + death). Next: line 32 (4/5 vs 2/5 partial on white-water / draught), line 51 (3/5 vs 1/5 dark+cast). Largest T-D advantage: line 20 (*the good place*), 0/5 vs 3/5, where T-M mostly abstained on *yutsal* and T-D used the Cordemex *yutsal* "all-good" hit.

### Translator slots

Match+partial per 51-line sheet: T-M 25.5% to 33.3%; T-D 23.5% to 37.3%. Slot spread is larger than the pooled TM-TD gap. A single noisy translator is enough to move the pooled point by a few points. The headline CIs already swallow that.

### Declared confidence vs vs-gold bin

| Battery | Declared | n | Match vs gold |
|---|---|---:|---|
| T-M | high | 19 | 17/19 = 89.5% [68.6, 97.1] |
| T-M | medium | 60 | 8/60 = 13.3% [6.9, 24.2] |
| T-M | low | 135 | 2/135 = 1.5% [0.4, 5.2] |
| T-D | high | 15 | 15/15 = 100% [79.6, 100] |
| T-D | medium | 60 | 2/60 = 3.3% [0.9, 11.4] |
| T-D | low | 169 | 5/169 = 3.0% [1.3, 6.7] |

High-confidence claims are almost all the vocative *Atziri!* lines plus T-M *life/death* and a few *first sign / living* hits. T-M's two high-confidence clashes are seed-42 lines 15-16 (*shake* / *bug* for flesh / spirit). Medium and low are not calibrated to vs-gold match. Abstain maps to the abstain bin by construction.

### Inter-rater on vs-gold bins (exploratory)

Fleiss kappa across five translators on the four vs-gold bins: T-M **0.61**, T-D **0.61**. Pairwise same-bin: T-M 384/510 = 75.3% [71.4, 78.8]; T-D 412/510 = 80.8% [77.1, 84.0]. This is agreement on **which bin they land in**, including shared clash. It is higher than gold-free Jaccard compatibility (section 2) because "everyone clashed" counts as same-bin. Substantial kappa here means the kit reproduces the same errors, not that the English is right.

### Token-level confusion (offered glosses)

Highest clash counts among scored note-glosses:

- *ik'el*: T-M 24/25 clash, T-D 21/25 clash (spirit vs breath/bug/virus).
- *kutsen*: 15/15 clash in both (offering vs turkey/brush).
- *'ibil*: T-M 8/10, T-D 10/10 clash (flesh vs shake).
- *mucane*: more abstain under T-M (10/20 clash + 10 abstain) vs T-D 16/21 clash (mighty vs buried).
- *tlayeb*: T-M mostly abstain (16/22); T-D mostly clash (19/25 ladder). Anti-forcing shows up as silence rather than a correct "dark" gloss.

## Rubric (vs gold)

- **match:** same main predication and referents. Wording may differ. *Alive, death!* counts as match to *Life and death!*
- **partial:** same main predication / referents with different wording, or a minor role / sense error (for example *ek'* as dark/black rather than star on line 1). Recovering only the interrogative *who* on a *Máax* line is partial, not match.
- **clash:** different predication or referents. *Wasp* for gold *star* is clash. *Cacao-like tree* for gold *life* is clash. *Atziri* plus a wrong content noun (servant for essence) is clash, not a name-only gift.
- **abstain:** translator confidence is abstain, or the translation field is empty.

Default is clash. Name-only overlap is match only when gold itself is the vocative *Atziri!* (lines 39, 41, 47).

## Blinding proof

- Translator packets (`translation_battery_TM_packet/`, `translation_battery_TD_packet/`) contain numbered surface lines, no published English. A search of those directories for gold phrases (*star of the mighty Vaal*, *Behold the blaze*, *Life and death*, *undying as Zerphi*, *eternal waters*) is empty.
- Gold (`translation_battery_gold.csv`) was extracted with `translation_battery_extract_gold.py` after all ten sheets existed.
- None of the ten sheets contains those gold phrases.
- T-D translators were forbidden the methodology packet (AGENTS form-first / palette, HARDENING_PROTOCOL, TIGHTENED_LATITUDE). T-M translators were forbidden gold, §9, `committed_readings.csv`, and other sheets.
- Dictionaries were opened from `VAAL_DICT_DIR=/tmp/vaal_dicts` (hashed uploads). They are not in git (`.gitignore`).

## What the numbers are not

- Not PPV, not a product-of-token sentence band, not a claim that the published English is correct.
- Not a test that Vaal is "not random." No 10^-15 headline.
- Shared Cordemex / Christenson / Nahuatl lists pull independent slots toward the same false friends (*ek* wasp, *kuxte'* cacao-tree, *ik'el* virus/bug). CIs are under this kit.

## Files

- Protocol: `TRANSLATION_BATTERY_PROTOCOL.md`
- Packets: `translation_battery_TM_packet/`, `translation_battery_TD_packet/`
- Sheets: `translation_battery_TM_s{seed}.csv` / `.md` and `TD` (seeds 1729, 9001, 271828, 42, 55555)
- Gold: `translation_battery_gold.csv`
- Scores: `translation_battery_line_scores.csv`, `translation_battery_token_scores.csv`, `translation_battery_pairwise.csv`, `translation_battery_score_summary.csv`, `translation_battery_explore.csv`
- Scorer: `score_translation_battery.py`
- Exploratory: `explore_translation_battery.py`

Reproduce: `python3 translation_battery_extract_gold.py && python3 score_translation_battery.py && python3 explore_translation_battery.py`
