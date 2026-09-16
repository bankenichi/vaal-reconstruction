# Null-model protocol: measuring the decoder's false-positive rate

## Why this exists

The reconstruction's central risk is base-rate blindness. Mesoamerican languages have small phoneme inventories and simple CV(C) shapes, and the palette admits four source languages plus Spanish plus secondary pools, with several licensed sound-changes. Under those conditions almost any short, Vaal-shaped string can be matched to some attested root. "An attested root was found" is therefore only evidence if the method finds roots for real tokens *more often* than for strings that were never built from roots. This protocol measures that gap.

## Materials

- `generate_pseudo_vaal.py` -- the reference generator. Phonotactic model trained only on authentic Vaal surface forms; default seed 1729, fully reproducible (regenerates the identical set on re-run). A seed and shuffle-seed may be passed as arguments; `gen_set.py <seed>` produces the same worksheet for any other seed.
- `pseudo_vaal_test_set.txt` -- 100 pseudo-Vaal strings with no designed meaning.
- `blind_test_worksheet_s<seed>.csv` -- the 100 pseudo strings shuffled with 30 real committed Vaal tokens, labels hidden. This is what the decoder fills in.
- `blind_test_key_s<seed>.csv` -- which id is pseudo and which is real. Held aside until scoring.
- `TIGHTENED_LATITUDE.md` -- the strict-latitude ruleset used for the strict batteries (C and D).
- Result files, one per run, named by condition: `blind_test_results_s<seed>.csv` (loose/offline, A), `blind_test_results_online_s<seed>.csv` (loose/online, B), `blind_test_results_tight_s<seed>.csv` (strict/offline, C), `blind_test_results_tight_online_s<seed>.csv` (strict/online, D). Score with `score.py <results.csv> <key.csv>`.

## The design: a latitude x access 2x2

The test is run in four conditions, crossing two binary factors:

- **Latitude** -- loose (the project's standard permissive rules: cross-grafts, vowel raising and lowering, metathesis, and coda adjustments allowed) versus strict (`TIGHTENED_LATITUDE.md`: a root must match the surface with no unexplained residue).
- **Dictionary access** -- offline (Cordemex, Christenson, Campbell, the Spanish-Maya and small Nahuatl wordlists) versus online (the same, plus the Wired Humanities Nahuatl Dictionary and the Gran Diccionario Nahuatl).

The four cells are Battery A (loose / offline), B (loose / online), C (strict / offline), and D (strict / online). Every cell decodes the SAME five seeded worksheets (500 pseudo + 150 real, pooled), so the batteries differ only in the factor being varied. This isolates what each factor does to the signal-to-noise gap.

## Procedure

1. The decoder must be **blind to the key** -- a fresh agent instance or a collaborator who has not seen `blind_test_key_s<seed>.csv`. The analyst who built the lexicon must not grade their own recall.
2. For every row in the worksheet, the decoder applies the exact standards of the condition being tested: search the primary sources form-first, at the latitude for that battery (loose, or strict per `TIGHTENED_LATITUDE.md`) and with the access for that battery (offline or online). Record found (Y/N), the root, its source language, the gloss, and a confidence of `C` (committed-quality: attested root, workable phonology, sensible gloss) or `soft`.
3. No item is skipped; the decoder does not know which items are real.
4. Only after the whole worksheet is filled, join it to the key and score with `score.py`.
5. Run all four batteries across the five seeds to fill the 2x2. Re-run any battery after a change to the palette or the licensed sound-changes, since both move the false-positive rate directly.

## Scoring

Let P = the pseudo items (500 pooled), R = the real items (150 pooled).

- **FPR(C)** = (pseudo marked `C`) / |P|. The strict bar: how often pure noise is certified committed-quality.
- **FPR(C+soft)** = (pseudo marked C or soft) / |P|. The loose bar: how often noise gets any root at all.
- **TPR(C)** = (real marked `C`) / |R|.
- **TPR(found)** = (real marked C or soft) / |R|.
- **Discrimination(C)** = TPR(C) - FPR(C). Absolute separation; the headline number.
- **Enrichment(C)** = TPR(C) / FPR(C). Relative separation: how many times likelier a `C` is on a real token than on noise. More intuitive when both rates are small.

Full definitions, equations, and a worked example are in `NULL_MODEL_RESULTS.md`.

**Null-rejection test.** A battery's FPR(C) is the noise floor for a binomial test on the real committed lexicon: if the committed tokens' strict-pass count far exceeds what that floor predicts by chance, the all-noise hypothesis is rejected. The reconstruction quotes this against the strict-and-online floor (Battery D, FPR 0.046, the resources the real decode uses); see master §17.3.

## Interpretation

- **Discrimination near zero** (TPR approximately equals FPR): the method cannot tell designed tokens from noise. The committed lexicon is then not evidentiary, however careful each entry looks.
- **FPR above roughly 0.3**: `C` is being handed to noise too freely; the bar needs to be tightened.
- **High TPR with low FPR**: the method genuinely discriminates and the committed readings carry weight.
- **The 2x2 result** (full analysis in `NULL_MODEL_RESULTS.md`): latitude is the dominant axis. Strict rules collapse both noise and most of the lexicon together (only about 13 to 18% of real tokens survive), while loose rules inflate both. Dictionary access is a minor axis: going online lifts FPR and TPR together without widening discrimination. The strict-latitude survivors are the hardened core; everything else is latitude-dependent.

Record the numbers, the date, and the decoder used in the results log below each time the test is run.

## Honest caveats

- By design the pseudo strings share Vaal phonotactics with real tokens; a few may echo a real name-fragment shorter than four characters. That is intended (they must "sound Vaal") and does not undermine the test, because none has a designed meaning, so any `C` root found for them is a false positive by construction.
- This measures the *decoder's discipline and the palette's permissiveness*, not whether GGG actually built Vaal from these languages. That provenance question is separate and is discussed in `REVIEW.md`.
- 30 real plants per pass (150 pooled) is a small positive sample; treat TPR as indicative, not precise. Enlarge both sets if a firmer estimate is wanted.

## Results log

Pooled over 5 seeds per battery (500 pseudo + 150 real). Full per-seed tables and analysis in `NULL_MODEL_RESULTS.md`.

| Battery | Condition | FPR(C) | FPR(C+soft) | TPR(C) | Discrimination(C) | Enrichment(C) | Notes |
|---|---|---|---|---|---|---|---|
| A | loose / offline | 0.062 | 0.670 | 0.207 | +0.145 | 3.3x | baseline; committed clears noise ~3x |
| B | loose / online | 0.080 | 0.576 | 0.173 | +0.093 | 2.2x | more coverage, narrower gap |
| C | strict / offline | 0.034 | 0.064 | 0.127 | +0.093 | 3.7x | strict bar; 94% of noise returns "none" |
| D | strict / online | 0.046 | 0.094 | 0.140 | +0.094 | 3.0x | the noise floor the real decode uses |

The initial single-seed shakedown runs (offline, seeds 1729 / 9001 / 271828: FPR(C) 0.04 / 0.07 / 0.11, TPR(C) 0.20 / 0.23 / 0.23, discrimination +0.16 / +0.16 / +0.12) are superseded by the pooled Battery A row.
