# Vaal Translation

A reconstruction of the "Vaal language" (Vaalish) from Path of Exile 2, read as a Mesoamerican-sourced constructed language: a Yucatec Maya core with Classical Nahuatl, a thin K'iche' seam, and Spanish loans. It reverse-engineers the in-game Vaal texts into attested dictionary roots, documents every reading with primary-source citations, and reports the experimental pass with the intervals the tests actually produced.

Two deliverables: the master document `Vaal_Reconstruction.md` (18 sections) and its typeset PDF `build/The_Vaal_Tongue.pdf`. Start with either; a first-time human reader wants the PDF.

## The method, in brief

Three layers, each tested rather than merely asserted.

- **Lexicon (master §9).** 78 entries. Two survive the project's strictest checks (*xefe*, *Quecholli*; 2.6% [0.7, 8.9]). Most readings are committed hypotheses, not certified. *Ixchel* stays the Godstealer in the lexicon; the strict lookup found a medicinal-herb gloss, so that name is not counted as hardened. Independent translations match or partly match the published English about 29% of the time (method-notes 29.4% [24.2, 35.3]; dictionaries-only 28.2% [23.1, 34.1]; optimistic upper bounds 35.3% / 34.1%). None of the 51 published lines is graded fully secure (working 23.5% [14.0, 36.8]). Chance tests do not currently beat noise once a lookup must recover this project's declared sense. An older "not random noise at 10^-15" claim is withdrawn. Dual-base tables: master §17.7.
- **Syntax (master §3).** The grammar is derived from the corpus's own word order, never importing a source language's grammar. Analysts who did not see this project's English recovered word-order regularities on real lines (3 of 3) and not on scrambled lines (0 of 2). That difference is not statistically significant (Fisher p = 0.10). Possession order is not locked.
- **Phonology (master §2.6, §17.9).** The source-to-Vaal spelling correspondences are collected and hardened as orthographic rules. A phonetic phonology from audio is deliberately out of scope (see the §2.6 scope note).

The full statistics live in master §17 and `analysis/STATISTICAL_SUMMARY.md`.

## Repository structure

```
Vaal Translation/
  Vaal_Reconstruction.md   THE master document (the reconstruction itself). Canonical copy.
  README.md                This file. Human orientation, maintenance, expansion.
  AGENTS.md                Operating rules for AI agents. Read first before any editing.
  PROJECT_MEMORY.md        Running summary of project state across sessions.
  metadata.json            Project metadata.

  analysis/                The method and its evidence
    STATISTICAL_SUMMARY.md          Companion to master §17: tiers, chance-check, translation batteries, distinct-root recount.
    EXPERIMENT_RERUN_PROTOCOL.md    Re-run plan for the chance check, gates, and grammar panel. Older 2026-07 files stay on disk as history.
    NULL_MODEL_PROTOCOL.md          How the decoder's false-positive rate is measured.
    NULL_MODEL_RESULTS.md           Battery A/B/C/D results (the latitude x dictionary-access 2x2), metrics, conclusions.
    HARDENING_PROTOCOL.md           The two-gate test a token must pass to earn Hardened.
    TIGHTENED_LATITUDE.md           The strict phonological ruleset used for the strict battery.
    ADVERSARIAL_RESULTS.md          Blind cross-language competitor search over the committed lexicon.
    EXPERIMENT_LOG.md               Run record for the lexical / statistical experiments; reproduce steps.
    SYNTAX_CONFIRMATION_PROTOCOL.md How the §3 grammar is blind-confirmed and null-controlled.
    SYNTAX_EXPERIMENT_LOG.md        Run record for the syntax confirmation and the negative control.
    REVIEW.md                       The adversarial critique that prompted the statistical work.
    token_classification.csv        Per-token tier and gate outcomes (78 section-9 rows).
    gate1_rescore.csv, RESCORE_OUTPUT.md, NULL_HONESTY_OUTPUT.md  2026-09 recovery scoring proof.
    *.py                            Reproducible tooling (generate pseudo-Vaal, score runs, rescore gates).
    blind_test_*, adversarial_*, strict_committed_*  Raw experiment worksheets and outputs.

  build/                   Turns the master into the typeset PDF
    build_pdf.py           Build script (Markdown to PDF via WeasyPrint).
    BUILD.md               Build instructions.
    The_Vaal_Tongue.pdf    Current typeset PDF (a primary deliverable).
    fonts/, *.svg, *.ttf, *.zip   Fonts and cover-art assets.

  sources/                 Primary-source corpus (what roots are checked against)
    dictionaries/          Cordemex (Yucatec), Christenson (K'iche'), Campbell (Nawat), Molina / INALI, wordlists.
    lore/                  PoE lore dumps used for the narrative anchors.

Downstream copies, kept byte-identical to the canonical and never edited directly:
  ../Vaal_Reconstruction.md          parent-folder copy (often opened here)
  ../Vaal Translation/               a full mirror of this folder
```

## Maintaining the project

- **One canonical master:** `Vaal_Reconstruction.md`. Never edit the copies or the PDF directly; they are generated from the master.
- **Data integrity is the first rule.** Verify the master is complete (18 sections, citations contiguous to 59, clean ending, expected line count, no em dashes or emoji) BEFORE copying it anywhere, propagate one-way only, and verify each copy by reading it back. The full protocol is `AGENTS.md` section 4. This is not theoretical: content has been lost here to a flaky filesystem sync, so the checklist is mandatory.
- **After any content change:** sync the two downstream copies and rebuild the PDF with `python3 build/build_pdf.py` (see `build/BUILD.md`).
- **Formatting rule, no exceptions:** no em dashes, middots, or emojis, in any document.

## Expanding the project

- **A new token.** Resolve it form-first, from its shape and phonology, never from the gloss you expect it to have. Attest the root in a named primary dictionary. Then run it through the two-gate hardening test (`analysis/HARDENING_PROTOCOL.md`) before assigning a tier, and log any competing readings in the master §10 appendix rather than silently choosing.
- **A new corpus line.** Add it to the relevant text section (master §4 to §8). New lines also feed the syntax and phonology, whose confidence intervals tighten as the corpus grows, so more attested Vaal is the single most valuable addition. Audio details caught by ear go straight into the corpus.
- **Promoting a soft token.** Only when it clears the attestation bar. Update the lexicon (§9), the morpheme index (§15), the status (§14), and `PROJECT_MEMORY.md` together.
- **A new citation.** Append to master §18, keep the numbered list contiguous, and personally verify the URL.
- **Extending syntax or phonology.** When the conclusions change, re-run the blind confirmation and negative control (`analysis/SYNTAX_CONFIRMATION_PROTOCOL.md`) with fresh analysts so the confidence figures stay honest.

## Versioning against game patches

The reconstruction is a living hypothesis tied to the game patches it covers: currently *Path of Exile 2* 0.5.0 and *Path of Exile 1* through 3.27 (stated in master §1; full procedure in master §14). When a patch adds Vaal text, audio, or lore:

1. **Snapshot first.** Copy the current master and PDF to a dated, patch-labelled archive before touching anything, so the pre-patch logic is preserved and the change is auditable.
2. **Fold in and re-test.** Add the new corpus, then re-run the null-model battery, the strict-latitude and adversarial gates, and the blind syntax pass. Do not hand-wave new data into the existing rules.
3. **Let it fall where it falls.** If the enlarged corpus breaks a hardened rule, rewrite the rule or the lexicon wholesale, on the same verifiable-data-first basis. The hardened core (§17) is the last thing to move; the starred soft and open parses (§10) are where new data lands first.
4. **Deprecate, do not delete.** A reading a patch overturns moves to the master §10 appendix, tagged with the patch that overturned it, so the record shows why each change was made.

## Who reads what

Humans start with this README and the PDF. AI agents read `AGENTS.md` first for the operating rules. `PROJECT_MEMORY.md` is the running state summary between sessions.
