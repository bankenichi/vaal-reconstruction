# Adversarial critique and recommendations

> **Status note (added later).** This adversarial review predates the statistical and structural work it called for, and most of its central criticisms were subsequently acted on. It is kept here as the record that prompted that work. Where each critique was addressed: the missing base-rate / null model (3.1) became master §17 (null model, base rate b, PPV); the absence of regular sound correspondences (3.2) became the collected correspondence rules in §2.6 and their orthographic hardening in §17.9; post-hoc licensing and the cross-graft escape hatch (3.3, 3.4) are quantified by the strict-versus-loose latitude test (§17.3, `TIGHTENED_LATITUDE.md`); and compounding semantic latitude (3.6) is the sentence-level confidence interval (§17.5). The "creole" framing point (3.5) is acknowledged, not resolved. The critiques below therefore stand as written, but should be read alongside the sections that now answer them.


*An objective, adversarial assessment separating the craft (strong) from the epistemics (not yet sound). The tone is deliberately critical: the aim is to surface failures and realism, not reassurance.*

## 1. The framing issue that governs everything

The project decodes the Vaal strings as if they were produced by a real language-formation process (a "Mesoamerican creole"). The actual generative process is a games writer at GGG choosing syllables that sound Mesoamerican. These are not the same thing, and the gap between them is the whole problem.

Some tokens were almost certainly built from real roots: *Atziri*, the *-tlan* place-names, *teotl*, *Xibaqua*, anything carrying visible Nahuatl morphology. Others are very likely phonaesthetic filler with no root behind them. The method as it stands cannot distinguish the two classes, because it will find an attested root for the filler as well. That is not an execution flaw; it is a property of the target. Until provenance is addressed, every "committed" reading carries an unquantified prior that it may be decoding noise. This is the pareidolia trap that sinks Bible-code and amateur Voynich work: the discipline can be genuine while the object refuses to support it.

## 2. What is genuinely strong

- **Attestation discipline.** Requiring a primary-source root is real philological hygiene, far above the fan-linguistics norm.
- **Logging competing readings** instead of discarding them is epistemically honest and unusual.
- **The phoneme-as-source-diagnostic.** Loan-only /f/, /d/, /r/ and silent /g/ as source markers is the one part of the framework that behaves like real linguistics: it makes a falsifiable, system-level prediction rather than a per-word guess. The recent form-first correction strengthens this considerably.
- **Separating romanization artifacts from morphemes** (the *-uks / -s* coda) is a sophistication most reconstructions miss.

## 3. The substantive weaknesses

### 3.1 No base-rate / null model (the deepest problem)
There is no measurement of how often the pipeline finds an equally "good" root for a random Vaal-shaped string. Without that baseline, "attested root found" is close to zero evidence. This is now testable: see `NULL_MODEL_PROTOCOL.md` and `pseudo_vaal_test_set.txt`.

### 3.2 No regular sound correspondences
The comparative method rests on regular correspondences, and they are absent. *taal -> tul* (aa to u), *-tl -> -to*, metathesis for *Axba*, onset substitutions: each is invoked one token at a time, exactly when a token needs rescuing. A sound change is only evidence when it is a rule that applies everywhere its environment occurs. What the document has are stylizations, not sound laws, and stylizations can fit anything.

### 3.3 Post-hoc source-language licensing
K'iche' is admitted "only where the other two cannot account for a sound," which is precisely when it is needed. Spanish is summoned for /f/ and /d/, Xinkan/Nawat for edge cases. Enlarging the hypothesis space at the moment of difficulty guarantees success and drains any single fit of meaning.

### 3.4 The cross-graft escape hatch
Maya-root-plus-Nahuatl-affix splices (*qexcan*, *pochiti*, *Otsuks*) are typologically strong claims used as routine repair tools. That is a general-purpose rescue mechanism, and general-purpose rescue mechanisms fit almost any token. Each cross-graft should be a red flag demanding extra justification, not a normal move.

### 3.5 The "creole" claim is a category error
A creole has its own grammar: a tense-mood-aspect system, consistent word order, productive morphology. This analysis is almost entirely lexical; syntax is repeatedly "provisional," particles are "soft," no morphological system is reconstructed. What is actually present is a mixed or relexified lexicon, which is real and interesting but is not a creole. Either reconstruct the grammar or downgrade the claim to "lexical sourcing / phonaesthetic analysis."

### 3.6 Compounding semantic latitude
Chains like *green -> evergreen -> undying* (*kilya*) or *cluster -> company* (*Otsuks*) each add a degree of freedom, and these stack multiplicatively with the phonological freedoms. Using the game's English barks as ground truth is mildly circular: those glosses are the writer's intended meaning, possibly pinned to an arbitrary string, so "the reading matches the English" is not independent confirmation.

## 4. Recommendations, in priority order

1. **Build and run the null model first** (`NULL_MODEL_PROTOCOL.md`). Stop adding tokens until the false-positive rate is known. This single experiment is worth more than any amount of further token work.
2. **Write the sound-correspondence rules as a table and enforce them globally.** Partition the lexicon into "regular" versus "special pleading." The size of the second pile is the honest signal-to-noise estimate.
3. **Pre-commit the admissible source languages** and accept the false-positive cost of each, rather than summoning languages only when convenient.
4. **Establish provenance.** Hunt for GGG developer statements, datamined design comments, or dictionary-specific spelling artifacts. Even a partial answer splits the corpus into "plausibly designed" and "plausibly filler," which every confidence label should then respect.
5. **Reconstruct grammar or drop the creole framing.** Pick one.
6. **Run an adversarial pass.** For each committed reading, have a skeptic or a second model find an equally good root from a different language. Anything that falls is not committed. Recommended standing rule: no token is labeled committed until it has survived this pass.
7. **Replace binary committed/soft with a transparent score**: attestation strength times phonological regularity times semantic directness times number of independent cross-checks. It forces the hidden judgment calls into the open and makes the document auditable.

## 5. Verdict

As disciplined creative philology, reconstruction-as-craft, this is well above the norm: documented, self-critical, and now self-correcting. As evidentiary historical linguistics it is not yet there, and the two things standing in the way are the null model and regular sound correspondences, both currently absent. The blunt read: a meaningful fraction of the committed lexicon is probably real (the tokens GGG built from actual roots) and another meaningful fraction is confident decoding of noise, and the present method cannot report the ratio. The most valuable next move is not another token; it is the baseline that tells you which half of the work you are looking at.
