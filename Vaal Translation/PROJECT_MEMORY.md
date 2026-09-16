# Project memory (running summary)

Carried-over summary of the Vaal Translation project state. Update as work progresses. For operating rules see `AGENTS.md`; for the statistics see master §17 and `analysis/STATISTICAL_SUMMARY.md`.

## Purpose and context

Kenichi is producing a rigorous academic reconstruction of the "Vaal language" (Vaalish) from Path of Exile 2, read as a Mesoamerican-sourced constructed language. The core layer is Yucatec Maya, with Classical Nahuatl (divinity, place-names), K'iche' (a thin /r/ seam), Spanish loans, and Xinkan and Nawat/Pipil as secondary candidate pools. Standards are historical-linguistic: every committed root is attested in a named primary dictionary with explicit phonology, competing readings are logged not discarded, forced etymologies are prohibited (form-first, never gloss-led), and no lore is fabricated. Hard formatting rule across all documents and chat: no em dashes, middots, or emojis.

## Files and where they live

- Canonical master: `Vaal Translation/Vaal_Reconstruction.md`. Two downstream copies kept byte-identical: the parent `Vaal Reconstruction/Vaal_Reconstruction.md` and the full mirror `Vaal Reconstruction/Vaal Translation/Vaal_Reconstruction.md`. PDF: `build/The_Vaal_Tongue.pdf` (built by `build/build_pdf.py`), propagated to all three build locations.
- Companions in `analysis/`: STATISTICAL_SUMMARY, EXPERIMENT_LOG, NULL_MODEL_PROTOCOL/RESULTS, ADVERSARIAL_RESULTS, HARDENING_PROTOCOL, TIGHTENED_LATITUDE, SYNTAX_CONFIRMATION_PROTOCOL, SYNTAX_EXPERIMENT_LOG, REVIEW, token_classification.csv, and the reproducible tooling.

## Data-integrity protocol (mandatory, learned the hard way)

Data loss is unacceptable. The FUSE mount's read cache has returned zero-length and truncated views of intact files, and once zeroed a file during sync; the sandbox `/tmp` is wiped between sessions. So: designate the one canonical master, verify it is COMPLETE against the checklist (sections 1-18 present, citations contiguous to 59, ends cleanly, line count not shrunken, zero em dashes/emoji) BEFORE using it as a copy source, propagate one-way only (canonical to downstream, never back), and verify every destination by copy-back to local `/tmp`. Full rule in `AGENTS.md` section 4. Citations 47-53 were once lost this way and recovered from Kenichi's Proton Drive versioned backup.

## Current state

- Master: 18 sections, roughly 147 morpheme-index elements, 59 citations. Two synced copies plus mirror plus a current PDF.
- Committed lexicon (§9): 62 tokens, tiered by the hardening taxonomy H / C / C\* / S / L. Distribution 22 Hardened, 7 committed-with-competitor (C\*), 33 committed latitude-dependent (C). Over 53 distinct roots (morphological relatives collapsed) the split is 22 H / 6 C\* / 25 C. Three onomastic names added after the battery (Quecholli, Panquetzaliztli, Ixchel) were then blind-certified as plants by Battery E (§17.7, 15/15 Gate-1), so the enlarged base (65 tokens / 25 hardened = 38.5%; 56 roots = 44.6%; 26 strict passes, p ≈ 3 x 10^-18) is now the headline; the original 62 / 22 run (Batteries A-D) is retained as the prior epoch; a full re-run of the battery is the versioning trigger (§14).
- Statistical hardening (§17, companion `STATISTICAL_SUMMARY.md`): the null model rejects the all-noise hypothesis (23 of 62 strict-reconstruct vs ~3 expected at the Battery D strict-and-online 4.6% noise floor, p about 2 x 10^-15; 22 of 53 distinct roots, p about 4 x 10^-16). Hardened core 35.5% [24.7, 47.9] per token, 41.5% [29.3, 54.9] per distinct root. Per-reading PPV depends on the base rate b, estimated at about 58% from the name roster (§17.6); using the Battery D strict-and-online rates (the resources the real decode uses) hardened readings then sit around 75 to 81%. Adversarial pass logs 7 competitors (strongest itsok vs Nahuatl itztli).
- Syntax and grammar (§3): derived in isolation from the corpus (never importing palette grammar), blind-confirmed by 3 fresh analysts (18/18, Wilson [82.4, 100]) with a scrambled-corpus negative control that recovered the word-order rules 12/12 real vs 0/8 scrambled (Fisher p about 7.9 x 10^-6), §17.8. Findings: clause type set by a clause-initial particle; article/possessive/modifier prenominal; possessed before possessor; verb before object; no copula; proclitic operators, suffixed derivation. Palette comparison is a closing note (§3.8): the grammar matches the Mayan profile, diverges from Spanish, and Nahuatl's heavy verbal prefixation does not reach it.
- Phonology (§2.6, §17.9): correspondence/stylization rules collected in one place and hardened orthographically (strict-safe rules vs permissive; 23/62 derive with strict-safe rules only, = the Gate 1 set). A phonetic phonology needs trained audio transcription and is deliberately out of scope; audio details caught by ear are added to the corpus (as /o/ and silent-g already were), otherwise the line is drawn there.
- Texts 1 and 2 closed and source-validated; Texts 3, 4, 5 documented with soft tokens in the §10 appendix.

## Open items (tracked, not forced)

The o-...-s wrapping around tsuk in Otsuks; the exact K'iche' lemma behind jare'; fukuur's phonetic fit; ta' (ti' vs taak); ukto (leading reading Nahuatl ocotl "pine torch," soft); and from the syntax pass the particles ka and ti, and the le le doubling.

## Out of scope

A phonetic (audio-based) phonology. Anyone with the specialist skills is welcome to take it up; §17.9 is the ceiling this project sets for phonology.

## Key principles

Anti-forcing (opaque stays opaque); form-first, never gloss-led (applies to roots and to syntax); competing readings logged; semantic field constrains the search; romanization artifacts are distinguished from morphology; living-Maya and Nawat sources corroborate; variant NPC names are a game mechanic, not lore drift; present-first, approve-then-edit; the PDF and all copies are kept current every editing turn under the data-integrity protocol.
