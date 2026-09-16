# Tightened-latitude ruleset (Battery C)

## Purpose

Battery A and B showed that adding a larger dictionary did not improve discrimination, which points at the *latitude* (how much sound-change and segmentation freedom the decoder is granted), not the coverage, as the driver of false positives. Battery C tests that directly: same worksheets, same seeds, same offline sources, fresh blind agents, with the **only** change being a strict latitude. If the false-positive rate falls sharply while the true-positive rate holds, permissive latitude is confirmed as the cause of the noise-matching.

## The strict ruleset (what the Battery C decoder may and may not do)

Allowed:
- Doubled vowels represent length only (`aa` ~ `a`, `uu` ~ `u`, `ii` ~ `i`). No other vowel change.
- The apostrophe represents a glottal stop and may be present or absent, but only consistently within a token.
- The loan-phoneme diagnostic stands: a token containing `/f/`, `/d/`, `/g/`, or `/r/` is treated as a Spanish loan (or, for `/r/`, K'iche'), because those are loan-only in the Mayan/Nahuan core.
- A root is accepted only if it matches the surface form with **no unexplained residue**: every segment of the surface must be accounted for by the root plus a genuinely attested affix of the SAME language.

Forbidden (these are the latitudes Battery A allowed and Battery C removes):
- **No cross-grafts.** A Maya root may not take a Nahuatl affix, or vice versa. One language per token.
- **No free vowel raising or lowering** (no `a`~`u`, `o`~`u`, `e`~`i` substitutions of convenience).
- **No metathesis** (no reordering of segments to reach a root).
- **No ad hoc coda simplification.** A final cluster may be dropped only if that exact reduction is independently attested for the proposed root, not merely assumed (so a bare `-tl -> -to` or `-s`/`-ks` "romanization tail" is not granted for free).
- **No consonant substitution** outside the loan-phoneme diagnostic.

## Confidence bar (unchanged from the null model)

- `C` = attested root, clean phonology under the strict rules, sensible gloss.
- `soft` = attested root but with exactly one residual issue that the strict rules do not resolve.
- `none` = no attested root fits under the strict rules.

## Experiment

Reuse the five seeded worksheets (`blind_test_worksheet*.csv`, seeds 1729/9001/271828/42/55555). One fresh blind agent per seed, offline sources only (to isolate latitude from coverage against Battery A), strict ruleset above. Output `blind_test_results_tight_s{seed}.csv`. Score with `score.py` against the existing keys; pool as Battery C; compare FPR/TPR/discrimination to Battery A.

Prediction to test: FPR(C) and especially FPR(C+soft) drop substantially versus Battery A (0.062 / 0.670), while TPR holds up better than FPR falls, so discrimination widens. If instead TPR collapses alongside FPR, it would mean the real committed lexicon itself depends on the loose latitude, which would be an even more pointed finding.
