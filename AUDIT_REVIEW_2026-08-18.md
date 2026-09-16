# Review of `FULL_AUDIT_2026-08-18.md`

Date: 2026-08-18
Reviewer: Claude (Cowork session), working from the canonical tree, the mirror, and the raw analysis CSVs
Method: every checkable claim in the audit was re-derived from the project's own files. Counts were recomputed from `analysis/*.csv`, tier tables from master section 9, statistics in Python with scipy, and copy integrity by direct `md5sum`, `diff`, and a staged direct Read (never a bare mount read as verification).

## Verdict on the audit

**The audit is substantially correct and should be acted on.** Its central claim, that Gate 1 measures whether a string finds *any* dictionary root and not whether it finds *our* root, is verified in the code and in the raw decode records. Every structural, taxonomic, and repository-integrity finding reproduces exactly, several of them token for token.

**Three things in it are wrong or overstated, and one of them is the headline number.** The audit's selection-matched p of 0.197 comes from an apples-to-oranges pairing. The like-for-like comparison exists in the same files and gives p between 0.005 and 0.06. And the audit's assurance that "the count arithmetic is correct" is itself incorrect: the single number the whole null rejection rests on, 23 of 62, does not reproduce from the artifact it cites.

Net effect: the audit does not overturn quite as much as it claims, but the direction of every major criticism holds, and the remediation list is the right one.

## Part 1: findings that reproduce exactly

### F1, the scorer ignores the proposed root and gloss. CONFIRMED, and this is the important one.

`analysis/score.py` reads exactly two fields per row, `confidence` and `found`. The `root`, `lang`, and `gloss` columns exist in every result CSV and are never read. A real token counts as a true positive whenever a blind agent writes `C`, regardless of what it matched.

The consequence is not hypothetical. From `strict_committed_results_batch*.csv`, the decodes that earned Gate 1 passes:

| Token | Section 9 published reading | What the strict decoder actually accepted | Tier awarded |
|---|---|---|---|
| `akal` | Maya *akal* "pond", glossed still / eternal waters | Yucatec *akal*, "to quarrel/scold" (Campeche) | H |
| `ek` | Maya *ek'*, star / black / dark | Yucatec *ek*, "a large wasp" | H |
| `tul` | Maya *tul* "decline", glossed wane, dwindle | K'iche' *tul*, "reed, bullrush" | H |
| `uch'` | Maya *uk'* "drink" or *puuch'* "crush" | K'iche' *uch'*, "opossum" | H |
| `xi` | Nahuatl *xi-*, imperative "do! / make!" | Yucatec *xi'*, "go" | H |

Six of the 26 recorded Gate-1 passes validated a different root, a different language, or a different sense than the entry they were used to harden. The `H` tier is therefore not certifying the reading it is attached to. This finding alone invalidates the interpretation of every PPV and every sentence-level probability, and it is correct.

Note also that `xi-` in Classical Nahuatl is the optative/imperative *prefix* that replaces the second-person subject marker. It is not a free verb meaning "do" or "make". The section 9 gloss is wrong independently of the scoring problem.

### F5, section 9 has 78 rows against 65 in the CSV. CONFIRMED, token for token.

Recount of the section 9 table, confidence column:

| Tier | Count |
|---|---:|
| C | 21 |
| H | 19 |
| C+L | 16 |
| L (alone) | 13 |
| H+L | 6 |
| C\* | 3 |
| **Total data rows** | **78** |

`token_classification.csv` has 65 rows. The 13 `L`-only entries the audit lists are exactly the 13 present: *chikula'*, *Gyan'uks*, *kíimil*, *ko'janti*, *kux / kuxkal / kuxte'*, *le / le'*, *líimek*, *Ma'oxe*, *Tlaxye'*, *Tzokan'te / tzok*, *Xatlene*, *yax / Yaxe*, *yuquia*. AGENTS.md rule 2b says `L` is orthogonal and must combine with `H` or `C`, so all 13 violate the project's own taxonomy, sit outside every reported denominator, and are used in the translations anyway. Hardened total is 19 + 6 = 25, so 25/78 = 32.1% is the correct raw hardened share of the table a reader actually consults.

### F6, hardened entries violate the hardening protocol. CONFIRMED against section 9.

- `k'ux (quxzeh)` is `H`, and its own note says "*-zeh* coda is a non-morphemic tail". Gate 1 forbids unexplained residue.
- `uch' / pu uch'` is `H` while its own note reads "Ambiguous: *uk'* fits the draught theme; *puuch'* fits his Crush! barks". A hardened entry carrying two incompatible readings is a contradiction in terms.
- `ma` is `H` bundling Maya *ma'* negation and Nahuatl *mā* optative in one row.
- `ek`, `xi`, `tul`, `akal` are hardened on passes that matched other senses, per F1.

Gate 2 as written searches only for a *different-language* competitor (`score_adversarial.py` explicitly skips any candidate whose language class equals the committed class). Same-language homophones are structurally invisible to it, which is exactly how *ek* "wasp" and *akal* "quarrel" survive.

### The sigma labels. CONFIRMED, precisely.

| Claimed p | Quoted sigma | Count z-score | True one-sided normal-tail sigma |
|---:|---:|---:|---:|
| 2 x 10^-15 | 12.2 | 12.21 | 7.87 |
| 4 x 10^-16 | 12.8 | 12.83 | 8.04 |
| 3 x 10^-18 | 13.6 | 13.62 | 8.64 |
| 5 x 10^-19 | 14.3 | 14.30 | 8.83 |

The quoted sigmas match the count z-score to two decimals in all four cases. The audit's diagnosis is exactly right: the sigma label reports the standardized count, not the normal-tail equivalent of the binomial p. Remove the sigma column.

### F8, syntax pseudoreplication. CONFIRMED and quantified.

The published 12/12 versus 0/8 Fisher table reproduces at p = 7.94 x 10^-6. But 12 is 3 analysts times 4 rules and 8 is 2 analysts times 4 rules. Scored at the real experimental unit, analyst by corpus, the table is 3/3 versus 0/2 and Fisher gives **p = 0.10**. Not significant.

The blinding objection is confirmed by the master's own wording: section 17.8 states the analysts were given "surface lines, English translations, and a token glossary". They were not blind to the project's readings. The master concedes the limit in its "honest caveat" paragraph, which the audit does not credit, but the Fisher table is still presented as a chance test it cannot support.

On the chance model, the master's (1/2)^3 = 0.125 is right only if agreement on the *specific predicted value* is required. If agreement on either value counts, it is 0.25, and the six-parameter figure moves from 3.8 x 10^-6 to 2.4 x 10^-4. Both are academic next to the non-independence problem.

### F7 (partial), `yan` has no lexicon entry. CONFIRMED.

Section 17.5 assigns *yan* a token-level `C*` probability inside the Kamasan Smith line. There is no `yan` row in section 9 and no `yan` row in `token_classification.csv`. It appears only inside the source column of the *A'te / U'Te / Yatle* entry. The claim that every token in that line is committed is false.

### Repository integrity. CONFIRMED, every claim.

| Copy | md5 | bytes | lines |
|---|---|---:|---:|
| canonical `Vaal Translation/` | 5ae88209... | 211578 | 1398 |
| parent `Vaal Reconstruction/` | f97c8b1e... | 211577 | 1397 |
| mirror `Vaal Translation Mirror/` | 9238c1d9... | 211516 | 1397 |

- Parent differs from canonical only by the trailing newline.
- Mirror carries a genuinely older paragraph at line 847, in section 12.5, describing the post-battery names as sitting "beside the 62-token statistical corpus" rather than the current enlarged-base wording. This is a real body divergence, not a read artifact.
- Mirror `AGENTS.md` is 17342 bytes against 17522 and ends mid-word at `... Nahuatl *ocotl* "pine `. Verified with a direct Read on a staged copy, not a mount read, so it is genuine truncation. The mirror is also missing the entire "Imported Claude Cowork project instructions" section.
- Canonical 101 files, mirror 100. Mirror lacks `analysis.7z` and `analysis/VERIFICATION_PASS_2026-07-06.md`, and carries an extra `Vaal_Reconstruction (# Name clash 2026-07-13 29w3c8C #).md`.

The mirror is not a verified backup and should not be treated as one until reconciled.

### Battery A-D pooled counts. CONFIRMED.

| Battery | Pseudo C | Real C |
|---|---:|---:|
| A loose offline | 31/500 | 31/150 |
| B loose online | 40/500 | 26/150 |
| C strict offline | 17/500 | 19/150 |
| D strict online | 23/500 | 21/150 |

All four cells reproduce from the key and result CSVs.

## Part 2: where the audit is wrong or overstated

### O1. The headline p of 0.197 is the weakest of several defensible estimates, and it comes from a mismatched pairing.

The audit's selection-matched test compares:

- real arm 23/62, from the **strict-committed run** on tokens selected by the project's own human loose search, and
- pseudo arm 8/31, from the **blind Battery A to D pipeline**.

Two different filters and two different strict tests. The genuinely like-for-like comparison is available in the same files, applying the same blind loose filter (Battery A) and the same blind strict test (Battery D) to both arms:

| Comparison | Real | Pseudo | Fisher one-sided p |
|---|---|---|---:|
| Audit's pairing | 23/62 = 37.1% | 8/31 = 25.8% | 0.197 |
| Same pairing, CSV-verified real count | 21/61 = 34.4% | 8/31 = 25.8% | 0.275 |
| **Matched within A to D, trial level** | **19/31 = 61.3%** | **8/31 = 25.8%** | **0.0049** |
| Matched within A to C offline, trial level | 21/31 = 67.7% | 8/31 = 25.8% | 0.0010 |
| **Matched, de-pseudoreplicated to item level** | **6/9 = 66.7%** | **8/27 = 29.6%** | **0.058** |

So the honest statement is not "the null rejection fails". It is: **conditioning on selection collapses the claimed 2 x 10^-15 to somewhere between roughly 0.005 and 0.2, depending on how the arms are matched and whether repeated seeds are counted as independent.** The signal survives as marginal rather than overwhelming. The audit is right that the published figure is indefensible and right about the mechanism; it is wrong to present the single weakest matching as the answer, and it does not flag that its own real arm was filtered differently from its pseudo arm, which is the same class of error it charges the project with.

### O2. "The count arithmetic is correct" is not correct, on the number that matters most.

The audit states the raw counts reproduce. The headline 23 of 62 does not.

- `strict_committed_results_batch{1..4}.csv` contains **61 rows**, not 62, and **21** carry `confidence = C`, not 23.
- `analysis/EXPERIMENT_LOG.md` line 15 itself records the run as "61 committed tokens".
- `token_classification.csv` records **26** `gate1_strict = pass`. Reconciling that against the CSVs: 3 are the Battery E names (certified in a separate documented run, fine), `Eztli Pilli` was scored `soft` in the strict-committed run but passed 5/5 at `C` in Battery D across all five seeds (defensible, though the upgrade is not recorded where it was applied), and **`pul / puul` is recorded as a Gate-1 pass with no decode in any result file in the repository**.

This is the most consequential traceability gap in the project and neither the audit nor the master catches it. The number carrying the entire null rejection cannot be rebuilt from the artifact the experiment log points at.

### O3. "Sentence probability intervals are invalid" overstates by half.

The audit is right that calling the independence product a "floor" is wrong, that the master contradicts itself two paragraphs later ("not even an absolute floor"), and that the correct Frechet lower bound is max(0, sum p_i - n + 1).

But the **ceiling is correct**. P(line) <= min_i P(token_i) is the Frechet upper bound and the master applies it properly. What fails is the lower end and, more fundamentally, the PPV inputs. The recommendation to delete all sentence-level percentages is still the right call, but for the input reason, not because the interval arithmetic is broken end to end.

## Part 3: three problems neither document found

### N1. The pseudo corpus is itself pseudoreplicated.

The 500 pseudo trials contain only **426 distinct strings**. 53 strings repeat across seeds: *ko'ja* appears 5 times, *noche*, *noch* and *fuks* 4 times each, *eztl* and *kori* 3 times each. The 4.6% floor is therefore measured on fewer independent draws than 500, and its confidence interval is narrower than reality. Every binomial p computed against that floor inherits the error.

Worse for the generator's stated guarantee that it rejects corpus words and long substrings: *eztl* is a four-character substring of the committed token *Eztli*, and *noche* is an ordinary Spanish word inside a palette that includes Spanish loans. Some of the "false positives" in the noise arm are not noise.

### N2. The PPV tier inversion has a traceable cause, and it is a wiring error.

The audit flags that `C` scores 77% against `H` at 75% on the neutral prior and calls it a warning sign. The cause is explicit in section 17.5: the `H` row uses Battery D rates (TPR 0.140 / FPR 0.046, likelihood ratio 3.04) while the `C` row uses Battery A rates (TPR 0.207 / FPR 0.062, likelihood ratio 3.34). The top tier is being scored with a weaker likelihood ratio than the tier beneath it. That is not an anomaly to note, it is a mis-specification: a tier that passes a *stricter* gate cannot be assigned the diagnostic characteristics of the gate as a whole and then compared against a looser tier scored on a different battery.

### N3. Gate 2 is structurally incapable of finding the competitors that matter.

`score_adversarial.py` classifies both the committed source and the adversary's language, then counts a competitor only when `acl != c["cclass"]`. Same-language competitors are filtered out by construction before any gloss comparison happens. Given that the F1 failures (*ek* wasp, *akal* quarrel) are same-language homophones, Gate 2 was blind to the exact failure mode Gate 1 was producing. The two gates share a hole rather than covering each other.

## Recommended action

The audit's remediation list is sound. Reordered by how much each fixes per unit of work:

1. **Repair repository integrity first.** It is mechanical, it is a stated non-negotiable in AGENTS.md, and everything downstream should be built from a reconciled tree. Re-apply the section 12.5 paragraph and the AGENTS.md tail to the mirror with targeted Edits, move the name-clash file out of the live tree, copy in the two missing files.
2. **Withdraw the sigma column, the sentence-level percentages, and the 10^-15 null-rejection claim.** Replace the last with the matched range, roughly p = 0.005 to 0.06 at the trial and item level, stated as marginal.
3. **Reconcile 23 versus 21 versus 26.** Record where every Gate-1 pass was decided, and either decode `pul / puul` or drop its pass.
4. **Normalize the lexicon population.** Give all 78 section 9 rows an H/C/S/O status with `L` as a tag only, then make the CSV, the prose, and the calculations agree on one denominator.
5. **Rescore Gate 1 against the predeclared root, language, and sense.** This is the deep fix. The existing result CSVs already carry the `root`, `lang`, and `gloss` columns, so the rescore is possible today without re-running a single decoder, and it will tell you immediately how many of the 25 hardened entries survive.
6. **Extend Gate 2 to same-language homophones and alternate segmentations.**
7. **Rebuild the null as a full-pipeline simulation**, and de-duplicate the pseudo corpus while doing it.
8. **Rescore the syntax control at the analyst level** and re-run with analysts blinded to the project's English glosses.

Item 5 is the one that decides how much of the project's headline survives, and it is cheap. It should go first among the analytical fixes.

## What is not in dispute

The audit's positive assessment is also correct and worth keeping in view. The exact Nahuatl names, the transparent Spanish loans, and the direct Maya forms (*k'áak'*, *máax*, *náach*, *che'*, *ki'*, *ti'*, *u-*) are strong independent evidence that the developers drew on real Mesoamerican lexical material. The project's practice of preserving alternates, running blind decoders against seeded noise, and publishing its own adversarial critique is more rigorous than the field norm. What fails is the inferential layer built on top of it, not the underlying observation.
