# Leave-one-text-out consistency (2026-09-16)

Closed 51-line gold set (Texts 1-4 plus Kamasan Smith), same partition as `TRANSLATION_BATTERY_RESULTS.md` / `translation_battery_gold.csv`. This is not a new null-model battery, not PPV, and not a sentence-band product. Headlines are Wilson 95% CIs on held-out parse/gloss recovery.

Scorer: `score_loto_secure.py`. Table: `loto_line_scores.csv`.

## 1. Why

The published English can be internally consistent even when a text is full of hapaxes, or it can depend on text-specific commitments that do not transfer. Leave-one-text-out (LOTO) asks: from the other texts only, can a minimal working lexicon plus an order sketch parse and gloss the held-out surface lines?

## 2. Protocol

Five folds. One text held out at a time.

| Fold | Held-out text | Gold lines | N |
|---|---|---|---:|
| T1 | Atziri Chant | 1-8 | 8 |
| T2 | Cuachic Vault Litany | 9-24 | 16 |
| T3 | Commander block | 25-37 | 13 |
| T4 | Drill (catechism plus two one-offs) | 38-49 | 12 |
| T5 | Kamasan Smith | 50-51 | 2 |

**Training inputs (allowed):** surface lines of the other texts; published English of those training lines only; constructions that actually occur in training.

**Held-out inputs while parsing:** surface lines only.

**Scoring key (after the parse):** held-out published English. Same match/partial idea as the translation-battery rubric: ok needs the same main predication and referents; partial is a recoverable core with a hole or a minor sense error; fail is a different predication, or a line whose content is mostly unseen.

**Working lexicon.** Every training surface token may carry the gloss that the training gold actually uses for it. Licensed stem transfer is allowed when a held-out surface shares a documented family with a training surface (*ik'*, *kux*, *muk'*, *aocmo*, *el*, *k'ex*, *itsok*, *ts'ook*, *'Ibil/inib*, *jare*, *tul* in *jare'yantul*, *ātl*). Stem transfer is not a license to import the held-out gold.

**Order sketch.** Rebuilt per fold from training distribution only. Clause-initial presentative, vocative, privative, and imperative are available whenever those openers occur in training. Interrogative *Máax* is T4-only. Possessed-before-possessor (*u mujuk' le mucane*) is T3-only. Prenominal *tlayeb* / *le* transfer when they occur in training.

Gold of the held-out text was not a search key. §9 rows that appear only in the held-out text were not used as training commitments.

## 3. Scoring rubric

- **ok:** every load-bearing token is in the training lexicon (exact surface or licensed stem), the fold's order sketch licenses the clause type, and the composed gloss matches the held-out gold predication.
- **partial:** at least one load-bearing piece is known and does not clash with gold, but a hapax, a missing operator (*Máax*), or a sense split (T1 *ek* star vs T5 *ek* dark) blocks a full match.
- **fail:** the main predication cannot be recovered. A leftover name or presentative is not a gift.

Name-only *Atziri!* is ok when *Atziri* occurs in training (T1, T2, T3). That inflates T4 the same way the translation battery's vocatives inflate match.

## 4. Headlines (Wilson 95%)

N = 51 held-out lines (each line scored once, in the fold that holds its text out).

| Rate | Wilson 95% |
|---|---|
| ok | 12/51 = **23.5% [14.0, 36.8]** |
| ok+partial | 33/51 = **64.7% [51.0, 76.4]** |
| fail | 18/51 = **35.3% [23.6, 49.0]** |

Macro-average of the five fold rates: ok **18.3%**; ok+partial **62.9%**. The macro is pulled down by T3 and T5. It is not a second inferential unit; the 51-line table is the headline.

## 5. Per fold

| Fold | N | ok | partial | fail | ok Wilson | ok+partial Wilson |
|---|---:|---:|---:|---:|---|---|
| T1 chant | 8 | 1 | 5 | 2 | 1/8 = 12.5% [2.2, 47.1] | 6/8 = 75.0% [40.9, 92.9] |
| T2 litany | 16 | 6 | 5 | 5 | 6/16 = 37.5% [18.5, 61.4] | 11/16 = 68.8% [44.4, 85.8] |
| T3 commander | 13 | 0 | 7 | 6 | 0/13 = 0.0% [0.0, 22.8] | 7/13 = 53.8% [29.1, 76.8] |
| T4 drill | 12 | 5 | 3 | 4 | 5/12 = 41.7% [19.3, 68.0] | 8/12 = 66.7% [39.1, 86.2] |
| T5 Kamasan | 2 | 0 | 1 | 1 | 0/2 = 0.0% [0.0, 65.8] | 1/2 = 50.0% [9.5, 90.5] |

T3 has **zero** ok lines. That is the weakest fold, as hypothesized. T4 looks stronger because three vocative *Atziri!* lines are ok and *U'te mucane* recurs from T1/T3. Drop those five T4 gifts and T4 is 0/7 ok, 3/7 ok+partial. T2 ok lines are mostly the couplets already present in T1 (*'Ibil*, *ik'el*, *tlayeb kutsen*, *tlayeb kifba*) plus *Tzokan'te ik'el* from T4.

T5 is N = 2. The CIs are wide on purpose.

## 6. What transferred, and what did not

**Transfers that actually fire.** Presentative *A'te / U'Te* plus a noun already seen in another text. *ik'* family (*ik'el / ik'bala / ikba'yucane / Ik'eche*). *kux* life (*kuxte' / kuxkal*). *muk'* strength (*mucane / mujuk' / ko'mujuk*). Privative *Aiokmo / 'Ayok*. *jare* plus *tul* inside *jare'yantul*. *ts'ook* between *Tzokan'te* and *cha'tsoke*. *'Ibil* to *inib*.

**Held-out-only walls.** T1: *Teoyuxtlane*, *ascensionada*, *akal*, *Zerphi*, *til*, *xu'te*, *anab*, *nochira*. T2: *Tlaxye'*, *Gyan'uks*, *ko'janti*, *Yaxe*, *chikula'*, *líimek*, *yuquia*, *Xatlene*, *Ma'oxe*, *kíimil'*. T3: *fukuur*, *daka*, *puxe*, *puyao*, *Donuks*, *xefe*, *tlapec*, *uch'*, *sakilja*, *Eche lu nochbe*. T4: *Otsuks*, *Máax*, *a'tul*, *cheyel*, *ukto*, *Axba*, *Kíibsa'*, *quxzeh*. T5: *tala*, *upulché*, *yan*.

*xefe* is the only H token in the 51-line corpus, and it is T3-only. Holding out T3 removes the hardened commander title from the training lexicon. That is a feature of the partition, not a demotion of *xefe*.

## 7. Order sketch, per fold (training only)

| Fold | Presentative | Vocative *Atziri* | Privative | Imperative *Xi* | Interrogative *Máax* | Prenominal *tlayeb/le* | Possession *u N le N* |
|---|---|---|---|---|---|---|---|
| hold T1 | yes (T2, T3, T4) | yes | yes ('Ayok T3) | yes (T3) | yes (T4) | yes | yes (T3) |
| hold T2 | yes | yes | yes (both) | yes (T1, T3) | yes (T4) | yes | yes (T3) |
| hold T3 | yes | yes | yes (Aiokmo T1) | yes (T1) | yes (T4) | yes | **no** |
| hold T4 | yes | yes | yes | yes (T1, T3) | **no** | yes | yes (T3) |
| hold T5 | yes | yes | yes | yes | yes | yes | yes |

Holding out T4 deletes every question. Holding out T3 deletes the one possessed-before-possessor string. Those gaps are why lines 42/44 fail and why line 27 is only partial.

## 8. Leaks (documented)

Unavoidable overlap, not hidden gold:

1. Shared names (*Atziri*, *Vaal*) that occur in training.
2. Stem families listed above. These are form-first family licenses, not held-out glosses.
3. The T1/T5 *ek* split: training T5 tells a T1 parser that *ek* is dark; training T1 tells a T5 parser that *ek* is star. That is a real sense clash inside the published English, not a LOTO artifact.
4. *tul* vs *pul* were **not** merged. *jare'yantul* can donate *tul* "wane"; it cannot donate *upulché* "cast down".
5. Global master §3 was not copied in. Each fold's sketch uses only training attestations. The published §3.7 particle verdicts were not imported as extra lexicon.

Held-out gold English was opened only to assign ok / partial / fail after the parse. It does not appear in the training lexicon.

## 9. What the numbers are not

- Not PPV, not a product-of-token sentence band, not a 10^-15 test.
- Not a claim that T3 is "wrong." T3 is hapax-heavy. LOTO measures transfer, not designer intent.
- Shared couplets (*tlayeb kutsen*, *A'te 'Ibil*) raise T1-held-out and T2-held-out together. That is recurrence, which is the point of the test.

## 10. Reproduce

```
python3 score_loto_secure.py
```

Gold: `translation_battery_gold.csv` (same 51-line extractor as the translation battery). Per-line reasons: `loto_line_scores.csv`.
