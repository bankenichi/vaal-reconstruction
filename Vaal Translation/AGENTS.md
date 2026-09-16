# AGENTS.md

Operating instructions for any AI agent working in this repository. Read this file in full before touching any document. If a request conflicts with the rules here, stop and ask the user (Kenichi) rather than proceeding.

## 1. What this project is

A rigorous academic reconstruction of the "Vaal language" (Vaalish) from Path of Exile 2, read as a Mesoamerican-sourced constructed language. The work reverse-engineers the in-game Vaal texts into attested dictionary roots and documents every reading with primary-source citations.

The deliverable is a single master document, `Vaal_Reconstruction.md`, supported by a corpus of source dictionaries and lore references. This is scholarship, not fan fiction. The standard of proof is closer to historical linguistics than to worldbuilding.

## 2. Source palette (search order)

Every token is resolved by searching candidate languages in this fixed priority:

1. Yucatec Maya (core layer, most content roots, articles, presentatives)
2. Classical Nahuatl (divinity, place-names, negation, several adjectives)
3. Highland Maya, K'iche' (thin seam, surfaces only where the first two cannot account for a sound, e.g. the /r/ in *jare*)
4. Romance, Spanish (loans for abstract and martial concepts)
5. Xinkan and Nahuan (Pipil/Nawat) as secondary candidate pools and geographic corroboration

## 3. Hard rules (non-negotiable)

1. **No em dashes, no middots, no emojis.** Anywhere. In documents and in chat replies. Use commas, colons, parentheses, or regular hyphens instead. This is a strict formatting rule with zero exceptions.
2. **Anti-forcing discipline.** Opaque tokens are reported as opaque. Never propose an etymology without an attested primary-source root that matches both form and semantics. "Squinting until it fits" is prohibited.
2a. **Root search is form-first; never gloss-led.** Do NOT search for roots based on the translation a token already has. Start from the surface form and its phonology, enumerate every attested root that fits the form, then read off what those roots mean and follow where the best-attested, sensical ones lead, even if that overturns the current gloss. Searching a dictionary for words that mean what we already think the token means is reverse-engineering our own answer and is forbidden. (Distinct from rule 6: constraining plausibility with *neighboring attested tokens* is allowed; constraining it with the token's own prior translation is not.)
2b. **Confidence taxonomy and hardening.** Tiers are: **H** hardened (top), **C** committed but latitude-dependent, **S** soft candidate (appendix §10, or S+L in §9 when a lore-tagged row still has an unresolved step), **O** opaque; **L** lore-anchored is an orthogonal tag (H+L, C+L, S+L), never a lone tier, and a star (C\*) flags a logged competitor (same-language homophones included). A token earns **H** only by passing BOTH gates of the lexicon hardening protocol (`analysis/HARDENING_PROTOCOL.md`) under **recovery scoring**: Gate 1 must match the predeclared root, language class, and sense, not any dictionary hit. No token may carry `H` without both gates recorded. Cite the protocol in the token's entry. Empirical basis: master §17, `analysis/STATISTICAL_SUMMARY.md`, `analysis/RESCORE_OUTPUT.md`.
3. **Primary-source attestation required for commitment.** A root may only be promoted to the committed lexicon if it is attested in a named primary dictionary (Cordemex, Karttunen, Molina, Florentine Codex, etc.) with explicit phonology.
4. **Competing readings are logged, not discarded.** When multiple candidates exist, track all of them with explicit reasoning in the appendix (section 10). Do not silently pick a winner.
5. **Distinguish romanization artifacts from morphology.** Scribal or spelling conventions (for example the "-uks" coda) are not productive morphemes. Verify before treating a pattern as grammar.
6. **Semantic field constrains the search.** Use surrounding attested tokens to bound the search before phonology (for example *Ela* "burns" in Text 4 ruled out "drink" glosses for *ukto*).
7. **All bibliographic URLs must be personally verifiable.** Do not invent or approximate citations. Do not fabricate lore.

## 4. Working conventions

- **Present-first, approve-then-edit.** Show every analytical proposal to Kenichi for approval before committing it to the master document. Do not edit committed entries unilaterally.
- **File delivery every turn.** After any change, the updated master document is delivered as a file.
- **DATA-INTEGRITY PROTOCOL (mandatory, non-negotiable). Data loss is unacceptable. Follow this exact order on every turn that changes the master.**
  1. **Designate ONE canonical master:** `Vaal Translation/Vaal_Reconstruction.md`. The one genuinely separate on-disk copy is the parent-folder `Vaal Reconstruction/Vaal_Reconstruction.md`; keep it in sync with a direct write, never a bash copy. The `Vaal Reconstruction/Vaal Translation/` path is the SAME physical folder as the canonical (item 8), not a separate copy. The PDF is a generated downstream artifact. None of these is ever edited directly.
  2. **Verify the canonical is COMPLETE before it is used as a copy source.** Run the completeness checklist: (a) sections §1 through §18 all present; (b) citation list is contiguous with no gaps and reaches the expected maximum (currently 59); (c) the file ends cleanly on the last citation, not mid-word or mid-sentence; (d) line count is within expectation (currently ~1390) and not suddenly smaller; (e) 0 em dashes, 0 emoji. If ANY check fails, STOP and repair before copying. A truncated or shrunken master must never be propagated.
  3. **Propagate one-way only, canonical -> downstream.** Never copy a downstream file back over the canonical. Never overwrite a known-good copy with an unverified one.
  4. **Verify every destination after writing** by reading it back (copy the written file to local storage and compare md5 and citation count against the canonical). Only report success when all copies match.
  5. **The sandbox `/tmp` is ephemeral and is never the only copy of anything.** Persist to the mounted canonical immediately; treat `/tmp` as scratch that can vanish between turns.
  6. **The mount's bash read cache can lie (it has returned zero-length and truncated views of intact files, and has zeroed a file during sync).** Never trust a single `wc`/`md5sum`/`cp` on a mount path; always verify by copy-back to local `/tmp` and by the completeness checklist. Writes do land; stale *reads* are the hazard, so never use a mount read as the SOURCE of a copy without verifying it is non-empty and complete first.
  7. **Propagate an edit by re-applying the same Edit to the mirror, never by copying the whole file.** The real backup is the separate folder `Vaal Reconstruction/Vaal Translation Mirror/` (created 2026-07; distinct from the same-inode `Vaal Reconstruction/Vaal Translation/` alias, which is not a copy). When you change a file, apply the identical targeted diff through the direct Edit tool to the file in BOTH the canonical `Vaal Translation/` and the mirror. The Edit tool uses the real files (never bash) and applies only if the target text matches, so the match is the verification; the cost is the size of the change, not the file. Never read-then-write a whole file to propagate, and never use bash to propagate an edit (bash reads a stale, truncated view and has zeroed files here, including `ADVERSARIAL_RESULTS.md`, recovered from backup).
  8. **New, binary, and bulk/static files may be moved with a whole-file copy (bash is acceptable for this).** A copy into the mirror only writes the destination and cannot corrupt an existing good file, so it is safe for brand-new files and for the binaries and large static sources (fonts, PDFs, the built PDF, the zip, the multi-MB dictionaries). Confirm the destination afterward with a single direct Read, not a bash read.
  9. **Never trust a bash read as verification;** it lies (zero-length, truncated, stale). Verify only through the direct Read tool. External last-resort recovery is the user's Proton Drive versioning.
  10. **Byte-identity check after every iteration (mandatory).** After each editing turn, before building the PDF, confirm all three masters (canonical `Vaal Translation/`, parent `Vaal Reconstruction/`, mirror `Vaal Translation Mirror/`) are byte-identical. Run `md5sum` on all three and `diff` the canonical against each other copy. All three md5s matching means identical. A `diff` difference that appears ONLY at the end of the file, where one side is cut mid-line or mid-word with `\ No newline at end of file`, is a mount-read truncation artifact, not a real divergence: confirm that copy's true tail with the direct Read tool (it must end on the last citation, currently 59 / the *Xibaqua* *-aqua* etymology note). A `diff` difference in the body, with matching context around an added or removed block, is a REAL divergence (this is how the mirror silently lost the §17.7 enlarged-base subsection on 2026-07-13, while its md5 mismatch was the only warning): re-apply the missing content to that copy from the canonical with the Edit tool, then re-check. Do not build the PDF or hand off until all three reconcile. The failure mode that matters is a mid-document add or delete that lands in one copy but not the others, so this check runs every turn, not just when something looks wrong.
  - Background: apparent "lost edits" and one real citation-truncation (citations 47-53 lost, recovered from the user's Proton Drive versioned backup) both traced to propagating an unverified/partial copy. This protocol exists to make that impossible.
- **The PDF is a primary deliverable, not a byproduct.** `build/The_Vaal_Tongue.pdf` must be kept current with the master document. Rebuild it (via `build/build_pdf.py`) at least every few turns, and always before handing off or at the end of a working session, so the PDF never lags the markdown by more than a few edits.
- **In-game audio and screenshots are primary data.** Treat them as valid phonological evidence for disambiguating vowels and onsets (for example the silent /g/ in *Gyan'uks*, the /o/ realization of written *u*).
- **When a token is unresolved, say so plainly** and move it to the open-questions appendix rather than forcing a reading.

## 5. Established diagnostics (apply these)

- **Word-initial *Gua-/Gue-*** in the corpus signals Nahuatl *cua-/cui-* /kʷ/, following Spanish colonial orthography (as in *Cuauhtemoc > Guatemoc*).
- **Word-initial or loan-only /d/, /f/, /r/, /g/** flag a non-core source: /r/ points to K'iche', /f/ and /d/ to Spanish loans, silent /g/ to Nahuatl.
- **Variant NPC names are a game mechanic, not lore drift** (Quemalani/Xolotl; Tizoc/Cotan/Axilo; the Drill Sergeant set). Do not treat randomized names as inconsistencies.

## 6. Master document structure (`Vaal_Reconstruction.md`)

Section map, so edits land in the right place:

- 1 Overview
- 2 Linguistic framework (2.1 standard, 2.2 source palette, 2.3 phoneme inventories, 2.4 diagnostic key, 2.5 lore-anchor summary)
- 3 Vaal-internal syntax and grammar (3.1 method/isolation, 3.2 corpus, 3.3 clause types, 3.4 word order, 3.5 morphology, 3.6 sketch, 3.7 open questions). Analysed in isolation: grammar is read from Vaal's own distribution, never imported from the palette.
- 4 Text 1: The Atziri Chant (closed)
- 5 Text 2: The Cuachic Vault Litany (closed)
- 6 Text 3: Quemalani, the Elite Commander
- 7 Text 4: The Drill Sergeant and the Vaal Regiment
- 8 Text 5: Stray captures
- 9 Combined lexicon (committed tokens only)
- 10 Appendix: recorded alternates and open questions (soft tokens live here until promoted)
- 11 Lore anchors
- 12 Vaal and Vaal-related figures
- 13 Method notes
- 14 Status
- 15 Morpheme index
- 16 Contributors and acknowledgments
- 17 Statistical analysis and lexicon hardening (methodology, metrics + formulas, null-model results, hardened tier, distinct-root recount; syntax stats added here too)
- 18 Citations (final section)

Rule of thumb: committed readings go in section 9 and section 15; anything soft, contested, or unresolved stays in section 10 until it clears the attestation bar. Tiers (H/C/S) are set by the hardening protocol (§2b).

## 7. Repository layout

```
Vaal Translation/
  Vaal_Reconstruction.md     THE master document. Single authoritative copy.
  AGENTS.md                  This file. AI agent operating instructions.
  PROJECT_MEMORY.md          Carried-over running summary of prior sessions.
  metadata.json              Project metadata.
  sources/
    dictionaries/            Lexical sources (the root-checking corpus)
      Cordemex_MayaEsp_FULL.pdf     Full text-layer Cordemex (primary Yucatec). Authoritative.
      Cordemex_FULL.txt             Extracted text of the above (greppable, 257k lines).
      Cordemex_scan.pdf             Image-scan Cordemex (backup; no text layer).
      norma_maya.pdf / .md          INALI Maya orthography standard.
      ilide_SpanMaya.pdf / .md      Modern Spanish->Maya wordlist.
      Nahuatl_1100_MyLittleWordLand.md   Nahuatl wordlist cross-reference.
      Maya_Dictionary_Sources.md    Sourcing catalog (direct PDF links to more dictionaries).
      kiche_christenson_FULL.pdf / .txt  Christenson K'iche'-English dictionary (full).
      kiche_christenson_PARTIAL.txt, kiche_ENG-KICHE_reversal_taterenner_PARTIAL.txt
    lore/
      POE 3.27 & POE II 0.4.pdf / .md     PoE lore dump.
      POE ... supplement - Atlas of Worlds.pdf, ... - Heist.pdf
  analysis/                  Meta-work on the method itself
    REVIEW.md                Adversarial critique of the project.
    HARDENING_PROTOCOL.md    The two-gate test each token must pass to earn H. Cite it per token.
    NULL_MODEL_PROTOCOL.md   How to measure the decoder's false-positive rate.
    NULL_MODEL_RESULTS.md    Batteries A/B/C results, metrics, conclusions.
    ADVERSARIAL_RESULTS.md   Adversarial survival of the committed lexicon.
    EXPERIMENT_LOG.md        Concise evidence-based run record; reproduce/resume instructions.
    EXPERIMENT_RERUN_PROTOCOL.md  True remediation (Batteries A-E). The 2026-09 rescore is a STOPGAP.
    TIGHTENED_LATITUDE.md    The strict ruleset used for Battery C and Gate 1.
    STATISTICAL_SUMMARY.md   Companion to master §17: tier tables, PPV, base rate, distinct-root recount.
    token_classification.csv Per-token tier (H / C* / C) with gate outcomes.
    generate_pseudo_vaal.py / gen_set.py / score.py / score_adversarial.py  (reproducible tooling)
    pseudo_vaal_test_set.txt, blind_test_worksheet*.csv, blind_test_key*.csv, *_results_*.csv
  build/                     PDF pipeline for the deliverable
    build_pdf.py             Build script.
    BUILD.md                 Build instructions.
    The_Vaal_Tongue.pdf      Current exported PDF of the reconstruction.
    Cardo-*.ttf, Cinzel-*.ttf, *.svg, Vaal_PDF_build_assets.zip   Fonts and assets.
```

Edit the canonical master (`Vaal Translation/Vaal_Reconstruction.md`), then sync it over the parent-folder copy and the full mirror at the end of the turn (see the DATA-INTEGRITY PROTOCOL in §4). Rebuild `build/The_Vaal_Tongue.pdf` from it at least every few turns. Search the dictionaries by grepping the `.txt` extracts under `sources/dictionaries/`; the full Cordemex is `Cordemex_FULL.txt`.

Campbell, *The Pipil Language of El Salvador* (Nawat), is in `sources/dictionaries/` as `nawat_Campbell_Pipil_1985_FULL.pdf` / `.txt`. **Optional, not yet acquired:** Yucatec cross-checks (Bolles combined, Hofling Itzaj and Mopan) and Kaufman's comparative Mayan dictionary; direct links in `Maya_Dictionary_Sources.md`. These are non-essential now that the full text-layer Cordemex is in place.

## 8. Primary sources

- Diccionario Maya Cordemex (Yucatec, primary)
- Karttunen, An Analytical Dictionary of Nahuatl (Nahuatl, primary)
- Molina, Vocabulario en lengua castellana y mexicana
- Florentine Codex (Wired Humanities digital edition)
- Belize Yucatec heritage word-list (Andy Chuc / NICH Institute of Archaeology)
- PoE2 in-game audio and screenshots (primary phonological data)

## 9. Current state (update this as work progresses)

- Master document: 18 sections, roughly 147 morpheme index elements; 59 citations.
- Texts 1 and 2: closed and source-validated against game files.
- Texts 3, 4, 5: documented, with soft tokens tracked in section 10, not yet promoted.
- Statistical hardening (§17): 78 section-9 rows with H/C/S/O (L is a tag). Stopgap hardened share 17/78 = 21.8% [14.1, 32.2] per token (17/69 distinct roots); battery 14/61 / 14/52; provisional Battery E third base 17/64 / 17/55. The 2 x 10^-15 all-noise headline is withdrawn as a headline; stopgap matched range p about 0.005 to 0.06 (marginal). True remediation is the re-run in `analysis/EXPERIMENT_RERUN_PROTOCOL.md`. Companion: `analysis/STATISTICAL_SUMMARY.md`, `analysis/RESCORE_OUTPUT.md`.
- Syntax and grammar (§3): derived in isolation from the corpus. Gloss-blind re-run (2026-09-16): 3/3 vs 0/2 recovered word-order regularities, Fisher p = 0.10, not significant. Qualitative match to the six §3 conclusions is weaker without English. Historical 2026-07 3/3 vs 0/2 p = 0.10 is not gloss-blind. Protocol/log: `SYNTAX_CONFIRMATION_PROTOCOL.md`, `SYNTAX_EXPERIMENT_LOG_RERUN.md`.
- Phonology: correspondence/stylization rules collected in §2.6 and hardened orthographically in §17.9; a phonetic (audio-based) phonology is deliberately out of scope (§2.6 scope note).
- Known open items: the *o-...-s* wrapping around *tsuk* in *Otsuks*; the exact K'iche' lemma behind *jare'*; *fukuur* phonetic fit; *ta'* (leaning relational *ti'*, not closed); *ukto* in the Text 4 catechism (leading reading Nahuatl *ocotl* "pine torch," soft). Particle probes: *le le* doubling and *-yan-* still open; *ka ti*, presentative slot, and *ta'* leaning (`analysis/PARTICLE_PROBES_3_7.md`).

When you close an open item or promote a token, update section 14 (Status) of the master and this section together.

## Imported Claude Cowork project instructions
