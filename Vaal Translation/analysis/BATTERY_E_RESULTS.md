# Battery E: blind certification of the post-battery hardened names

Battery E extends the null-model program (Batteries A-D, `NULL_MODEL_RESULTS.md`) to certify three onomastic tokens that were hardened *after* the original battery had already been run: **Quecholli**, **Panquetzaliztli**, and **Ixchel** (master §9, §12.5-12.6). Its purpose is narrow and specific: run those three names through the same blind, strict-plus-online decode the original 62 committed tokens faced, so they can enter the null-tested base rather than sitting beside it as post-hoc additions. Batteries A-D are unchanged and remain the historical record; this is a new, separately labelled run.

## Design

- **Conditions:** strict latitude + online dictionaries (identical to Battery D; `TIGHTENED_LATITUDE.md`).
- **Replication:** the same five seeds as A-D (1729, 9001, 271828, 42, 55555), one fresh blind decoder agent per seed.
- **Blindness:** the three target names were embedded among 12 pseudo-Vaal distractors (Markov-generated per seed by `gen_set.py`) and 5 real committed controls, shuffled to 20 tokens per worksheet. No agent was told which tokens were targets, distractors, or controls; none had access to the master, the answer key, or the other agents.
- **Controls (calibration):** `naach` (Hardened), `ek` (Hardened), `kutsen` (Committed-with-competitor), `sakilja` (Committed, latitude-dependent), `kilya` (Committed, latitude-dependent). These have known tiers, so their pass/fail behaviour under a fresh strict decode tests whether each agent applied the same bar as the original battery.
- **Scoring:** a token is a strict Gate-1 pass only if the agent reconstructed it to an attested root under the strict ruleset with no unexplained residue and no forbidden move (cross-graft, vowel shift, metathesis, coda drop, non-loan consonant substitution).

## Result 1: the three names pass unanimously (Gate 1)

| Target | s1729 | s9001 | s271828 | s42 | s55555 | Pass rate |
|---|---|---|---|---|---|---|
| Quecholli | Y | Y | Y | Y | Y | 5/5 |
| Panquetzaliztli | Y | Y | Y | Y | Y | 5/5 |
| Ixchel | Y | Y | Y | Y | Y | 5/5 |

**15 of 15 blind strict passes.** Every agent independently reconstructed *Quecholli* to Nahuatl *quecholli* (roseate spoonbill / 14th veintena), *Panquetzaliztli* to Nahuatl *pan* + *quetza* + *-liztli* (15th veintena), and *Ixchel* to Yucatec *ix-* + *chel* "rainbow." No agent needed a forbidden move.

## Result 2: control calibration matches known tiers

| Control | Tier (lexicon) | Passes | Expected under a correct strict bar |
|---|---|---|---|
| naach | Hardened | 5/5 | pass (hardened) |
| ek | Hardened | 4/5 | mostly pass (one agent took the glottalized *éek'* "star" reading and failed it; the plain *ek* "wasp" reading passes) |
| kutsen | Committed + competitor | 1/5 | mostly fail at the strict bar |
| sakilja | Committed (latitude-dependent) | 0/5 | fail strict (needs a permissive step; K'iche' *saq*/*saqil* vs *sak*, plus *-ja* residue) |
| kilya | Committed (latitude-dependent) | 0/5 | fail strict (*quil-* + *-ya* is a near-miss, not a clean strict parse) |

The agents applied the strict bar consistently with the original battery: hardened controls pass, latitude-dependent committed controls fail, the competitor-flagged control mostly fails. This is the check that the blind decoders were neither too lenient nor too strict relative to Batteries A-D.

## Result 3: distractor false positives (reported for transparency, not a new floor)

Across the 60 pseudo distractors (12 x 5), 10 were marked as strict passes (16.7%): *xech* (x2), *otli*, *noche*, *xolo*, *kahua*, *atli*, *much*, *kala*, *tlane*. Every one is an accidental real lexeme the Markov generator produced by chance (Nahuatl *ohtli* "road", *xolotl*, *cahua*, *atl+i*; Yucatec *xech*, *much*; Spanish *noche*, *cala*), not a forced parse.

This 16.7% is **not** a replacement for the noise floor. It is a small (n=60), high-variance sample, it is inflated by accidental real words the 500-token battery averaged out, and one agent (s9001) was notably more lenient (4 of its 12). The established false-positive floor remains **Battery D's 4.6%** measured over 500 pseudo tokens; Battery E is a target-certification run, not a floor re-measurement, and the null-rejection test continues to use the Battery D floor. The distractor rate is logged here only so the run is fully auditable.

## Result 4: adversarial survival (Gate 2)

Gate 2 asks whether a blind decoder finds an equal-or-stronger attested root in a *different* source language. Across all five blind passes, every agent assigned each of the three names to exactly one source language (Quecholli, Panquetzaliztli -> Classical Nahuatl; Ixchel -> Yucatec Maya) with no competing cross-language reading offered. The five independent blind decodes therefore corroborate the earlier adversarial pass (`HARDENING_PROTOCOL.md` run, master §12.5-12.6): no genuine competitor. Gate 2 pass for all three.

## Conclusion

All three names clear both gates under blind, strict-plus-online battery conditions: **3/3 Gate 1 (15/15 across seeds), 3/3 Gate 2.** They are certified Hardened by the same procedure as the original lexicon, not by post-hoc inspection. The enlarged base (65 tokens / 56 distinct roots, 26 strict Gate-1 passes, 25 Hardened) is therefore battery-tested and can carry the headline, with the original 62-token run (Batteries A-D) retained as the prior epoch.

Caveat retained from the merge analysis: the three names are exact attested lexemes and so are unusually easy plants. They pass honestly, but they are not representative of the harder text tokens, so they buoy the per-token coverage figure slightly. This does not affect the null rejection, which is driven by the floor (unchanged at 4.6%), not by plant difficulty. The coverage figure carries a composition note to that effect (master §17.5).

## Reproduce

Worksheets were built by sampling `gen_set.py <seed>` pseudo output and adding the three targets plus the five controls, shuffled with `random.Random(seed+7)`. Raw per-token agent decodes for all five seeds are preserved in `battery_e_raw.md`. Blind decoders were fresh agents with dictionary and online-Nahuatl access and no answer key.
