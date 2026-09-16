# Syntax confirmation protocol

The two-part test each syntactic conclusion in master §3 must pass before it is reported as confirmed. It mirrors the lexical hardening protocol (`HARDENING_PROTOCOL.md`): a claim is credible only if it is (1) derived in isolation from the corpus and (2) reproduced blind by independent analysts. Results live in `SYNTAX_EXPERIMENT_LOG.md`; the statistical treatment is master §17.8.

## 1. Isolation gate (how §3 is written in the first place)

Every grammatical claim is read from Vaal's own distribution: which element sits in which position, adjacent to what, and how consistently across the corpus. Palette grammar is never evidence. A token's committed gloss (§9) may label what a clause does; it may never license how the clause is built. This is the syntactic form of the form-first rule (AGENTS.md 2a).

## 2. Blind confirmation gate

- **Analysts.** 2 to 4 fresh agents, each with no access to §3 or to each other.
- **Inputs given.** Only: the closed Vaal corpus (surface lines + English translation), a token glossary (meanings only), and the isolation rule. Nothing about the expected answers.
- **Task.** Derive, with corpus line-number evidence and a self-assigned confidence (high/medium/low): clause-type marking and its position; noun-phrase order (article / possessive / modifier vs. noun); possessed-vs-possessor order; verb-object order; presence or absence of a copula; affix positioning (proclitic vs. suffix); and a list of elements whose function cannot be determined.
- **Scoring.** Each of the testable §3 conclusions is marked, per analyst, confirm / partial / refute. A conclusion is **confirmed** when it replicates across the panel with no refutation. Agreement is reported as the confirmation rate with a Wilson 95% interval, and against a chance baseline (random word-order choice per analyst: unanimity on one binary parameter has probability (1/2)^3 = 0.125).


## 2a. Specificity gate (negative control)

Reproducibility (2.) is necessary but not sufficient: analysts might impose a grammar on any word list. So the panel is also run on a **scrambled** corpus, the identical lines and glossary with words randomly reordered within each line (fixed seed), which destroys word order but preserves vocabulary and morpheme shapes. A word-order conclusion passes the specificity gate only if it is recovered on the real corpus and reported "no consistent order" on the scrambled corpus. Conclusions that survive scrambling (a missing copula, within-word morpheme edges) are not evidence of linear syntax and are marked as such. Report the real-versus-scrambled dissociation (e.g. Fisher exact on rule-recovery counts). Note: with unanimous confirmation on the real panel, Fleiss kappa degenerates to 0/0; the negative control replaces it.

## 3. Testable conclusions (the current six)

1. Clause type is set by a clause-initial particle (presentative, interrogative, imperative, privative, modal).
2. Article, possessive, and attributive modifier precede the noun.
3. The possessed precedes the possessor.
4. Verb precedes object.
5. Equational clauses take no copula (juxtaposition).
6. Grammatical operators are proclitic (front); lexical derivation is suffixed (back).

## 4. Honest limit

The panel shares one corpus and glossary, so confirmation measures reproducibility of the reading from the data, not independent proof of designer intent (the syntactic analogue of the lexical base-rate limit, §17.7). Conclusions about surface position are largely gloss-independent, which is a strength; the corpus is small (about two dozen clauses), which caps the precision and widens the intervals.

## 5. Reproduce / resume

Re-run by issuing the corpus + glossary + the seven questions in §2 to fresh blind agents (verbatim prompt archived in `SYNTAX_EXPERIMENT_LOG.md`). Score against the six conclusions in §3. Add analysts to tighten the intervals; add corpus lines (new attested Vaal) to test new conclusions.
