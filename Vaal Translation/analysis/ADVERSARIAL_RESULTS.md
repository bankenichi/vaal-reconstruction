# Adversarial survival of the committed lexicon

## 2026-09 addendum (Gate 2 hole N3)

The original method (below) counted a competitor only when the adversary's language class differed from the committed class. `score_adversarial.py` now counts a **strong different-meaning** competitor regardless of language, including same-language homophones and plus-join alternate segmentations. Same-meaning cognates remain corroboration.

Re-score of the archived CSVs (`gate2_rescore.csv`): **47 survive / 58 testable = 81%**, 11 falls, of which 7 involve a same-language competitor. New falls relative to the old effective-7 list: *'Ibil* (lima bean), *Ik'eche* (ik' + che' tree), *ta'nuk* (lime/ash), *tul* (animate classifier). Residual limit: competitors a decoder never wrote down are not invented. *ek* wasp is a Gate-1 failure, not a Gate-2 CSV row.

*pul* has no adversarial row; its old "survives" claim is dropped with its Gate-1 pass.

The historical write-up from the original cross-language-only pass is kept below.

---

## Method (original, cross-language filter)

The 61 committed tokens (labels C / C+L, extracted from master section 9; the lexicon later reached 62 with the addition of *pul*) were handed, surface form only, to four fresh "adversary" agents blind to every existing reading. Each agent independently found, form-first, the best-attested root for a token and the best-attested root from a *different* source language. A committed token FALLS if the adversary produced a **strong** attested root in a language different from the one the project committed to (evidence the reading is one-of-several, not uniquely forced). It SURVIVES otherwise. Three pure in-game names (Vaal, Zerphi, Guatelitzi) are N/A.

Batch results: `adversarial_results_batch{1..4}.csv`. Scorer: `score_adversarial.py`.

## Headline

- Testable tokens: 58 (plus 3 names, N/A).
- **Raw survival: 47 / 58 = 81%.** 11 falls.
- On inspection the 11 falls split into two very different kinds (see below): 4 are cognate or already-dual artifacts (not genuine competition), 7 are genuine different-root reinterpretations.
- **Effective survival (removing the cognate artifacts): 51 / 58 = 88%.**

## The 11 falls, triaged

### Not genuine competition (4): the sister language simply shares the root

These fell only because the adversary found the same root in a cognate language, or the committed entry is already dual-sourced. They are corroboration, not competition, and need no change.

- **ma** committed as "Nah. ma / Maya ma'" already, and the adversary's Maya `ma'` "not" is one of the two sources the entry names. Non-issue.
- **qexcan**: adversary's K'iche' `k'ex` "change" is the *same root* as the committed Maya `k'ex` (k'ex is pan-Mayan). Cognate, same meaning.
- **sakilja**: adversary's K'iche' `saqil` "whiteness" is the cognate of committed Maya `sak` "white" (sak = saq). Same compound in the sister language.
- **Yutsal**: adversary's K'iche' `utz` "good" is the cognate of committed Yucatec `uts` "good"; the entry already notes this. Same meaning.

### Genuine competitors (7): a different root, a different plausible meaning

These are real alternative readings that a blind analyst preferred from the form alone. They do not automatically overturn the committed reading (context and neighboring tokens still matter, and are not available to the adversary), but each one weakens the claim that the committed reading is uniquely forced, and each should be logged as a live alternate.

| Token | Committed reading | Adversary's competitor | Assessment |
|---|---|---|---|
| **itsok / itzil** | Maya *iitz* "essence, blood" | Nahuatl **itztli** "obsidian (sacrificial blade)" | **Strongest challenge.** Obsidian blade is thematically as apt as "blood/essence" in a sacrifice corpus, form fit is clean, and it is Nahuatl (a core palette language, not a stretch). This deserves to be logged as a serious co-reading, not a footnote. |
| **tala** | Maya *taal* "to come" | Nawat/Nahuatl **ta:l** "earth, land" | Form-identical, both attested, different meaning. Context (the smith's line) favors "come," but the ambiguity is real. |
| **pochiti** | Maya *poch* "hungry" (+ Nah. -ti) | Nawat **puchini** "it bursts, frays" | Competitor to the lore-anchored "Hungering One." Lore still favors *poch*, but the form supports another root. |
| **kutsen** | Maya *kutz* "sacrificial bird" -> "the offering" | K'iche' **kotz'i'j** "flower, candle" | Both plausible as an offered thing; the committed reading leans on the bird-as-offering step. |
| **A'te / U'Te** | Maya presentative *at / yan* "behold" | Nahuatl **ahtle** "nothing" | Form competitor with an opposite meaning; context (offering gesture) favors the presentative, but the form alone does not force it. |
| **te** | Maya *ti' / te'* relational "of, to" | Nahuatl **tetl** "stone" | A function-word reading vs a content-word reading; syntax favors the relational, but the bare form is ambiguous. |
| **mucane** | Maya *muk'* "strength" -> "the mighty" | K'iche' **muq** "to bury, hide" | Already carried in the entry as the shadow sense *muk* "bury," so partly acknowledged. |

## Interpretation

The committed lexicon holds up reasonably well: 88% of testable tokens have no genuine cross-language competitor once cognates are set aside. That is meaningfully better than the null-model noise floor and is the strongest evidence so far that the committed tier is not simply decoded noise.

But the exercise did what it was meant to. Seven committed readings turn out to be one-of-several on form alone, and one, **itsok -> itztli "obsidian,"** is a genuinely strong alternative. The pattern is also telling: every genuine competitor is a content-plausible root that the committed reading beats only by appeal to *context* (neighboring tokens, lore), never by phonology alone. That is exactly the latitude-and-context dependence the review flagged.

## Outcome (implemented)

All of the following were acted on and are now in the master; this section records the result, not a proposal.

1. **itsok / itzil:** Nahuatl *itztli* "obsidian, sacrificial blade" is logged as a strong co-reading in section 10.12, and the section 9 note reads "leading reading, with a live Nahuatl competitor." The token carries the **C\*** tier.
2. **tala, pochiti, kutsen, A'te, te:** each is tagged **C\*** in the lexicon (section 9) with a one-line form-alternate note recording the competitor, keeping the committed reading as leading on contextual grounds.
3. **mucane:** tagged **C\*** as well (K'iche' *muq* "to bury"), giving seven C\* tokens in total. **ma, qexcan, sakilja, Yutsal:** no change (cognate corroboration, already dual-noted).
4. The standing rule was adopted: a token earns the top tier only after passing the adversarial gate, and any token with a genuine different-meaning competitor is flagged **C\***. This is written into AGENTS.md rule 2b and the two-gate hardening protocol (`HARDENING_PROTOCOL.md`); the empirical basis is master section 17.

Net: 7 of the 62 committed tokens carry a logged competitor (C\*); the other 55 survived the adversarial pass with none.
