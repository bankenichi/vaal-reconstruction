# Rewrite pass, 2026-09-16

Full in-place pass over the canonical master so it states the completed 2026-09-16 experimental pass. No new experiments. No published English rewrite. No PDF rebuild. Parent `Vaal_Reconstruction.md` kept byte-identical with `Vaal Translation/Vaal_Reconstruction.md`.

## What changed

**Master (`Vaal Translation/Vaal_Reconstruction.md`, then parent copy).**

- **§1 Overview.** Statistical standing now names the whole pass (null, gates, gloss-blind syntax, T-M / T-D, tournaments, particle probes, LOTO, secure-line). Headlines: H 2/78 (*xefe*, *Quecholli*); *Ixchel* C+L; 10^-15 / "probable lexicon" / "very unlikely pure noise" withdrawn; matched null p ≈ 0.095 trial / 0.31 item; recovery-scored matched p = 1; syntax 3/3 vs 0/2, p = 0.10, possession not locked; vs-gold match+partial about 29% both arms; methodology does not lift agreement, cuts clash / raises abstain; secure-line 0% / ~24% / ~75%; LOTO ~24% ok / ~65% ok+partial, T3 weakest. New paragraph splits **transcriptions/corpus documentation (stable)** from **interpretive/translation confidence (thin)**. Companion list added.
- **§3.4 / §3.6 / §3.8.** Possession marked not locked (gloss-blind 1/3 confirm). Sketch notes the panel p. Palette comparison no longer calls the grammar "fixed."
- **§3.7.** Compact verdict table from `PARTICLE_PROBES_3_7.md` (leaning / still open). Bullet text unchanged in substance.
- **§9 confidence key.** Split H 2 / C* 30 / C 45 / S 1. H described as protocol certification, not gloss correctness. *Ixchel* C+L named. Former L-only rows described as gated (mostly Gate 1 fail), not pending.
- **§10.12.** Pointer to §10.13 for same-language false friends already logged (insect, shake, bury, wax, tear-out, ladder).
- **§14 Status.** Opening no longer claims a "measured statistical footing." Project status: texts/transcriptions stable; interpretive/translation confidence thin. Translation-battery, secure-line, and LOTO headlines aligned with §1 / §17.
- **§17.** Intro lists the full pass and current-epoch companions. §17.5 now tables T-M / T-D match and match+partial, clash/abstain, secure-line grades, and LOTO ok / ok+partial / T3. Withdrawn sentence-band prose no longer says the texts run mostly on hardened vocabulary.
- **§4-8 published English, §9 gloss column, approved readings:** not rewritten.

**Companions / pointers (only where they still contradicted, or where the headline was thinner than the master).**

- `STATISTICAL_SUMMARY.md`: headline now carries syntax, translation, secure-line, LOTO, and the corpus-vs-interpretation split; companion list completed.
- `PROJECT_MEMORY.md`: translation-battery / LOTO ok+partial / secure-line shares; "gates pending" on the former L-only 13 corrected (gates are recorded).
- `AGENTS.md` §9: translation / secure-line / LOTO pointers; possession not locked; line-count expectation ~1460.
- `README.md`: dropped "honest confidence intervals rather than assertion" and "why the readings are trustworthy"; syntax bullet now p = 0.10 / possession not locked; lexicon bullet notes ~29% match+partial and 0/51 secure.

## Meaning lock

All 51 `translation_battery_gold.csv` `gold_en` strings remain present in the master (checked before and after). *Ixchel* §9 gloss remains "the Godstealer (a Vaal citizen; later the Trialmaster)". `committed_readings.csv` was not edited.

## Shape lock

Sections §1-§18 still present in that order. Tables, citation system, and heading hierarchy unchanged. No new top-level section. Prose is still the existing academic voice, edited in place.

## Completeness checklist

Run against canonical `Vaal Translation/Vaal_Reconstruction.md` after the last edit, then parent copy.

1. **§1-§18 present.** Yes. File ends on citation 59 (the *Xibaqua* *-aqua* note), not mid-sentence.
2. **Citation list contiguous.** 1 through 59, no gaps. No citation numbers added or removed.
3. **0 em dashes, 0 emoji.** Yes in the files this pass edited (`Vaal_Reconstruction.md` both copies, `STATISTICAL_SUMMARY.md`, `PROJECT_MEMORY.md`, `AGENTS.md`, `README.md`, this file). Endashes and middots also 0 in the master.
4. **Line count not collapsed.** Pre-edit canonical 1443 lines (`wc -l`); post-edit 1463 lines. Grew, not truncated.
5. **Parent md5 == canonical md5.** Yes. `1541e667dcbaf748fc8be412239046ae` on both after the one-way copy.
6. **Headline consistency.** H 2/78, 2/69, 1/61, 1/52, 2/64, 2/55; *Ixchel* C+L; split H 2 / C* 30 / C 45 / S 1; matched p = 0.09494 / 0.3069; recovery-scored p = 1 / 0.9991; syntax 3/3 vs 0/2 p = 0.10; T-M match+partial 29.4%, T-D 28.2%; secure 0/51, working 12/51, fragile 38/51; LOTO ok 12/51, ok+partial 33/51, T3 0/13. Same numbers in overview, §14, §17, `STATISTICAL_SUMMARY.md`, and `token_classification.csv` (2 H rows: *xefe*, *Quecholli*; *Ixchel* C+L).
7. **No leftover Hardened labels on demoted roots in §15.** Only *quechōl-* (Quecholli) and *jefe / xefe* (xefe).
8. **No claim that contradicts `SECURE_LINE_TAGS.md` or `NULL_MODEL_RESULTS_RERUN.md`.** Secure-line 0/51 / 12/51 / 38/51 / 1/51; null matched any-C 0.09494 / 0.3069 and recovery-scored 1 / 0.9991. The withdrawn 10^-15 headline is labelled withdrawn.

No PDF rebuild.
