# Translation battery protocol (T-M and T-D)

Blind, line-level English translation of the closed surface corpus (Texts 1-4 plus Kamasan Smith: 51 numbered lines, 186 whitespace tokens). This is not a null-model token decode and not a p-value exercise. The headlines are Wilson 95% confidence intervals on agreement rates (vs the project's published English, and among translators).

Related files: `syntax_rerun_corpus_real.txt`, `syntax_rerun_build_packets.py`, `dict_lookup.py`, `TRANSLATION_BATTERY_RESULTS.md`, `translation_battery_gold.csv` (scoring only), `EXPERIMENT_LOG.md`.

## 1. Why

The withdrawn PPV / sentence-band numbers in master §17.5 answered a different question (model-based "probability a certified root is genuine"). They are not inter-translator agreement and they are not agreement with the published line English. This battery measures those agreement rates under two information conditions, with CIs.

## 2. Batteries

Seeds / analyst slots: **1729, 9001, 271828, 42, 55555**. Five independent translators per battery. N = 5 sheets x 51 lines = **255 line-slots per battery**.

| Battery | Inputs while translating | Blind to |
|---|---|---|
| **T-M** (methodology on) | Surface corpus only + methodology packet + dictionaries (form-first `dict_lookup.py`) | Published English; master §9 committed glosses; `committed_readings.csv`; other translators' sheets; §17 answers; the gold key |
| **T-D** (dictionaries only) | Surface corpus only + dictionaries/sources | Same blinds as T-M, **plus** the methodology packet (no AGENTS form-first / palette search order, no HARDENING_PROTOCOL, no TIGHTENED_LATITUDE, no project search-order) |

Packets live in `translation_battery_TM_packet/` and `translation_battery_TD_packet/`. Dictionaries are decode-only and are never committed.

## 3. Corpus

Reuse the 51-line surface-only packet built by `syntax_rerun_build_packets.py` from the canonical master (Texts 1-4 + Kamasan Smith). No English in translator packets. Ahuatotli and Mektul skill-cries stay excluded (master §3.2).

## 4. Methodology packet (T-M only)

Tracked copies under `translation_battery_TM_packet/`:

- `methodology.md`: AGENTS hard rules on form-first search, anti-forcing (opaque stays opaque), and palette search order. Finished English translations of corpus lines are stripped. The *Ela* / *ukto* example is reduced to the rule (neighboring attested tokens may bound a search; a token's own prior English may not).
- `HARDENING_PROTOCOL.md`: two-gate confidence taxonomy. Translators are not scoring the committed lexicon; they use the gates as a bar for trusting a dictionary hit.
- `TIGHTENED_LATITUDE.md`: strict reconstruction rules.

Do not include `STATISTICAL_SUMMARY.md`, master §9, master §17, or `committed_readings.csv` in this packet.

## 5. Dictionaries (decode only, never git)

Cordemex, norma_maya, kiche_christenson, ilide Spanish-Maya, Campbell Pipil/Nawat, Nahuatl 1100 wordlist. Paths: `VAAL_DICT_DIR` or the hashed upload copies. `dict_lookup.py` searches by **surface form**. It does not load committed readings or gold.

T-M: prefer `dict_lookup.py` over hallucinated roots. Try strict latitude first; use loose only if strict misses. Follow palette order when several hits remain. If nothing attested fits, **abstain** (opaque stays opaque).

T-D: dictionaries and sources only. No palette order and no project latitude rules. Translators may use any dictionary hit they judge useful, including Spanish. They may still abstain. They must not open the methodology packet.

## 6. Translator task

Each of the 10 slots writes a full best-effort English translation of every numbered line.

Required fields: `line_id`, `translation`, `confidence` (high / medium / low / abstain), `notes`.

Notes may list per-token root / language / gloss when found. Abstain is allowed when the line is opaque. Proper names that are already Latin-script in the surface (Atziri, Zerphi, Vaal as a name) may be kept.

Isolation: when filling a sheet, open only that battery's packet plus dictionaries / `dict_lookup.py`. Do not open the master English sections, §9, other sheets, or `translation_battery_gold.csv`.

Tie-break among equally plausible hits: `random.Random(seed).choice` after sorting candidates by folded lemma length descending. Seeds are the analyst slots above.

Raw sheets:

- `translation_battery_TM_s{seed}.md` (table) and `.csv`
- `translation_battery_TD_s{seed}.md` (table) and `.csv`

## 7. Gold key (scoring only)

After all 10 sheets exist, extract the project's published English line translations from the master (same 51-line closed set) into `translation_battery_gold.csv`. Translators must never see this file while drafting. Builder: `translation_battery_extract_gold.py`.

## 8. Scoring (after all sheets)

Per line per translator, against gold:

- **match**: same main predication and the same referents; wording may differ if the claim is the same.
- **partial**: same main predication / referents, different wording, or a minor role error (for example agent/patient swap on an otherwise right event).
- **clash**: different predication or different referents.
- **abstain**: translator confidence is abstain, or the translation is empty / "opaque" with no English claim.

Whole-line abstain is scored abstain even if notes list token guesses.

### Load-bearing tokens (secondary)

A **load-bearing content token** is any whitespace token that is not a pure particle, not punctuation-only, and not a proper name copied unchanged from the surface.

Particles (excluded unless the translator's note treats them as content): `a'te`, `u'te`, `u'te`, `le`, `le'`, `ti`, `ti'`, `ka`, `ta'`, `u`, `ma`, `ma'`, `na'`.

Proper names copied unchanged (excluded from the token rate, counted in the line): `Atziri`, `Zerphi`, `Vaal` when used as a name.

For each load-bearing token where the translator offered a gloss in notes, score that gloss match / partial / clash / abstain against the gold line's corresponding content. Tokens with no offered gloss are unscored (not abstain, not clash). Documented in the results file.

### Inter-translator reproducibility (no gold)

Two translations of the same line are **mutually compatible** if they share the same main predication and referents under the match-or-partial rule applied to each other (not to gold). Wording differences and minor role errors still count as compatible. Abstain is compatible only with abstain.

- Pairwise same-bin rate: among the 10 translator-pairs x 51 lines = 510 pair-lines per battery, the share that are mutually compatible.
- 4/5 agreement: share of 51 lines where at least one compatibility clique has size >= 4 (at least four translators pairwise compatible with each other). Wilson CI on that 51-trial rate.

## 9. Headlines (Wilson 95% CIs)

Wilson interval on a binomial proportion. No Fisher / 10^-15 headlines. Do not invent PPV from recovery TPR.

1. Per battery: share of line-slots that are **match**, and that are **match+partial**, pooling 5 translators x 51 lines (N = 255). Also per-line match rate across 5 translators: median and IQR, plus mean with a Wilson CI treating the 51 line-rates as if they were not the inferential unit (the inferential unit for the headline remains the 255 line-slots; the per-line summary is descriptive).
2. Per battery: inter-translator reproducibility without gold, as in §8, with Wilson CIs.
3. **Methodology effect:** difference (T-M minus T-D) in match rate and in match+partial rate. Interval: nonparametric bootstrap of line-slots, 10,000 resamples, 95% percentile CI. Documented in the results. Plain English: does methodology change agreement with the project translation, and by how much?
4. Optional secondary: the same CIs at load-bearing-token level.

Further summaries the sheets support (per-text rates, clash hotspots, abstain CIs, token confusion, slot spread, declared-confidence calibration, Fleiss kappa on vs-gold bins) may be reported if they are **labeled exploratory** and do not replace the headline Wilson tables. Still no Fisher / 10^-15 headlines. Do not invent PPV from recovery TPR.

Small print: shared dictionaries imply shared bias. CIs measure reproducibility under this kit, not designer intent.

## 10. Hypothesis (non-binding)

T-M should raise match+partial vs gold if methodology constrains search. T-D may produce more clashes or Spanish-gloss drift. If rates are similar, methodology is not moving the needle on this corpus.

## 11. Reproduce

```
python3 syntax_rerun_build_packets.py
python3 translation_battery_extract_gold.py
python3 translation_battery_lookup_dump.py
python3 score_translation_battery.py
python3 explore_translation_battery.py
```

Gold extraction and scoring run only after the ten sheets exist. Do not hand gold or scores to a translator mid-draft.
