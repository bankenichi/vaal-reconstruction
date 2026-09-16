# Full project audit: Vaal Reconstruction

Date: 2026-08-18

Scope: canonical master, mirror and downstream copies, source extracts, all analysis protocols, Python scorers, CSV worksheets and results, lexicon classifications, syntax experiment records, and the published PDF.

## Executive verdict

Overall assessment: **Needs revision before the statistical claims or sentence translations are presented as validated.**

The project is unusually careful for a fan reconstruction. It preserves alternates, distinguishes soft readings, retains source dictionaries, uses blind decoders, generates fixed-seed pseudo-data, and openly states that developer intent cannot be recovered. Those are real strengths.

The central statistical conclusion does not survive audit, however. The tests score whether a surface string receives any acceptable dictionary match. They do not score whether the decoder recovered the project's proposed root, source language, or meaning. The null comparison is also applied after the real lexicon has been selected for matchability, while the quoted 4.6% pseudo floor is unconditional. On the closest selection-matched comparison available in the project's own files, the reported p-value changes from about 10^-15 to a nonsignificant Fisher exact p of about 0.197.

The translation is therefore not statistically verified. Some individual borrowings and roots are strong, especially exact Nahuatl names, transparent Spanish loans, and several direct Maya forms. Most complete English sentences contain semantic expansions, supplied grammatical relations, unresolved morphology, or soft tokens. They should be presented as interpretive reconstructions, not translations with calibrated probabilities.

## Confidence assessment

| Area | Assessment | Confidence in this audit |
|---|---|---|
| Raw count arithmetic in Batteries A-D | Mostly correct | High |
| Published significance and PPV interpretation | Invalid for the stated translation-correctness question | High |
| Sentence probability intervals | Invalid | High |
| Syntax statistics | Pseudoreplicated and based on the wrong chance model | High |
| Exact lexical borrowings and famous names | Often strong | High |
| Full sentence translations | Mostly speculative or underdetermined | High |
| Intended developer meaning | Not verifiable from current evidence | High |
| PDF rendering | Visually sound in the inspected pages | High |
| Repository copy integrity | Not compliant with the project's own protocol | High |

## Critical findings

### 1. The scorer ignores the proposed root and gloss

Severity: Critical

`analysis/score.py` reads only the decoder's confidence and found flag. The proposed root, source language, and gloss columns are never compared with the project's answer. A real token is counted as a true positive whenever the decoder labels any match `C`.

This produces hardened passes that do not validate the published reading:

| Token | Published reading | Strict decoder's accepted match |
|---|---|---|
| `akal` | still or eternal waters | Yucatec `akal`, quarrel or scold |
| `ek` | star or dark | Yucatec `ek`, a large wasp |
| `tul` | wane or decline | K'iche' `tul`, reed or bullrush |
| `uch'` | drink or crush | K'iche' `uch'`, opossum |
| `xi` | Nahuatl imperative, do or make | Yucatec `xi'`, go |

The local Cordemex extract supports `ak'al` for lagoon or marsh, with a glottal, but the strict blind result did not recover that reading. Cordemex also supplies distinct same-language senses around `ek` and does not support `tul` as decline. Christenson directly lists K'iche' `tul` as reed and `uch'` as opossum. These examples demonstrate that form matchability is not gloss recovery.

Impact: Gate 1 does not establish the correctness of a root or translation. Every PPV and sentence-level probability derived from that gate is answering the wrong question.

Required correction: score exact recovery of a predeclared root, source language, segmentation, and semantic class. Define acceptable synonyms before decoding. A different homophone must count as a failure for translation validation.

### 2. The null floor is not conditioned on lexicon selection

Severity: Critical

The real 62-token set consists of entries already committed after loose dictionary search. The quoted Battery D floor, 23 of 500 or 4.6%, is measured over all pseudo strings without first requiring them to pass the loose commitment stage.

The same pseudo items appear in Batteries A and D, so the existing files permit a selection-matched check:

| Quantity | Result |
|---|---|
| Unconditional strict pseudo pass | 23/500 = 4.6% |
| Loose-committed pseudo items | 31/500 |
| Strict pass among loose-committed pseudo items | 8/31 = 25.8% |
| Strict pass in the selected real lexicon | 23/62 = 37.1% |

Comparing 23/62 with 8/31 gives a one-sided Fisher exact p of approximately **0.197**. The project's binomial p of about 2 x 10^-15 treats the unconditional 4.6% as fixed and ignores the discovery-stage selection that created the real lexicon.

Impact: the claimed overwhelming rejection of the all-noise null is not supported by the experiment as designed.

Required correction: run the complete discovery and commitment pipeline on each pseudo corpus, then apply the strict and adversarial gates only to pseudo entries that were committed. Use the full pipeline's final false-positive rate as the null.

### 3. The positive class is not a gold standard

Severity: Critical

The 30 `REAL_COMMITTED` items are the project's own disputed readings. Calling them genuine positives assumes what the experiment is supposed to test. They are also hard-coded rather than sampled, and the same 30 items are repeated across five seeds. The reported `n = 150` is 30 items judged five times, not 150 independent positive tokens.

The positive controls can measure whether fresh decoders also find some root for preselected real strings. They cannot estimate sensitivity for true etymologies because true etymology is unknown.

Impact: the TPR values are not sensitivities for correct translations, Wilson intervals using `n = 150` are too narrow, and the Bayes PPV calculation has no valid TPR input.

Required correction: use externally indisputable positives, such as exact attested names and transparent loans, and report them separately from uncertain corpus readings. Treat item and decoder as crossed random effects, or use a prespecified item-level aggregation.

### 4. The PPV table does not estimate translation correctness

Severity: Critical

The published PPV formula is algebraically correct, but its inputs are not. TPR distinguishes selected real Vaal surfaces from generated pseudo surfaces, not correct roots from incorrect roots. The base rate `b` is proxied by a proper-name roster decoded with the same method and is therefore circular. Proper names are also not representative of ordinary liturgical tokens.

Internal warning signs include:

- The supposedly lower `C` tier receives a higher PPV than the top `H` tier at the neutral prior, 77% versus 75%.
- `C*` confidence is obtained by approximately halving the `C` value, without an empirical model for the competitor.
- The 58% base-rate proxy includes soft readings, excludes four names after classifying them as out of palette, and transfers a name rate to general tokens.

Impact: the published 43% to 90%, 75% to 81%, and related confidence statements should not be used.

Required correction: remove translation-correctness PPVs until an exact-root and exact-semantic validation set exists.

### 5. Section 9 has 78 rows, while the statistical dataset has 65

Severity: High

The combined lexicon table contains 78 data rows. `token_classification.csv` contains 65. Thirteen table entries are marked `L` alone:

`chikula'`, `Gyan'uks`, `kíimil`, `ko'janti`, `kux/kuxkal/kuxte'`, `le/le'`, `líimek`, `Ma'oxe`, `Tlaxye'`, `Tzokan'te/tzok`, `Xatlene`, `yax/Yaxe`, and `yuquia`.

The project defines `L` as orthogonal and says it must combine with `H` or `C`. These 13 entries violate that taxonomy, remain outside all reported denominators, and are nevertheless used throughout the translations.

Impact: the claim that 25 of 65 covers the committed lexicon is not consistent with the table readers actually use. Counting all 78 rows would make the raw hardened share at most 25/78 = 32.1%, before correcting erroneous hardening passes.

Required correction: assign every section 9 entry an `H`, `C`, `S`, or `O` status, with `L` only as an added tag. Use one explicit population definition in the table, CSV, prose, and calculations.

### 6. Several hardened entries violate the written hardening protocol

Severity: High

Gate 1 requires the proposed root and same-language affixes to account for every segment. Gate 2 searches only a different language. This misses same-language homophones and allows the following problems:

- `k'ux (quxzeh)` is hardened even though `-zeh` is explicitly called a non-morphemic soft tail. The strict rules prohibit unexplained residue.
- `uch'` is hardened despite two incompatible published readings, Yucatec drink and crush, while the strict decoder accepted K'iche' opossum.
- `ek` is hardened even though the selected star or dark sense competes with other Maya homophones, including the blind-decoder wasp match.
- `ma` combines Maya negation and Nahuatl optative under one hardened entry.
- `xi` is hardened under a strict match from a different language and meaning than the lexicon's claimed reading.
- `tul` is hardened from a K'iche' reed match while the lexicon claims Yucatec decline.

Required correction: Gate 2 must include same-language homophones and competing segmentations. Gate 1 must validate the claimed analysis, not any root, and must reject unexplained surface material.

### 7. Sentence probability intervals are not probability bounds

Severity: Critical

The report calls the independence product a floor, then acknowledges that it is not an absolute floor. Both statements cannot be true. Without a justified dependence model, for token probabilities `p_i` the general Frechet lower bound is `max(0, sum(p_i) - n + 1)`, while the upper bound is `min(p_i)`. The product is a point estimate only under independence.

The assertion that real language creates positive dependence and therefore places truth between the product and minimum is unsupported. Repeated words, shared roots, shared correspondence rules, and a common analyst create complex dependence. Some errors can be negatively associated.

Additional problems:

- The Kamasan example assigns a `C*` probability to `yan`, which is absent from `token_classification.csv`.
- The line repeats lexical hypotheses but sometimes multiplies repeated tokens as independent events.
- The C-star value is an arbitrary halving, not a measured probability.
- Token PPVs are probabilities of matchability under the current model, not probabilities that the English gloss is correct.

Required correction: remove all sentence-level percentages. Replace them with a qualitative weakest-link statement and a literal morpheme-by-morpheme uncertainty table.

### 8. Syntax significance uses pseudoreplication and the wrong null

Severity: High

The syntax panel used three fresh agents on the real corpus and two on one scrambled corpus. The published Fisher table treats four correlated conclusions per agent as independent observations, yielding 12/12 versus 0/8. The experimental unit is analyst by corpus, not analyst by conclusion.

The chance calculation also says that three analysts agreeing on one unspecified binary value has probability `(1/2)^3 = 0.125`. If agreement on either value counts, the probability is `2 x (1/2)^3 = 0.25`. More importantly, analysts were not random coin flippers. They received the project-generated English translations and token glossary, so their answers are expected to be correlated.

The raw Fisher p of about 7.9 x 10^-6 is arithmetically correct for the 12-by-8 table, but the table's cells are not independent trials. The negative control shows qualitatively that agents can see the order regularities that the supplied alignment presents. It does not validate the English translations or designer intent.

Required correction: use multiple independently scrambled corpora, cross analysts across real and scrambled conditions, score at the analyst-corpus level, and blind analysts to project-generated glosses when testing surface order.

## Statistical reproduction

### Raw pooled counts

The published A-D rates reproduce from the CSV files:

| Battery | Pseudo C | Real C | FPR | Reported TPR |
|---|---:|---:|---:|---:|
| A, loose offline | 31/500 | 31/150 | 0.062 | 0.207 |
| B, loose online | 40/500 | 26/150 | 0.080 | 0.173 |
| C, strict offline | 17/500 | 19/150 | 0.034 | 0.127 |
| D, strict online | 23/500 | 21/150 | 0.046 | 0.140 |

The count arithmetic is correct. The interpretation is not, for the reasons above.

### Uncertainty and replication

- The same 30 positive items are used in all five seed runs.
- Each condition uses fresh decoders, so the claimed 2 x 2 effect is confounded with decoder differences.
- Wilson intervals pool rater-token judgments as independent Bernoulli trials.
- The strict full-lexicon test treats related roots, shared rules, and a common selection process as independent. Collapsing seven obvious root families does not remove all dependence.
- Battery E observed 10 strict pseudo passes among 60 distractors, 16.7%, but reuses the older 4.6% floor. The target names are exact, famous lexemes selected after inspection and are much easier than ordinary tokens.

### Sigma labels are numerically wrong

The exact binomial p-values are approximately reproducible under the project's invalid fixed-floor model, but the quoted sigma equivalents use a normal z-score of the count rather than the normal-tail equivalent of the p-value.

| Published p | Quoted sigma | One-sided normal-tail equivalent |
|---:|---:|---:|
| 2 x 10^-15 | 12.2 | about 7.85 |
| 4 x 10^-16 | 12.8 | about 8.05 |
| 3 x 10^-18 | 13.6 | about 8.63 |
| 5 x 10^-19 | 14.3 | about 8.84 |

These labels should be removed even if the original null model were retained.

## Translation audit

### What can and cannot be verified

There is no official bilingual Vaal source, developer grammar, or published design document in the repository. Correct intended translation is therefore not directly observable. The auditable questions are narrower:

1. Is the proposed source root attested?
2. Does the surface form follow predeclared correspondences?
3. Does the cited root carry the published literal sense?
4. Does the proposed morphology supply the grammatical relations in the English line?
5. Are additions from lore clearly separated from literal translation?

On those tests, the project has a strong group of individual roots but weak sentence-level fidelity.

### Strongest lexical material

The best-supported material consists of exact or near-exact lexical borrowings:

- Nahuatl `Quecholli`, `Panquetzaliztli`, and `Eztli Pilli`.
- Maya `k'áak'` fire, `máax` who, `náach` far, `ti'` relational, `u-` possessive, `che'` wood, and `ki'` sweet.
- Spanish `xefe/jefe` chief and transparent Romance-looking material.
- The fact that several PoE names and item names are real Nahuatl or Maya forms is genuine and relevant evidence for Mesoamerican sourcing.

Even here, exact lexical sourcing does not establish the surrounding English sentence.

### High-risk lexical material

| Entry | Audit finding |
|---|---|
| `kilya` | Attested material points to green or become green. `undying` is a lore-driven semantic chain, and the line has no explicit `as` marker. |
| `ikba'yucane` | The cited segmentation does not transparently yield `undying breath`. |
| `'Ibil` | `il` plus `-bil` yields a seen or visible form, not independently `flesh laid bare`. |
| `Gyan'uks` | `yancuic` can support `new`; `children` and possession are supplied by context. |
| `kifba` | Blood plus self does not independently establish `heart`. |
| `Yutsal/yutsal` | `goodness` is supportable; `good place`, the city Utzaal, and capitalization-based semantic switching add interpretation. |
| `Atziri` | The `atl + -tzin` proposal leaves major form changes and does not translate `queen`. |
| `jare'` | Christenson supports K'iche' `are'` as a focus pronoun and `ri` as an article. The published connective `and so` is interpretive. |
| `tul` | Local sources do not support `wane`; the strict pass used K'iche' `reed`. |
| `uch'` | Drink, crush, and opossum analyses compete. A unique literal sense is not established. |
| `Ixchel` | Reuse of the attested theonym is secure. The exact decomposition as `Lady Rainbow` is debated and should not be stated as certain. |

External cross-checks reinforce two points. The University of Oregon's [Online Nahuatl Dictionary entry for `xi-`](https://nahuatl.wired-humanities.org/content/xi) defines it as an optative or imperative command marker replacing second-person subject prefixes, not a free verb meaning `do` or `make`. Traci Ardren's peer-reviewed [study of Ixchel scholarship](https://www.osea-cite.org/class/readings/Ardren_Ixchel_Goddess.pdf) quotes a 1579 account in which local informants could not explain what the name meant and documents later scholarly conflations, so the name's reuse is much firmer than the project's exact decomposition.

### Line-level fidelity

Rating key:

- **Plausible**: major content roots roughly support the line, but grammar or idiom is still reconstructed.
- **Speculative**: at least one essential word, relation, or semantic step is unsupported or soft.
- No complete line qualifies as independently verified, because intended meaning is unavailable.

#### Text 1, Atziri Chant

| Line | Rating | Main issue |
|---:|---|---|
| 1 | Plausible | `ek` sense is ambiguous and `te` has a competitor. |
| 2 | Speculative | `Teoyuxtlane` is constructed, and `ascensionada/ascenada` is not a clean standard Spanish form. |
| 3 | Speculative | `kilya` supports green or become green, not directly undying; `as` is absent. |
| 4 | Speculative | `itsok` has a strong competitor; possessors, objects, and `us` are supplied. |
| 5 | Speculative | The morphology does not transparently produce `undying breath`. |
| 6 | Speculative | `flesh laid bare` and locative `in` are inferred; `kutsen` is weak. |
| 7 | Speculative | Lagoon or pond is possible for `ak'al`, but `eternal` and `into` are absent. |
| 8 | Plausible core, embellished English | No more, burn, end, and go out are thematically coherent, but ash and embers are supplied. |

#### Text 2, Cuachic Vault Litany

| Pair | Rating | Main issue |
|---:|---|---|
| 1 | Speculative | Life/death pairing is possible, but the response adds people-of relations not overtly established. |
| 2 | Mixed | `essence` is plausible; `countless` depends on a loose `ma' + xok` reconstruction. |
| 3 | Speculative | `Xatlene` needs loose correspondence; `children` and `your` are not in `Gyan'uks`. |
| 4 | Mixed | Spirit is plausible; flesh is a semantic reinterpretation of a seen form. |
| 5 | Plausible | First sign and last spirit are among the cleaner compositional pairs, though several entries are L-only. |
| 6 | Speculative | Those in the earth and good place are contextual expansions from earth and goodness. |
| 7 | Plausible core | Dark plus offering and blood-self are possible, but locative and heart readings are supplied. |
| 8 | Speculative | Presentatives are contested and `yuquia` depends on loose sound change. |

#### Text 3, Commander barks

All complete English barks are **speculative**. Most lines contain tokens explicitly marked soft or open. The apparently cleaner lines still add grammatical and semantic material, including `now`, `in me`, `her house`, `heart beats`, `undying`, possession, and ritual-drink relations. These are coherent lore readings, not literal translations established by the cited morphemes.

#### Text 4, Drill Sergeant

All multiword English lines are **speculative**. `Máax` who and several repeated content roots are strong, but `Otsuks`, `ukto`, `a'tul`, `cheyel`, `quxzeh`, `Axba`, and `Kíibsa'` are soft or contain unresolved material. The line `Máax tlayeb mucane?`, answered `Atziri`, is a plausible question-answer pattern, but the exact `of the dark` relation is not overt.

#### Text 5, stray captures

- `Ti ek tala jare'yantul` is **speculative**. `tala` can relate to come, but `jare'` as `and so`, `yan` as a separately tiered committed token, and especially `tul` as wane are not established. The claim that every token is committed is false because `yan` is absent from the classification CSV.
- `Ti' ek'le upulche` is **speculative** because the full verb form and `-che` tail remain unresolved.
- The Ahuatotli and Mektul lists are appropriately framed as candidate roots rather than translations. They should remain outside claims about decoded sentences.

## Source and provenance audit

### Strengths

- Full local Cordemex and Christenson extracts permit direct checking.
- Many entries point to named dictionaries rather than unattributed web glosses.
- Alternates and open questions are preserved instead of silently deleted.
- Texts 1 and 2 cite datamined or database sources and are more traceable than later captures.

### Gaps

- No audio or screenshot files are stored in the repository, although audio is used as primary phonological evidence.
- Citation 37 and citation 44 describe footage but provide no file, URL, timestamp, or archive.
- Text 4 cites `[1]`, but citation 1 is the Commander page, not the Drill Sergeant source.
- The repository does not include the cited `NPCTextAudio.json` snapshot used to assert zero transcription drift.
- Several bibliography entries bundle many roots under one source without headword, page, edition, or quoted source-language context.
- Some committed claims rely on Wikipedia, Wiktionary, game wikis, or secondary summaries despite the declared primary-source rule.
- The exact meaning of `Ix Chel` is not certain in the specialist literature, so the confident `Chel = rainbow` decomposition is too strong.

Required correction: archive every audio clip, screenshot, data row, and game patch identifier used as evidence. Add a machine-readable evidence table with token, surface source, timestamp, proposed root, dictionary headword, page or entry URL, literal gloss, and transformation steps.

## Reproducibility and code audit

### What works

- Fixed seeds regenerate the pseudo strings and shuffled keys.
- Raw A-D worksheets and result CSVs are present.
- Pooled counts can be recomputed from the files.
- The generator rejects exact corpus words and obvious long substrings.
- The PDF build artifacts are present.

### What does not reproduce independently

- The lexical decoder prompts are not archived verbatim.
- Decoder provider, model, model version, temperature, and date are not recorded per result file.
- Many result rows leave root, language, and gloss blank, retaining only the classification.
- The 30 positive items are hard-coded and their selection rationale is not randomized or preregistered.
- Gate decisions after the initial runs are partly manual and do not have one executable derivation from raw files.
- There is no dependency lockfile or environment manifest for the Python and PDF pipelines.
- The workspace is not a Git repository, so claims of preregistration and historical ordering cannot be independently checked.

## Repository integrity audit

The project fails its own byte-identity rule.

- Canonical master: `Vaal Translation/Vaal_Reconstruction.md`.
- Parent copy: content-normalized identical to canonical, but missing the canonical final newline.
- Mirror master: contains a substantive older paragraph in section 12.5 and is missing the final newline.
- Mirror `AGENTS.md` is truncated in the final open-items sentence.
- Canonical has `analysis.7z` and `analysis/VERIFICATION_PASS_2026-07-06.md`, both absent from the mirror.
- Mirror contains an extra name-clash master document.
- Canonical has 101 files, mirror 100, with five detected path or content differences.

The published PDF copies are byte-identical to each other, SHA-256 `771E006AEA30B79278F16F76C3642DCABCCAADDBD49913A876C6AF83A104739D`.

Required correction: stop treating the current mirror as verified, reconcile the body divergence and truncated instructions, remove or archive name-clash files outside the live tree, and add a checked manifest of expected paths and hashes.

## PDF audit

The canonical PDF is 77 pages. The cover and statistical pages 63 through 68 were rendered and visually inspected. Tables are legible, typography is consistent, and no clipping or overlapping was observed. The three published PDF copies are identical.

Minor presentation issue: long code-style filenames wrap awkwardly in section 17. This is cosmetic.

The PDF accurately presents the project's current statistical claims, but those claims require substantive revision for the reasons above. Good rendering does not mitigate the inferential errors.

## What the statistical work is actually relevant to

The experiments retain limited exploratory value:

1. They show that permissive dictionary search can match a very large share of generated Vaal-like noise.
2. They show that tightening form rules sharply reduces match frequency.
3. They expose which proposed entries depend on loose transformations.
4. They demonstrate that famous exact names are easy for blind decoders to identify.
5. They provide a useful warning that a found root alone is weak evidence.

They do **not** establish:

- that a specific proposed root is the intended root;
- that the published English gloss is correct;
- that 75% to 81% of hardened readings are genuine;
- that complete lines have the reported probabilities;
- that the grammar reflects developer design;
- or that the all-noise hypothesis is rejected at 10^-15 after conditioning on how the lexicon was selected.

## Recommended remediation order

1. **Withdraw the PPV, sentence probability, sigma, and 10^-15 null-rejection claims.** Keep raw descriptive rates with a clear note that they measure matchability.
2. **Repair repository integrity.** Reconcile canonical, parent, mirror, instructions, and archive files before further analysis.
3. **Define the estimand.** Decide whether the test targets exact root recovery, broad source-language influence, literal gloss recovery, or sentence translation. Do not combine these outcomes.
4. **Rebuild the null as a full-pipeline simulation.** Run loose discovery, commitment, strict recovery of the same proposed root and sense, and adversarial testing on pseudo data.
5. **Use a real gold standard.** Separate indisputable exact borrowings from uncertain corpus tokens. Never label the disputed lexicon as known positives.
6. **Score exact analyses.** Require predeclared root, language, segmentation, complete surface accounting, and semantic class.
7. **Include same-language competitors.** Homophones and alternate segmentations are as important as cross-language competitors.
8. **Use crossed, recorded decoders.** Archive prompts and model metadata, randomize items, and account for item and decoder clustering.
9. **Normalize the lexicon population.** Resolve the 78 versus 65 discrepancy and eliminate L-only confidence entries.
10. **Replace fluent English with three layers.** Give a literal morpheme gloss, a minimally normalized translation, and a separate lore interpretation.
11. **Archive primary game evidence.** Store audio, screenshots, data rows, patch versions, timestamps, and checksums.
12. **Retest syntax without supplied project translations.** Use surface strings, independently verified token categories, multiple scrambles, and analyst-level inference.

## Bottom line

The project has credible evidence that Grinding Gear Games drew repeatedly from real Mesoamerican lexical material, especially in names and transparent borrowings. It does not currently have a valid statistical demonstration that the proposed sentence translations are correct or even that the selected committed lexicon beats a selection-matched noise pipeline. The strongest defensible product today is an annotated set of source hypotheses with explicit literal, semantic, and morphological uncertainty. Calling it a statistically verified translation overstates what the evidence can support.
