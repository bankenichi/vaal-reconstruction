# Sol 56 blockers applied (2026-09-16)

Kenichi scope lock: no published English line text changed; no approved sense rewritten; Ixchel stays Godstealer / theonym in §9 and `committed_readings.csv`; no PDF rebuild; no em dashes, middots, or emojis. Parent `Vaal_Reconstruction.md` kept byte-identical to canonical `Vaal Translation/Vaal_Reconstruction.md`.

## 1. Ixchel Gate 1 honesty

Battery E / `gate1_rescore_rerun.csv` recovered Cordemex *ixchel* with gloss *yerba para curar hinchazones* (medicinal herb). The frozen approved sense is the theonym / Godstealer reading (`committed_readings.csv` committed_gloss: "the Godstealer (a Vaal citizen; later the Trialmaster)"). Herb ≠ that sense. Gate 1 is a recovery miss.

Changes:

- `token_classification.csv`: *Ixchel* `pass,survive,H+L` to `fail,survive,C+L`.
- `gate1_rescore_rerun.csv`: recovery `yes` / `root_lang_sense_match` / `pass` / `H+L` to recovery `no` / `mismatch:sense` / `fail` / `C+L`. Raw Battery E sheets left as decoder history.
- Master §9 row: tier C+L. Gloss column unchanged. Note records the sense miss.
- Master §12.6: still theonym + Godstealer epithet. Carried as C+L, not H+L. Herb is the miss reason, not a replacement gloss.
- H totals: **2 of 78 = 2.6% [0.7, 8.9]** per token; **2 of 69 = 2.9% [0.8, 10.0]** per distinct root. Hardened set: *xefe*, *Quecholli*. Battery frame unchanged (1/61, 1/52). Enlarged: 2/64 = 3.1% [0.9, 10.7]; 2/55 = 3.6% [1.0, 12.3]. Split: H 2 / C* 30 / C 45 / S 1.
- Gate 1 recovery on the 78-row frame: 6/78 (drops *Ixchel*), not 7/78.
- `STATISTICAL_SUMMARY.md`, master §1 / §9 / §12 / §14 / §17, `EXPERIMENT_LOG.md`, `BATTERY_E_RERUN.md`, `ONOMATIC_COMPOUND_PASS.md`, `SECURE_LINE_TAGS.md`, `MORPHOLOGICAL_FAMILY_AUDIT.md`, `PROJECT_MEMORY.md`, `AGENTS.md`, `README.md` updated to the same H set and intervals.

Secure-line working count: **unchanged at 12/51**. *Ixchel* does not occur in the 51 published lines. The only H token in that corpus remains *xefe* (line 35, still fragile because *te'moxti* is S).

## 2. Unsupported confidence language

Removed from master §1 the claim that the statistics show the corpus is "very unlikely" to be pure noise, and the claim that "the committed lexicon is probable."

Replaced with the re-run facts: selection-matched any-C Fisher **p = 0.09494** (trial) / **p = 0.3069** (item); recovery-scored matched **p = 1** / **p = 0.9991**; Gate 1 recovery **6/78**; H **2/78**.

`PROJECT_MEMORY.md` and `AGENTS.md` current-state blurbs aligned to those rates (no leftover 17/78 stopgap as if it were current). `STATISTICAL_SUMMARY.md` headline already used the matched/recovery p-values; H counts there now match the honesty pass.

## 3. Contradictions (Text 5 / Kamasan; opens; overview)

- §8 Kamasan notes no longer say every token is committed, or that the only soft point is syntax. *yan* inside *jare'yantul* is not a §9 row (O). *ek* and *tul* are C*. Published English "Into the dark you come; and so, your waning!" unchanged.
- §14 no longer says the Kamasan line "parses fully on committed roots."
- §14 "Open items are narrow" softened: 30 C* and 45 C / C+L remain. Named holdouts are still listed.
- Overview / status H counts aligned to 2 of 78.

## 4. Stale morpheme index

§15 Status column no longer labels demoted roots as Hardened. Only *quechōl-* (Quecholli) and *jefe / xefe* (xefe) remain Hardened.

Recount by best tier each element reaches: 2 Hardened, 59 Committed, 26 Committed (Competitor), 23 Soft, 37 Lore (147 elements). Previously Hardened heads of demoted §9 rows (including *che'*, *-en*, *ich*, *k'áak'*, *ki'*, *máax*, *náach*, *te' / ti'*, *u-*, *waaj*, *cualli*, *eztli*, *-liztli*, *pan(tli)*, *pilli*, *quetza*, *-ada*, *ascensión*, *chel*, *ix-*) now Committed or Committed (Competitor) to match `token_classification.csv`.

## 5. Tournament C rows (*'Ibil*, *mucane*, *tlayeb*, *kifba*)

No gloss wording changed.

- *'Ibil*: already **C+L*** (Cordemex *IBIL* "sacudir", *EBIL* "escalera" logged in §10.13).
- *mucane*: already **C*** (Yucatec *muk* "sepultar", K'iche' *muq* logged).
- *kifba*: already **C+L*** (medial */f/*; *KIB* wax logged).
- *tlayeb*: stays **C+L**. Ladder is Cordemex *YEB* plus Nah. *tla-*, a cross-graft, not a Gate 2 equal. Logged as a loser in §10.13; not starred.

`gate2_rescore_rerun.csv` not rewritten (same residual limit as the tournament pass).

## Proof

- Published English: all 51 `translation_battery_gold.csv` `gold_en` strings still present in the master; presence vs HEAD unchanged.
- Ixchel gloss in §9 and `committed_readings.csv`: "the Godstealer (a Vaal citizen; later the Trialmaster)" unchanged. `committed_readings.csv` byte-identical to HEAD.
- H count: `token_classification.csv` has 2 H rows (*xefe*, *Quecholli*); master §1 / §9 / §14 / §17 and `STATISTICAL_SUMMARY.md` use 2/78, 2/69, 2/64, 2/55 with the Wilson intervals above.
- Parent copy md5 matches canonical after this pass.
- No PDF rebuild.
