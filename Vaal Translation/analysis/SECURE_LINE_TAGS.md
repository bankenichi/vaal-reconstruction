# Secure-line tags (2026-09-16)

Editorial stress test on the 51 published English lines (the gold set). Companion to the T-M / T-D agreement CIs, **not** a revival of model PPV or sentence-level products. Scorer: `score_loto_secure.py`. Table: `secure_line_tags.csv`. Tiers from `token_classification.csv` plus §10 softs.

## 1. Why

A line of committed tokens is not a secure translation. This table asks how many published lines are carried only by hardened roots, how many mix in competitors or softs, and how many are blocked by an opaque slot.

## 2. Protocol

**Load-bearing content.** Whitespace tokens after punctuation strip. Particles excluded: *a'te, u'te, Yatle* (one presentative row), *le, le', ti, ti', ka, ta', u, ma, ma', na', en*. Onomastic *Atziri, Zerphi, Vaal* **are** load-bearing here, because they are referents in the published English. (The translation-battery token rate excluded those names. Using that exclusion would make *Atziri!* vacuously secure. That is rejected.)

**Long form.** *jare'yantul* is segmented into *jare'* + *yan* + *tul* because §8 and the published English treat it as three content words. Other fused forms stay whole (*le'itzil, ek'le, upulché, ikba'yucane*).

**Line grade**

| Grade | Rule |
|---|---|
| **secure** | every load-bearing token is H (H+L counts as H) |
| **working** | every load-bearing token is H or plain C (C+L counts as C; no star) |
| **fragile** | any C* or S on a load-bearing slot |
| **opaque-blocked** | any O on a load-bearing slot |

L is orthogonal. A star is a competitor. Soft §10 tokens that are not §9 rows are S. *yan* is O (not a lexicon row).

The only H token in the 51-line corpus is *xefe* (line 35). *Quecholli* (still H+L) and *Ixchel* (now C+L after the Gate 1 sense miss) do not occur in these lines. Working count is unchanged by the Ixchel demotion.

## 3. Headlines (Wilson 95%)

N = 51 lines.

| Grade | Wilson 95% |
|---|---|
| secure | 0/51 = **0.0% [0.0, 7.0]** |
| working | 12/51 = **23.5% [14.0, 36.8]** |
| fragile | 38/51 = **74.5% [61.1, 84.5]** |
| opaque-blocked | 1/51 = **2.0% [0.3, 10.3]** |

Almost no secure lines (none). Many fragile. One opaque-blocked line (Kamasan *jare'yantul*, because *yan* has no §9 row). This is the translation-confidence companion to T-M / T-D: agreement CIs measure reproducibility under the kit; these grades measure how much of the published English sits on H versus C* / S / O.

Do not multiply these shares into a sentence PPV. Do not quote the withdrawn independence product in master §17.5 as if this table restored it.

## 4. Working lines (12)

All load-bearing tokens H or plain C. None is secure.

| Line | Surface (short) | Why working, not secure |
|---|---|---|
| 2 | *Teoyuxtlane ascensionada ... Yutsal* | three C / C+L names and a Spanish loan; Gate 1 failed on *ascensionada* |
| 3 | *ma kilya Zerphi* | *kilya* C+L, *Zerphi* C; *ma* excluded as particle |
| 5 | *ikba'yucane Vaal* | *ikba'yucane* C (leftover *yuc*, family audit); not H |
| 10 | *Tlaxye' le Vaal* | both C+L |
| 12 | *Atziri le'itzil* | C+L; *itzli* competitor lives on *itsok*, not on this fused vocative as a star in the row used here |
| 14 | *Gyan'uks ko'janti* | both C+L |
| 19 | *A'te líimek* | *líimek* C+L |
| 20 | *Yatle yutsal* | presentative excluded; *yutsal* C+L |
| 24 | *A'te yuquia* | *yuquia* C+L |
| 39, 41, 47 | *Atziri!* | name is C+L |

T3 contributes **zero** working lines. Every commander line has a C* or an S hapax. Line 35 contains the corpus's only H (*xefe*) and is still fragile because *te'moxti* is S.

## 5. Opaque-blocked (1)

Line 50 *Ti ek tala jare'yantul!* segments to *ek* C*, *tala* C, *jare'* C, **yan O**, *tul* C*. The published English "and so, your waning" spends *yan* as a content word that §9 does not carry. That is an opaque slot, not a C* competitor.

Line 51 *Ti' ek'le upulché* is fragile (C* on *ek* and *pul*), not opaque. The *-ché* tail is S inside a *pul* row, not a separate O.

## 6. Fragile mass (38)

Typical blockers:

- Tournament stars: *ik'el, 'Ibil, kutsen, kifba, mucane, Tzokan'te, kux / kíimil*.
- Gate-2 stars already on the 61-row sheet: *ek, te, akal, til, tul, nochira, máax, náach, ich, uch', ki'*.
- Text 3/4 softs: *fukuur, Donuks, puyao, Otsuks, a'tul, cheyel, Axba, Kíibsa', ukto, Xatlene*.

A short presentative line is fragile as soon as its noun is starred (*A'te 'Ibil*, *A'te ik'el*, *U'te mucane*, *U'Te kuxkal*). Recurrence does not harden it.

## 7. What this is not

- Not PPV. Not a Frechet sentence band. Not "probability the English is the designer's intent."
- Not a claim that working lines are correct. Working means the published line does not currently rest on a starred competitor, a soft, or an opaque. T-M / T-D still clash on several of those lines.
- Shared dictionaries still pull T-M and T-D into the same false friends. This table does not undo that.

## 8. Reproduce

```
python3 score_loto_secure.py
```

Requires `translation_battery_gold.csv` and the tier map in the scorer (synced to `token_classification.csv` plus §10).
