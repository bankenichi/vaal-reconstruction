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
- Scores: `translation_battery_line_scores.csv`, `translation_battery_token_scores.csv`, `translation_battery_pairwise.csv`, `translation_battery_score_summary.csv`
- Scorer: `score_translation_battery.py`

Reproduce: `python3 translation_battery_extract_gold.py && python3 score_translation_battery.py`
