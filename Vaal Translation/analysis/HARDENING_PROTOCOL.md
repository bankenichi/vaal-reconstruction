# Lexicon hardening protocol

The standard test a token must pass to earn the top confidence tier. Apply this to every token going forward; cite this file in the token's entry when its tier is set or changed. The empirical basis for why these gates matter (the noise floor they clear) is in `NULL_MODEL_RESULTS.md`; run history is in `EXPERIMENT_LOG.md`.

## Why

The null-model batteries showed two things. Under loose latitude the decoder roots about 67% of pure-noise strings at soft-or-better, so a bare "attested root found" is close to worthless as evidence. Under strict latitude noise-matching collapses to about 6%, but so does the committed lexicon's own reconstructability (to about 18%). The tokens that survive strict rules AND have no equally-good competitor are the ones that clear the noise floor by a real margin. Hardening is the procedure that identifies them.

## The confidence taxonomy

- **H, Hardened** (top): the token passes BOTH gates below.
- **C, Committed (latitude-dependent)**: an attested root with sound phonology under the standard (loose) latitude, but it fails Gate 1 (needs a cross-graft, vowel shift, metathesis, or ad hoc coda drop) and/or has a logged competitor. Real, but standing on permissive rules.
- **S, Soft / candidate**: a plausible attested root with one unresolved step. Explicitly "candidate, not evidence." (These live in the appendix, not the committed lexicon.)
- **O, Opaque**: no attested root; reported as opaque.
- **L, Lore-anchored**: orthogonal tag, combined as needed (H+L, C+L, S+L). L marks narrative fit, never substitutes for root evidence.

## The two gates

### Gate 1, strict-latitude reconstruction
The token's root must reconstruct the surface form under the strict ruleset in `TIGHTENED_LATITUDE.md`: doubled vowels = length only; apostrophe = glottal (consistent); loan-phoneme diagnostic only; and the root plus a genuinely attested affix of the SAME language must account for every segment with no unexplained residue. Forbidden: cross-grafts, free vowel raising/lowering, metathesis, ad hoc coda simplification, consonant substitution outside the loan diagnostic.
PASS = an attested root reconstructs the surface legally under these rules, AND the recorded decode matches the predeclared committed root, language class, and sense (`score.py`, `match_committed.py`). A `C` label on a different lemma is not a pass (AUDIT_REVIEW F1).

**Residual limit.** Some Battery D online rows have empty root/lang/gloss columns; those trials are labelled unscorable for recovery rather than guessed. The 61-row `strict_committed_results_batch*.csv` files do carry the columns and are the Gate-1 source for the original battery.

### Gate 2, adversarial survival
A decoder blind to the current reading, given only the surface form, must NOT find an equal-or-stronger attested root carrying a DIFFERENT meaning. Same-language homophones and alternate segmentations count as competitors. (A same-meaning cognate in a sister language, or a same-language restatement of the committed lemma, is corroboration, not a competitor.) Language-class inequality is not required. See `score_adversarial.py`.
PASS = no genuine different-meaning competitor in the recorded adversarial CSV.

**Residual limit (AUDIT_REVIEW N3).** The archived `adversarial_results_batch*.csv` files store one best root and one alt-language root. A homophone a decoder never wrote down (for example the Gate-1 wasp reading of *ek*) cannot be scored from those files without inventing a row. Gate 1 already fails that token on sense mismatch. New adversarial runs would be needed to close the remaining gap.

## Outcome

| Gate 1 (strict) | Gate 2 (adversarial) | Tier |
|---|---|---|
| pass | pass | **H** |
| fail | pass | C |
| pass | fail | C (competitor logged) |
| fail | fail | C, flagged weak; consider demotion to S |
| no attested root at all | n/a | O |

## Procedure for any token (new or revisited)

1. Run Gate 1: attempt a strict-latitude reconstruction (ideally a fresh/blind decode; see the batch method in `EXPERIMENT_LOG.md`). Record pass/fail with the root and the exact residue if it fails.
2. Run Gate 2: a blind adversary reports the best cross-language competitor and its strength. Record survive/fall with the competitor.
3. Assign the tier from the table. In the token's lexicon entry, state the tier and add "hardened per HARDENING_PROTOCOL.md (Gate 1: pass/fail; Gate 2: pass/fail)".
4. A token not yet run through both gates is `C` at most, never `H`, and is marked "hardening pending."

## Standing rule

No token may carry the `H` tier without both gates recorded. `H` is earned, not assumed. Re-run both gates after any change to the palette or the latitude rules, since both move the noise floor. The 2026-09 recovery rescore of archived CSVs is a STOPGAP; a full blind re-run is `EXPERIMENT_RERUN_PROTOCOL.md`.
