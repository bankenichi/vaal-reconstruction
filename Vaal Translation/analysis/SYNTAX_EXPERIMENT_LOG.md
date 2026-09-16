# Syntax confirmation experiment log

Evidence-based record of the blind confirmation of the master §3 syntactic analysis. Protocol: `SYNTAX_CONFIRMATION_PROTOCOL.md`. Statistics: master §17.8.

## What was run

| Run | Design | Analysts | Inputs | Blind to |
|---|---|---|---|---|
| SYN-1 | independent grammar derivation | 3 fresh general-purpose agents (A, B, C) | 33-line Vaal corpus (surface + English), token glossary, isolation rule | master §3, each other |

Date: 2026-07-02. Each analyst answered seven questions (clause-type marking; NP order; possession order; verb-object order; copula; affix position; undetermined items) with line-number evidence and self-assigned confidence. No analyst had file or tool access; the task was self-contained in the prompt.

## Headline results

All three analysts confirmed all six testable conclusions.

| # | §3 conclusion | A | B | C |
|---|---|---|---|---|
| 1 | Clause type set by a clause-initial particle | confirm (high) | confirm (high) | confirm (high) |
| 2 | Article / possessive / modifier precede the noun | confirm (high) | confirm (high) | confirm (high, with *tlayeb* caveat) |
| 3 | Possessed precedes possessor | confirm (high) | confirm (high) | confirm (high) |
| 4 | Verb precedes object | confirm (medium) | confirm (medium) | confirm (medium) |
| 5 | No copula (juxtaposition) | confirm (high) | confirm (high) | confirm (high) |
| 6 | Operators proclitic, derivation suffixed | confirm (high) | confirm (med-high) | confirm (high) |

- Confirmation rate: **18 / 18 = 100%**, Wilson 95% CI [82.4%, 100%]. Per conclusion 3/3, Wilson 95% CI [43.8%, 100%].
- All three flagged verb-object as the one medium-confidence claim (it rests on the single clean transitive clause *Xi daka puxe*), matching §3.
- All three independently reproduced the §3.7 open-questions set: the particles *ka* and *ti*, the *le le* doubling, and the segmentation of *jare'yantul*. Additional undetermined items each raised (*ko'*, *na'*, *pu*, *buxa*, *jare* category) are recorded but were not §3 conclusions.

## Refinement adopted

Analyst C observed that *tlayeb* "dark" may be a fronted locative ("in the dark") rather than a pure attributive in some lines (*tlayeb kutsen*, *Ela tlayeb ukto*). This does not change the word order (it remains pre-nominal) but leaves the adjective-versus-adverbial category open. Folded into master §3.4 and added to §3.7. Counted conservatively as a partial, the rate is 17/18 = 94.4%, Wilson 95% CI [74.2%, 99.0%].

## Against chance

Null: each analyst picks a word-order value at random. Unanimity of 3 analysts on one binary parameter = (1/2)^3 = 0.125; all six parameters unanimous = ~3.8 x 10^-6 (binary) or ~2.6 x 10^-9 (three-way). Observed agreement is far beyond coincidence.

## Honest limit

Shared corpus and glossary: this measures reproducibility of the §3 reading from the data, not independent attestation of designer intent (syntactic analogue of the base-rate limit, §17.7). Strengths within that limit: the conclusions are about surface position, largely independent of gloss correctness; the corpus is closed and fully examined.

## Negative control (SYN-2)

To test specificity (not just reproducibility), 2 further blind analysts were given a **scrambled** corpus: the same 33 lines and the same glossary, but with the words randomly reordered within each line (seed 1729), destroying word order while leaving vocabulary and morpheme shapes intact. They were not told the corpus was scrambled, and answered the same seven questions.

Result: the four word-order conclusions collapsed. Both analysts reported "undetermined / no consistent order" for (1) clause-initial type marking, (2) noun-phrase order, (3) possessed-before-possessor, and (4) verb-object, each of which the real corpus had returned at 3/3. The two order-independent conclusions held in both conditions: (5) no copula and (6) front-operator / back-suffix morphology, which is correct, since scrambling word order cannot affect a missing copula or within-word morpheme edges.

Dissociation: counting recovery of a consistent order rule, real = 12/12 (3 analysts x 4 rules), scrambled = 0/8 (2 analysts x 4 rules), Fisher exact p about 7.9 x 10^-6. This establishes that the §3 word-order rules are specific to the real corpus and not an artifact of analyst expectation. It also correctly demotes the copula and morpheme-edge findings, which are true but not evidence of linear syntax (they would survive in a bag of words).

Note on inter-rater kappa: on the SYN-1 panel all ratings were "confirm" (one category), so Fleiss kappa is 0/0 (undefined). The negative control is the specificity test in its place.

## Reproduce / resume

Re-issue the archived prompt (corpus + glossary + seven questions) to fresh blind agents; score against the six §3 conclusions; report confirmation rate + Wilson CI + chance baseline. More analysts tighten the intervals; more attested Vaal lines enable new conclusions.
