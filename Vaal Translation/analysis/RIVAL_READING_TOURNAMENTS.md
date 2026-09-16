# Rival-reading tournaments (post T-M / T-D)

Date: 2026-09-16. Trigger: `TRANSLATION_BATTERY_RESULTS.md` clash hotspots. This file is **not** a new null-model battery, not a PPV, and not a Gate 1 re-score of `gate2_rescore_rerun.csv`. It is a form-first contest among attested dictionary roots for the tokens that carried the 16 lines that were 5/5 clash in both T-M and T-D, plus the highest-clash content words, plus line 9 as the methodology worked example.

Gold English was used only to name load-bearing tokens and to identify which battery glosses clashed. It was not used as a search key (AGENTS rule 2a). Neighbor tokens in the same line, and the same token's other attestations, were allowed as semantic-field constraints (rule 6).

Dictionaries: attached extracts via `dict_lookup.py` (`VAAL_DICT_DIR`, hashed uploads). Never committed.

Supporting table: `rival_tournament_brackets.csv`.

## 1. Protocol

For each token:

1. Freeze 2-4 competing attested roots. Include the current §9 reading and any battery false friend that is a real dictionary hit.
2. Score each rival on five axes, independently of the published English gloss:
   - **Form fit:** exact folded match, same-language affix covering the surface, licensed loose leftover, or unexplained residue / cross-graft / metathesis.
   - **Residue:** none, licensed coda, or unexplained segments.
   - **Sense in this line and other attestations:** does the rival make a coherent claim in every line the token appears, not just one.
   - **Morphology consistency:** same root, same job, across related surfaces (`ik'el` / `ik'bala` / `Ik'eche`; `kux` / `kuxkal` / `kuxte'`; `mujuk'` / `mucane`).
   - **Neighbor field:** surrounding attested tokens bound the search (rule 6).
3. Declare one of: **winner** (keep current, or replace if form-first plus field overturns it), **keep-as-C\*** (committed reading stands, competitor logged), **demote-to-S**, or **opaque**.
4. Log losers in master §10. Do not silently delete. Do not invent **H** (both gates under recovery scoring are still required: `HARDENING_PROTOCOL.md`).
5. Update `token_classification.csv` and §9 notes only when the outcome is clear.

Anti-forcing: a miss is a miss. Exact Cordemex / ilide / Campbell hits that lose on field or morphology stay in §10. They are not erased because they spoiled a translation battery.

## 2. The 16 dual 5/5-clash lines: load-bearing tokens

Particles and unchanged names excluded from the load-bearing list (same exclusion as the translation-battery token rate): `a'te`, `u'te`, `le`, `le'`, `ti`, `ti'`, `ka`, `ta'`, `u`, `ma`, `ma'`, `na'`, `en`, `Atziri`, `Zerphi`, `Vaal`.

| Line | Surface (short) | Load-bearing content | Why the line clashed |
|---|---|---|---|
| 3 | *ma kilya Zerphi* | *kilya* | no whole-form hit; *kil* leftover; *quil-ya* not in attached dicts |
| 6 | *A'te 'Ibil tlayeb kutsen! A'te ik'el tlayeb kifba!* | *'Ibil, tlayeb, kutsen, ik'el, kifba* | shake / insect / turkey / ladder salad |
| 10 | *Tlaxye' le Vaal* | *Tlaxye'* | no whole-form hit |
| 11 | *Ma'oxe ik'el* | *Ma'oxe, ik'el* | *ik'el* insect/breath; *Ma'oxe* opaque to lookup |
| 15 | *A'te 'Ibil* | *'Ibil* | exact Cordemex *IBIL* "sacudir" |
| 16 | *A'te ik'el* | *ik'el* | exact ilide *ik'el* insect/virus |
| 18 | *Tzokan'te ik'el* | *Tzokan'te, ik'el* | *TSOK* tear-out vs *ts'ook* end; *ik'el* as above |
| 21 | *Tlayeb kutsen* | *tlayeb, kutsen* | ladder + turkey |
| 24 | *A'te yuquia* | *yuquia* | K'iche' *yuq* "stretch" leftover *-ia*; *yocoya* not in attached dicts |
| 27 | *'Ayok ta' en, u mujuk' le mucane, niáach i'chian* | *mujuk', mucane, niáach, i'chian* | specter / buried / far / house pieces |
| 36 | *Na' puyao* | *puyao* | already soft; no whole-form hit |
| 37 | *Ich tlapec u'te puyao, a'te itsok pu uch' ta'nuk* | *tlapec, puyao, itsok, uch', ta'nuk* | altar / crush / drink / great-one all latitude-heavy |
| 38 | *Otsuks! Tzokan'te u'te ik'el* | *Otsuks, Tzokan'te, ik'el* | *Otsuks* not in §9; *ik'el* as above |
| 43 | *U'te mucane* | *mucane* | buried vs mighty |
| 45 | *U'te mucane* | *mucane* | same |
| 49 | *Axba!? Kíibsa' ta' en* | *Axba, Kíibsa'* | both already soft in §10.9; metathesis / *m→b* |

Shared misses, not a methodology split. T-M and T-D independently walked into the same Cordemex / ilide exact hits.

## 3. Worked example: line 9 (*Kuxte' kíimil'*) is not a 5/5 clash

This line is the largest T-M vs T-D split (T-M 5/5 match "life and death"; T-D 5/5 clash "cacao-tree + death"). It is included because RESULTS called it out as the methodology effect, and because *kux / kuxkal / kuxte'* is a high-traffic C+L* family that also feeds clash line 40 (*Kuxkal*).

**Rivals frozen**

| ID | Root | Lang | Gloss | Source | How it hits *kuxte'* |
|---|---|---|---|---|---|
| A | *kux / kuxtal* | Yucatec | life, living, to live; soul | Cordemex *KUX* "vida", *KUXTAL* "vivo, viviente"; ilide *kuxtal* "vida" | *kux* + *-te'* (relational / tree), or *kuxtal* with *al* vs *e'* leftover |
| B | *kuxta* | Nawat | tree resembling cacao; also gunny-sack | Campbell *kuxta* "cuxta (arbol parecido al cacao)" | exact stem; leftover glottal on *kuxte'* |
| C | *kux* + *te'* as "life-tree" | Yucatec pieces | living tree | composition of A with *te'* "tree" | exact two Maya pieces; sense is a tree, not "life" as a merism partner |

**Scores**

- Form: B is the cleanest single lemma (*kuxta*). A needs a leftover (*-tal* vs *-te'*) or a two-piece parse. C is legal Maya composition.
- Residue: B leftover `'`; A leftover *al* or a segmentable *-te'*; C none if *kux+te'* is accepted.
- Line 9 neighbors: *kíimil'* is exact Yucatec "death / the dead" (ilide *morir, muerte, deceso*). A merism "life and death" is a pair of the same grammatical class. "Cacao-tree and death" is a possible pairing but not a merism.
- Other attestations: *kuxkal* (line 23 *U'Te kuxkal*, line 40 *A'te Kuxkal*) has no cacao reading. Cordemex *KUX* "cosa viva" plus *kal* leftover is the same life family. A cacao-tree reading of *kuxte'* would split the family.
- Morphology: bundling *kux / kuxkal / kuxte'* as one life lemma is consistent if *-kal* and *-te'* are tails. It is inconsistent if only *kuxte'* is Nawat *kuxta*.
- Palette order (T-M only): Yucatec before Nawat. That is why T-M took A and T-D took B. The field, not the gold English, is what makes A win once both are on the table.

**Verdict: winner A (*kux / kuxtal* "life").** Keep **C+L\*** (already starred: Nawat *kuxta* is a real Gate-2 competitor). Do not promote to H. Loser B logged in §10.13. Loser C ("life-tree") is a same-language composition that explains the surface better than *kuxtal* as a single lexeme, but it loses the merism and the *kuxkal* family unless "life-tree" is stretched to mean "life." Logged, not adopted.

This is the case where methodology changes decoder behavior in a way that also tracks the better field reading. It does **not** raise vs-gold match+partial on the 16 dual-clash lines, which never saw this split.

## 4. Priority tokens (RESULTS highest-clash)

### 4.1 *ik'el*

Current §9: Maya *ik'* + *-el* "the spirit, the unseen" (**C+L**). Attestations: lines 6, 11, 16, 18, 38 (and the *ik'* family: *ik'bala, ikba'yucane, Ik'eche*).

**Rivals**

| ID | Root | Lang | Gloss | Source | Form |
|---|---|---|---|---|---|
| A | *ik'* + *-el* | Yucatec | wind / breath / spirit, abstractive *-el* | Cordemex *IK'* "aire"; *IK'IL* "aereo"; *IK'AL* "respirar" | composition; *-el* is an attested Maya suffix |
| B | *ik'el* | Yucatec | insect, moth, weevil, microbe, virus | ilide *ik’el* "bicho, insecto, microbio, polilla, virus"; Cordemex *IK'EL* "bicho, polilla, insecto, gorgojo" | **exact lexeme** |
| C | *ik’il* | K'iche' | month; menstruation | Christenson *ik’il* | exact fold (*i* vs *e* under glottal fold); different language |
| D | *IK'AL* | Yucatec | to breathe; rough sea | Cordemex | vowel *a* vs *e* |

Battery clash is B (and D as "breath"). B is not a hallucinated false friend. It is the best whole-form hit in the attached Maya lists.

**Scores**

- Form: B wins (exact). A is compositional. D is a near-vowel. C is K'iche' and a different vowel.
- Residue: B none. A none if *-el* is granted. D *a/e*. C language plus vowel.
- Line sense: B yields "behold the insect," "the countless insects," "the last insect." Grammatical, thematically odd in a presentative couplet with *'Ibil* and in a drill call *Tzokan'te u'te ik'el*.
- Morphology: the corpus has an *ik'-* family with *ba'*, *-ane*, *-ech*. Those suffixes attach to *ik'* "wind/spirit/breath," not to a frozen insect lexeme. If *ik'el* were only B, the family would be four unrelated insect-adjacent coins. A keeps one root.
- Neighbor field: line 6 pairs *'Ibil* with *ik'el* in the same presentative frame. Line 11 *Ma'oxe ik'el* sits in the litany after *Tlaxye' le Vaal*. A spirit/breath reading participates in that field. An insect reading does not, unless the whole litany is recast as entomology, which no neighboring committed token supports.

**Verdict: keep A, star it (C+L\*).** Exact insect *ik'el* is a live same-language homophone. It lost the tournament on morphology plus neighbor field, not on "it is not in the dictionary." Log B (and C, D) in §10.13. Do not promote to H. Do not demote to S: the *ik'* family is recurrent. Breath (D) is the same root as A with a different vowel; it is corroboration of *ik'*, not a different lemma.

`token_classification.csv` previously had Gate 2 survive because `gate2_rescore_rerun.csv` did not write the insect row. The tournament writes it. Tier moves C+L to **C+L\***. The rerun Gate-2 CSV is not rewritten (residual limit: do not invent rows in an archived sheet).

### 4.2 *kutsen*

Current §9: Maya *kutz* "sacrificial bird" → "the offering" (**C+L\***). Attestations: lines 6, 21, 40.

**Rivals**

| ID | Root | Lang | Gloss | Source | Form |
|---|---|---|---|---|---|
| A | *kuts / kutz* turkey, the native turkey | Yucatec | pavo de esta tierra | Cordemex *KUTS* "pavo" | *kuts* + Maya *-en*; affix coverage |
| B | *kuts* "acepillar / desflecar" | Yucatec | to brush, clean with a cloth, fray | Cordemex *KUTS* "acepillar" | same form as A (homophone) |
| C | *-kuts* | Nawat | leg, calf | Campbell | prefix leftover *-en* |
| D | *kotz'i'j* | K'iche' | flower, candle (already in §10.12) | Christenson | vowel plus glottal plus extra syllable |

Battery clash is mostly A read as "turkey" and B as "brush." Those are not two roots fighting the committed reading. **A is the committed root.** "Offering" is the L-step (sacrificial bird in a ritual frame). T-D also used C (leg) when the seed preferred Nawat.

**Scores**

- Form: A and B tied (same Cordemex head-shape). C leaves *-en*. D is a stretch (already logged).
- Line + neighbors: *tlayeb kutsen* next to *'Ibil*, *kuxkal*, *Ela tlayeb ukto* (burns). A turkey as a sacrificial bird sits in that field. Brush-cleaning can be forced ("laid bare") but does not recur. A leg does not.
- Morphology: *-en* as a Maya suffix on *kuts* is cheap. It does not decide A vs B.

**Verdict: keep A as C+L\*.** The battery "turkey" clash is sense-narrowing of the same lemma, not a different root. Do not replace "offering" with "turkey" in §9: the L-tag already marks the function gloss. Do not promote to H. Log B (brush) and C (leg) in §10.13 as the battery false friends; D stays in §10.12.

### 4.3 *'Ibil* / *'ibil*

Current §9: Maya *il* "see" + *-bil* "the seen → the flesh (laid bare)" (**C+L**). Attestations: lines 6, 15. Soft relative *inib* (*Kí' inib*, §10.4) is not a §9 row.

**Rivals**

| ID | Root | Lang | Gloss | Source | Form |
|---|---|---|---|---|---|
| A | *il* + *-bil* | Yucatec | passive/participle "that which is seen" | Cordemex *IL* (many homophones; "see" is the standard Yucatec verb); *-bil* attested | composition; initial glottal; sense-step to "flesh" is L, not a dictionary gloss |
| B | *IBIL* | Yucatec | to shake, that which must be shaken | Cordemex *IBIL* "sacudir" | **exact lexeme** |
| C | *EBIL* | Yucatec | ladder, stair, step | Cordemex *EBIL* "escalera" | exact fold if *i/e* is granted; T-D used it |
| D | *ib* | Yucatec | lima bean (already in §9 note) | Cordemex | leftover *-il* |

**Scores**

- Form: B wins. C is a vowel away. A is two pieces plus an L-step that no attached dictionary prints as "flesh." D is leftover.
- Line 15 *A'te 'Ibil* is a presentative + noun, the same frame as *A'te ik'el*, *A'te fukuur*, *A'te yuquia*. B as a noun "the shaking" is grammatical. C "the ladder" is grammatical and is what several T-D sheets wrote.
- Couple with *ik'el* (line 6, and the litany 15 vs 16): Maya ritual couplets pair complementary nouns. Seen/spirit or flesh/spirit is a pair. Shake/insect and ladder/insect are not, unless both tournaments take the battery exact hits, which then collapses the litany into "behold the shake, behold the moth."
- *inib*: if *'Ibil* is shake or ladder, *Kí' inib* "sweet, my shake/ladder" is nonsense. That parse is itself soft, so it is weak evidence, not a gate.
- Neighbor field (rule 6, not the token's own English): presentative object in an offering chant, paired with *ik'el*, *kutsen*, *kifba*. A nominal "the seen / the body presented" fits that slot better than a verb "shake" or a stair.

**Verdict: keep A, star it (C+L\*).** Exact *IBIL* "sacudir" is a stronger same-language competitor than the lima-bean note already in §9. It lost on neighbor field plus the *ik'el* couplet, not on form. Do not rewrite the gloss to "shake" (form-first does not mean "always take the exact hit and ignore the line"). Do not demote to S: the presentative-noun pattern is consistent. Do not promote to H: Gate 1 cannot recover "flesh" from attached dicts, and Gate 2 now has an exact homophone. Log B and C in §10.13. D stays as the weaker leftover.

### 4.4 *mucane*

Current §9: Maya *muk'* "strength" + *-ane* "the mighty, the enduring" (**C**). Attestations: lines 1, 27, 43, 45, 46. Lookup whole-form: miss.

**Rivals**

| ID | Root | Lang | Gloss | Source | Form |
|---|---|---|---|---|---|
| A | *muk'* + *-ane* | Yucatec | strength, force, fortitude | Cordemex *MUK'* "animarse, esforzarse"; *CHICH MUK'* "forzudo, valiente" | needs glottal *muk'* vs surface *muc-*; *-ane* honorific already used on *ikba'yucane* |
| B | *muk* "sepultar / encubrir" | Yucatec | to bury, hide, conceal | Cordemex *MUK* "sepultar"; "encubrir, negar, ocultar" | **better glottal fit** (no *'*) |
| C | *muq* | K'iche' | to bury, hide | Christenson *muq<u>* "to bury something"; *muqik* "to bury; to hide" | already in §10.12; same sense as B, sister language |

Battery clash is B ("buried"). That is a real dictionary hit. T-M often abstained (no whole-form), which is the anti-forcing contrast.

**Scores**

- Form: B is closer to the surface (no glottal). A needs *muk'* → *muc*. C is K'iche' corroboration of B, not a third sense.
- Line 27 *u mujuk' le mucane*: if A, figura etymologica "the strength of the mighty." If B, "the strength of the buried." Both are grammatical. The first is a known Maya-style echo. The second is thematically possible in a death cult.
- Lines 43/45 *U'te mucane* (drill response): "behold the mighty" vs "behold the buried." Both possible. Line 1 *ek te mucane Vaal*: "star of the mighty Vaal" vs "star of the buried Vaal."
- Morphology: *mujuk'* is independently read as *muk'* "strength." Keeping *mucane* on the same root is the conservative family. Splitting them (*mujuk'* strength, *mucane* buried) is allowed but costs the echo.

**Verdict: keep A, star it (C\*).** B/C are live co-readings, not dismissed. The echo with *mujuk'* plus the honorific *-ane* pattern keeps A as the lead. Do not silently delete "buried." Do not promote to H. Do not demote to S: both roots are attested. `token_classification.csv` previously survived Gate 2; the tournament writes the Yucatec bury homophone (K'iche' *muq* was already in §10.12 prose but the csv still said survive).

### 4.5 *tlayeb*

Current §9: Nahuatl *tla-* + *tlayohua* "night" → "the (sacred) dark" (**C+L**). Attestations: lines 6 (twice), 21, 22, 40 (twice), 46. Lookup whole-form: **miss**.

**Rivals**

| ID | Root | Lang | Gloss | Source | Form |
|---|---|---|---|---|---|
| A | *tlayohua* | Nahuatl | it gets dark | Nahuatl 1100 *tlayohua* "it gets dark" | stem *tlayo-*; leftover *hua* vs surface *-eb* |
| B | *YEB* | Yucatec | ladder, stair, step | Cordemex *YEB* "escalera" | *tla-* (Nah. prefix) + *yeb* is a **cross-graft**, forbidden under strict latitude |
| C | *tla* | Nahuatl / Nawat | if; trash; arrange/repair; paint | Campbell / Nahuatl 1100 | leftover *-yeb* unexplained |
| D | opaque | none | no attested whole form | lookup miss | honest miss |

T-M mostly abstained (RESULTS: 16/22). T-D mostly clashed as ladder / arrange / rubber (B and C). That is anti-forcing working: methodology withheld; dictionaries-only asserted a cross-graft.

**Scores**

- Form: D is the strict answer (no whole-form). A is the current reconstruction with a large leftover (*-ohua* vs *-eb*). B is the battery favorite and is illegal as a single-language parse. C does not cover the surface.
- Distribution: always immediately before a noun (*kutsen, kifba, ukto, mucane*). Prenominal position is settled (§3.4). Adjective vs fronted locative is a particle-probe question, not a root question (`PARTICLE_PROBES_3_7.md`).
- Neighbor field: *Ela tlayeb ukto* with *Ela* "burns" and *ukto* leading "torch" favors a darkness/night reading of A over a ladder. A ladder next to a burning torch is not impossible. It is worse.

**Verdict: keep A as C+L, do not star a ladder reading, do not demote, do not call opaque.** Whole-form miss is already what C means (latitude-dependent). Demoting to S would be defensible if *tlayohua → tlayeb* is treated as an unresolved sound-step on the same footing as *Xatlene*'s *o→a*. It is **not** treated that way here, because the night/dark lemma is the only same-language candidate that covers the *tlayo-* onset and the ritual field. Ladder (B) is logged as a battery cross-graft, not as a co-reading. Opaque (D) is the T-M behavior, not a lexicon row. Category (attributive vs locative) stays open in §3.7.

No new H. No silent deletion of ladder: it is in §10.13 as a loser.

## 5. Other high-traffic content words on the 16 lines

Short brackets. Same rubric. None of these become H.

### 5.1 *kilya* (line 3; also 31)

Current: Nah. *quil-* "green" + inchoative *-ya* (**C+L**). Lookup: miss. Rival: Yucatec *KIL* "dulzura; pulso" plus leftover *-ya* (T-M). **Keep C+L.** *quil-ya* is still the only parse that segments the whole surface with two attested Nahuatl pieces. *KIL* leftover is logged. Not opaque: the token is recurrent with *ma* (optative) and with *sakilja* (line 31). Not H.

### 5.2 *kifba* (lines 6, 22, 31)

Current: Maya *k'i'ik'* "blood" + *ba'* (**C+L**). Lookup: miss. Rival: Yucatec *KIB* "cera, candela" (T-D seed 55555). **Keep C+L, star it (C+L\*).** The medial */f/* is a loan-only core phoneme (AGENTS diagnostic). That is unexplained residue on the Maya parse, and it is why this token cannot harden. *KIB* "wax/candle" is a real shorter hit and is logged. Do not rewrite the gloss to "candle": neighbor *ik'el / kutsen / 'Ibil* and the couplet with *kutsen* still favor a body-internal noun. Do not demote to S in this pass: *ba'* as reflexive/self is recurrent (*elba, ik'bala*). The */f/* stays a logged defect.

### 5.3 *Tlaxye'* (line 10)

Current: Nah. *tlāl- / tlācah* "land, people" (**C+L**). Lookup: miss. Rival: Nahuatl 1100 *tlaca* "people, persons, men" (exact stem, leftover *-xye'*). Earlier Quechua *llaqta* already rejected (§10.3). **Keep C+L.** *tlaca* is corroboration of the committed lemma, not a different meaning. Leftover *-xye'* is why it is C not H. Logged.

### 5.4 *Ma'oxe* (line 11)

Current: *ma'* "without" + *xok* "count" (**C+L**). Lookup: miss. §10.1 already is a tournament. **No new winner.** Point to §10.1. Exact *xok* "cuenta" is in Cordemex; the whole surface is not.

### 5.5 *Tzokan'te* (lines 18, 38)

Current: Maya *ts'ook* "end, the last" (**C+L**). Lookup whole-form: miss. Rivals: Cordemex *TS'OK / ts’ook* "acabarse, fin, cabo"; Cordemex *TSOK* "arrancar; castigar" (battery tear-out). **Keep C+L, star it (C+L\*).** *TSOK* "tear out / punish" is a same-language different-meaning competitor on the *tzok-* onset. *ts'ook* "end" still wins the field: *Tzokan'te ik'el* next to *Yaxe chikula'* "first sign" is a first/last pair, and *cha'tsoke* is independently *ts'ook*. Log *TSOK*.

### 5.6 *yuquia* (line 24)

Current: Nah. *yocoya* "create, devise" (**C+L**). Lookup: *yocoya* miss; K'iche' *yuq* "stretch, knead" leftover *-ia* (soft). Audio: *u* as /o/. **Keep C+L.** *yuq* is logged as the battery rival (palette-third language, leftover). Not adopted. Not H (*yocoya* absent from attached dicts, same class of miss as *Panquetzaliztli*).

### 5.7 *mujuk'* (line 27)

Current: Maya *muk'* "strength" (**C**). Lookup: miss. Rival: K'iche' *muj* "shadow, ghost, specter" leftover *-uk'* (T-M). **Keep C.** The echo *u mujuk' le mucane* is the field. *muj* leftover is logged, not starred: residue is unexplained, so it is a weak competitor, not a Gate-2 equal.

### 5.8 *i'chian* (line 27)

Current: Nah. *ichan* "his/her home" (**C**). Lookup: Nahuatl 1100 *ichan* "his house / her house" **exact**. Extra *i'* / apostrophe is the only leftover. **Winner: current reading.** Clash was coverage (T-M often missed the Nahuatl extra list or treated *ICH* "in" plus leftover). No star. No H (apostrophe leftover; not in the recovery-pass set).

### 5.9 *niáach* (line 27)

Already **C\*** (*náach* "far"; Gate 2 fall). Extra *i* is latitude. Battery sometimes matched "far." Not a new tournament. Keep.

### 5.10 *puyao* (lines 36, 37)

Already **soft** in §10.4 (Nah. *poyahua* "to darken, redden"). Lookup: miss. Rival: *puy* "beso / cobertura" leftover *-ao*; K'iche' *puy* "stab." **Stay S.** Do not promote. Clash lines are expected: the token is not in §9.

### 5.11 *tlapec* (line 37)

Current: Nah. *tlapechtli* "platform, altar-bed" (**C+L**). Lookup whole-form: miss (*-tli* coda). **Keep C+L.** Licensed loose leftover is exactly why it is C. No new rival that covers more of the surface.

### 5.12 *itsok* (line 37; also 4, 12, 35)

Already **C+L** with live co-reading Nah. *itztli* "obsidian" in §10.12. Lookup whole-form: miss. **Keep.** Strongest original cross-language competitor, unchanged.

### 5.13 *uch'* (line 37)

Already **C\*** (drink vs crush vs K'iche' opossum). Battery often took Cordemex *UCH'* "aplastado, deformado" (crush). That is one of the two committed readings, not a new false friend. **Keep C\***.

### 5.14 *ta'nuk* (line 37)

Current: *nuk* "big, great"; *ta'-* soft (**C**). Lookup: *NUK* "gorda, gruesa; ancianidad." **Keep C.** *ta'-* still open (same item as particle *ta'*).

### 5.15 *Otsuks, Axba, Kíibsa'* (lines 38, 49)

Already **soft** in §10.9. Lookup whole-forms: miss. *tsuk* "cluster" and *ba'ax* "what" and *kíims* "kill" remain the leading pieces. **Stay S.** Clash is expected. Do not promote on a tournament that did not close their open steps (coda *-s*, metathesis, *m→b*).

## 6. Outcome table

| Token | Was | Outcome | Now | Why |
|---|---|---|---|---|
| *ik'el* | C+L | keep-as-C\* | **C+L\*** | exact insect lexeme is a real homophone; *ik'* family plus neighbor field keep spirit/breath |
| *kutsen* | C+L\* | winner = same root | **C+L\*** (no move) | turkey is the same lemma; brush and Nawat "leg" lose the field |
| *'Ibil* | C+L | keep-as-C\* | **C+L\*** | exact *IBIL* "sacudir" (and *EBIL* ladder) logged; couplet plus presentative slot keep "the seen / flesh" |
| *mucane* | C | keep-as-C\* | **C\*** | Yucatec *muk* "bury" and K'iche' *muq* live; *muk'* echo with *mujuk'* keeps "mighty" |
| *tlayeb* | C+L | keep C+L | **C+L** (no move) | whole-form miss; ladder is a cross-graft; night/dark still the only same-language onset |
| *kux / kuxkal / kuxte'* | C+L\* | winner *kux/kuxtal* | **C+L\*** (no move) | methodology plus merism plus family beat Nawat *kuxta* cacao-tree |
| *kilya* | C+L | keep | **C+L** | *KIL* leftover logged |
| *kifba* | C+L | keep-as-C\* | **C+L\*** | */f/* unexplained; *KIB* wax logged |
| *Tlaxye'* | C+L | keep | **C+L** | *tlaca* corroborates |
| *Ma'oxe* | C+L | keep; see §10.1 | **C+L** | no new winner |
| *Tzokan'te* | C+L | keep-as-C\* | **C+L\*** | *TSOK* tear-out/punish logged; first/last field keeps *ts'ook* |
| *yuquia* | C+L | keep | **C+L** | *yuq* stretch logged |
| *mujuk'* | C | keep | **C** | *muj* specter leftover too weak to star |
| *i'chian* | C | winner current | **C** | exact *ichan* |
| *puyao* | S (§10) | stay S | **S** | no promotion |
| *Otsuks, Axba, Kíibsa'* | S (§10) | stay S | **S** | open steps remain |
| *itsok, uch', tlapec, ta'nuk, niáach* | already C/C\* | no move | same | already logged or latitude-only |

No token is promoted to **H**. No competitor is silently deleted. Hypothesis check: most 5/5 clashes **are** Cordemex / ilide exact hits that lose once the rest of the corpus is scored. Three of those hits were not previously starred (*ik'el, 'Ibil, mucane*). One (*kutsen* turkey) was the same root. *tlayeb* ladder never deserved a lexicon row. Sol follow-up: keep Kenichi's gloss on *'Ibil*, *mucane*, *tlayeb*, *kifba*; C* already on *'Ibil*, *mucane*, *kifba*; *tlayeb* stays C+L because the ladder rival is a cross-graft, logged in §10.13.

## 7. Files touched (this pass)

- This document; `rival_tournament_brackets.csv`
- `token_classification.csv` (five new stars: *ik'el, 'Ibil, mucane, kifba, Tzokan'te*)
- master §9 notes, §10.13, §14 pointer, §17.4 C\* count
- `STATISTICAL_SUMMARY.md` tier split
- `EXPERIMENT_LOG.md` dated block
- `PARTICLE_PROBES_3_7.md` (separate)

Not touched: PDF, dictionary extracts, `gate2_rescore_rerun.csv`, parent/canonical identity except the listed master edits.

## 8. Reproduce

```
python3 dict_lookup.py --build
python3 dict_lookup.py "ik'el" --latitude strict --access online
python3 dict_lookup.py kutsen --latitude strict --access online
python3 dict_lookup.py "'Ibil" --latitude strict --access online
python3 dict_lookup.py kuxte' --latitude strict --access online
```

Attached dictionaries via `VAAL_DICT_DIR`. Gold and §9 were opened only after the T-M/T-D sheets existed; this tournament is a post-hoc contest, not a blind decode.
