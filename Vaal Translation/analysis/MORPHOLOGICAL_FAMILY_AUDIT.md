# Morphological family audit (2026-09-16)

Companion to master §17.7 and `STATISTICAL_SUMMARY.md` §7a. This pass collapses morphological relatives, inventories long-form segmentations, and asks per family: one root, or forced lookalikes? Prefer deletion of duplicate independent-count claims over new etymologies. No new H. Dictionaries via `dict_lookup.py` (uploads only, never committed).

## 1. Grouping rule (kept, then sharpened)

Two §9 rows merge when they share the **same attested head root** (the same §9 source lemma), regardless of affixes or compounding partners. Shared affixes (*-ba'*, *-ane*, *-el*) do not merge tokens whose heads differ.

That rule already collapses 16 of 61 battery tokens into 7 families (52 distinct roots). The 78-row table is 69 distinct roots under the same rule (*pul* plus 13 former L-only rows plus three Battery E names as further heads).

**Sharpening (appendix, not a recount).** A shared **piece** that is not the head of both rows is a footnote, not a merge. Counting that piece twice as independent evidence is the thing to delete. Merging the rows would be a new etymology of the second head. Footnote, do not merge.

Sensitivity if *Tzokan'te* were forced into *cha'tsoke*'s *ts'ook* piece: 69 heads become 68, H share 2/68 = 2.9% [0.8, 10.1] instead of 2/69 = 2.9% [0.8, 10.0]. Not adopted. Heads differ (*ka'a* vs *ts'ook*). Headline N stays **52 / 55 / 69**.

## 2. Families already in §17.7 (61-row)

| Head | Tokens | One root or lookalikes? | Gate 1 recovery |
|---|---|---|---|
| *ik'* spirit/breath | *ik'bala, ikba'yucane, Ik'eche, ik'el* | one root. Exact insect lexeme on *ik'el* is a homophone, already C+L* | all fail |
| *aocmo* no more | *Aiokmo, 'Ayok* | one root | all fail |
| *ātl* water | *atla, Atziri* | one root (name vs common noun) | all fail |
| *el* burn | *Ela, elba* | one root | all fail |
| *muk'* strength | *mucane, mujuk'* | one root. Bury (*muk*) is a homophone on *mucane*, already C* | all fail |
| *k'ex* transform | *Kextal, qexcan* | one root plus a Nahuatl locative tail on *qexcan* | all fail |
| *ti' / te'* relational | *te, Ti* | one slot; both C* | both fail |

None of these families is H. Collapsing them still removes no hardened row.

## 3. Candidates inspected and not merged

| Pair | Why it looks related | Verdict |
|---|---|---|
| *tul* decline vs *pul / puul* throw | user-listed; both short *ul* stems; both in Text 5 | **two roots.** Cordemex *tul* "decline" vs *pul/puul* "arrojar". Merging would be a forced lookalike. *jare'yantul* may donate *tul* under LOTO; it may not donate *upulché*. |
| *kux* life vs *k'ux* bite | same letters without the ejective | **two roots.** Glottal contrast is a palette distinction (*qexcan* vs *kuxkal*). Nawat *kuxta* cacao-tree is a competitor on *kuxte'*, not a reason to merge with *k'ux*. |
| *til* kindle vs *el / Ela / elba* burn | same semantic field | **two heads.** Field clustering is §17.7 level 4 (not counted). Do not invent a single burn lemma. |
| *xu'te* (*xul*+*te'*) vs *Tzokan'te* / *cha'tsoke* (*ts'ook*) | all "end" in English | **lookalikes, not one root.** *xul* and *ts'ook* are different Cordemex lemmas. |
| *Ma'oxe* vs *ma* | shared *ma'* | **shared piece, not a merge.** *Ma'oxe* is *ma'* + *xok*. The *ma* row is already a dual bundle (Maya negation / Nahuatl optative), C*. |
| *cha'tsoke* vs *Tzokan'te* | shared *ts'ook* | **shared piece, not a merge.** *cha'tsoke* head in §9 is *ka'a* + *ts'ook*. Footnote *ts'ook* so it is not two independent bets. |
| *Quecholli* vs *Panquetzaliztli* | both veintena maces | **two names, two heads** (*quechōl-* vs the failed *quetza* compound). Onomastic class, not a root family. |
| Spanish *-ada* | *ascensionada / ascenada* | **one row already.** No second *-ada* row to merge. Affix inventory, not a family. |
| *muk'zeh*-class | asked if present | **absent.** The residue class that exists is unexplained *-zeh* on *quxzeh* only, plus non-morphemic tails *-s / -uks* (*Otsuks*, *Gyan'uks*, *Donuks*). Do not mint a *-zeh* suffix. |

§9 rows that are already one lemma (*kux / kuxkal / kuxte'*, *A'te / U'Te / Yatle*, *itsok / itzil*, *tlapec / yotlapek*, *le / le'*, *yax / Yaxe*, *Yutsal / yutsal*) stay one count. No change.

## 4. Long-form segmentation inventory

| Surface | Pieces | Residue | Action |
|---|---|---|---|
| *jare'yantul* | *jare'* (C, K'iche' *are'*) + *yan* + *tul* (C*) | *yan* is not a §9 row. Existential Yucatec *yan* remains a lead, still open (§3.7) | do not mint *yan*. Line 50 is opaque-blocked in the secure-line table because of this hole |
| *ikba'yucane* | *ik'* + *ba'* + *-ane* | leftover **yuc** (three segments the published parse does not spend) | keep in the *ik'* family. Log residue. Do not invent *yuc* = *y-mucane* or a new root |
| *ascensionada / ascenada* | Spanish *ascensión* + *-ada* | none if the Romance parse is granted; Gate 1 still failed recovery | one row, C |
| *upulché* | *u-* + *pul* + *-ché* | *-ché* soft (maybe *che'*) | *pul* stays C*; the tail stays S in §10.7 |
| *le'itzil* | *le'* + *itzil* | none | not a separate §9 row |
| *cha'tsoke* | *ka'a* + *ts'ook* | none under the loose parse | C; shared *ts'ook* footnoted with *Tzokan'te* |
| *ko'janti* | *ko'* + *han-* + *-ti* | relational *-ti* vs inchoative *-ti* is a homophone, already noted | C+L |
| *Ma'oxe* | *ma'* + *xok* | vowel / residual *e* | C+L |
| *ik'bala* | *ik'* + *ba'* | none | C |
| *elba* | *el* + *ba'* | none | C |
| *kifba* | *k'i'ik'* + *ba'* | medial /f/ unexplained | already C+L* |
| *Teoyuxtlane* | *teōtl* + *Yux* + *-tlān* + *-e* | medial *Yux* from *Yutsal* | C; do not split into extra heads |
| *Gyan'uks* | *yancuic* | *-uks* non-morphemic tail | C+L |
| *quxzeh* | *k'ux* | *-zeh* unexplained | C*; not a *muk'zeh* class |

## 5. *ikba'yucane* leftover *yuc*

§9 currently writes *ik'* + *ba'* + *-ane*. The surface is *ik-ba'-yuc-ane* (or *ikba'-yucane*). The honorific/plural *-ane* is the same tail as *mucane*. That leaves *yuc*.

Form-first options that were **not** adopted:

- *y-mucane* with *m* dropped: forcing.
- a new Yucatec *yuc* root: no clean attached-dict head that also keeps the *ik'* family.
- recut as *ikba'yu* + *cane*: no attested *cane* honorific.

Verdict: one *ik'* root, unexplained medial residue, same kind of honesty as *k'ux* + *-zeh*. The family stays four surfaces of one bet. Residue logged in master §10.14. §9 note updated. No new etymology. No distinct-root change.

## 6. Outcome

- Duplicate independent-count claims removed only as **footnotes** (shared *ts'ook*, shared *ma'*, shared *-ba' / -ane*). Rows not merged.
- *tul* / *pul* stay two heads.
- Distinct-root headlines unchanged by this audit: **1/52, 2/55, 2/69** after Ixchel Gate 1 honesty.
- No §9 reading replaced. The only forced segmentation note is leftover *yuc* on *ikba'yucane*.
