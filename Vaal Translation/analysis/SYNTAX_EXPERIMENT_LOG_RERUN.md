# Syntax experiment log (re-run epoch, gloss-blind)

Protocol: `SYNTAX_CONFIRMATION_PROTOCOL.md`, `EXPERIMENT_RERUN_PROTOCOL.md` (Syntax panel). Date: 2026-09-16. This file replaces the pending stub. It is the current syntax panel. The 2026-07 log (`SYNTAX_EXPERIMENT_LOG.md`) remains history and is **not gloss-blind**.

## What was run

| Run | Design | Analysts | Inputs | Blind to |
|---|---|---|---|---|
| SYN-R1 | independent grammar derivation, gloss-blind | 3 isolated agents (A, B, C) | 51 numbered surface lines; form-only token list; isolation brief | project English translations, master §3 / §9 / §17, `committed_readings.csv`, other sheets, historical SYN-1 answers |
| SYN-R2 | same questions on scrambled corpus | 2 isolated agents (D, E) | same lines with words shuffled within each line (seed 1729); same token list and brief | the fact of scrambling, plus everything A-C were blind to |

Analysts were separate processes. Each process was allowed to open only copies of the three packet files. They were not given §3 conclusions, §9 readings, or English glosses.

Models (for audit, not a quality ranking): A `gpt-5.6-sol-high`; B `claude-sonnet-5-thinking-high`; C `gemini-3.8-flash-high`; D `composer-2.5`; E `gpt-5.6-terra-high`.

Raw sheets: `syntax_rerun_analyst_A_real.md`, `syntax_rerun_analyst_B_real.md`, `syntax_rerun_analyst_C_real.md`, `syntax_rerun_analyst_D_scrambled.md`, `syntax_rerun_analyst_E_scrambled.md`.

## Packets

Built by `syntax_rerun_build_packets.py` from canonical `Vaal Translation/Vaal_Reconstruction.md`.

- Closed corpus (master §3.2 / §17.5 count): Texts 1-4 plus Kamasan Smith = **51 lines, 186 whitespace tokens**. Ahuatotli and Mektul skill-cries excluded (not weighted). Soft-parse asterisks stripped. Speaker names and English cells not copied.
- Real packet: `syntax_rerun_corpus_real.txt` (numbered surface lines only).
- Form-only token list: `syntax_rerun_tokens_form_only.csv` (form key, attested spellings, count). No gloss column, no language, no §3 / §9 readings.
- Scrambled packet: `syntax_rerun_corpus_scrambled_s1729.txt`.
- Shared brief: `syntax_rerun_brief.md` (isolation rule and the seven questions). No §3 answers.

**Scramble procedure (reproducible).** Python 3 `random.Random(1729)`. For each numbered line in corpus order: split on whitespace; `shuffle` the token list in place; rejoin with a single space. Punctuation stays attached to the token it belonged to. Single-token lines are unchanged. Seed 1729 is the archived SYN-2 control seed. Re-run: `python3 syntax_rerun_build_packets.py`.

Packet scan: no English glosses in the line list or token CSV. Header comments on the tracked real file mention "No English translations" as a negative; analyst copies used comment-free numbered lines.

## Seven questions

Same as the protocol: (1) clause-type marking; (2) NP order; (3) possession order; (4) verb-object; (5) copula; (6) affix position; (7) undetermined items. Line-number evidence and high/medium/low confidence required for 1-6.

## Scoring (done after all five sheets existed)

Six testable §3 conclusions:

1. Clause type is set by a clause-initial particle.
2. Article, possessive, and attributive modifier precede the noun.
3. The possessed precedes the possessor.
4. Verb precedes object.
5. Equational clauses take no copula (juxtaposition).
6. Grammatical operators are proclitic (front); lexical derivation is suffixed (back).

Marks: confirm / partial / refute / undetermined. Scoring used the sheets only. (5) and (6) are order-independent: they may survive scramble and are not counted as linear-syntax evidence.

| # | §3 conclusion | A (real) | B (real) | C (real) | D (scrambled) | E (scrambled) |
|---|---|---|---|---|---|---|
| 1 | Clause-initial type particle | partial (Máax initial for questions; other type markers left undetermined) | partial (Máax initial for questions; Otsuks / 'Ayok not confirmed as type) | confirm (initial Máax, A'te, Ti, Xi, Aiokmo) | refute (mixed positions, not a uniform initial marker) | undetermined (restricted a'tul-final question association; no general marker) |
| 2 | Article / possessive / modifier precede noun | partial (`le` before noun-like; possessive and modifier undetermined) | partial (`le` prenominal; possessive / modifier undetermined) | partial (article and possessive prenominal; modifier undetermined) | undetermined (low-confidence tentative Det/Mod-before-N plus a postposed counterexample) | undetermined |
| 3 | Possessed precedes possessor | undetermined | undetermined | confirm (medium-to-high; line 27 `u mujuk' le mucane` as the clean pair) | undetermined (one low-confidence opposite reading) | undetermined |
| 4 | Verb precedes object | partial (predicate-like before complement-like on the `tlayeb` frame, not the `Xi daka puxe` clause) | partial (head-before-complement on `A'te` / `U'te`; verb vs presentative not independently shown) | confirm (medium; VO on several frames) | undetermined | undetermined |
| 5 | No copula (juxtaposition) | confirm (medium; no invariant intervening copula; equational label low) | undetermined | confirm (high) | refute (treated `ka` / `ti` as an overt linker frame in some strings) | undetermined |
| 6 | Operators front, derivation back | partial (front and back pieces; no operator-vs-derivation split) | partial (front and back pieces; split not stated) | partial (both edges attested; split not stated as operators vs derivation) | partial (front-bound pieces; suffixation undetermined) | undetermined |

Notes:

- Analyst C used a "third-person / possessive" label for `u`. That person feature is not licensed by the form-only packet. The positional claim (prenominal `u`, possessed-before-possessor) is what was scored.
- Without English, A and B did not recover the full five-opener clause-type system. C did. Possession (conclusion 3) is **not** reproduced by the panel: 1 confirm, 2 undetermined on the real side.
- Hypothesis check: word-order recovery is weaker than SYN-1 as a qualitative match to §3. That is the acceptable outcome. Honest undetermined was preferred over forcing §3.

## Analyst-level 2x2 (the experimental unit)

Predeclared recovery rule, applied after the sheets existed: an analyst recovered **consistent word-order regularities** if they reported, at medium or high confidence, a consistent linear order (not mixed, not undetermined) for **at least two** of questions 1-4.

| Analyst | Corpus | Recovered consistent word-order regularities? |
|---|---|---|
| A | real | yes (Q1 high initial Máax; Q2 medium prenominal `le`; Q4 medium predicate-before-complement) |
| B | real | yes (Q1 high; Q2 medium; Q4 medium head-before-complement) |
| C | real | yes (Q1 high; Q2 medium; Q3 high; Q4 medium) |
| D | scrambled | no (Q1 mixed; Q2 low / mixed; Q3 low; Q4 undetermined) |
| E | scrambled | no (Q1-Q4 undetermined) |

2x2:

|  | recovered | not recovered |
|---|---:|---:|
| real | 3 | 0 |
| scrambled | 0 | 2 |

Fisher exact, one-sided greater (`null_honesty.fisher_greater(3, 0, 0, 2)`): **p = 0.10**. Not significant. N = 5 analysts. Small N is the design, not a defect to paper over.

Do **not** publish a rule-level 12/12 vs 0/8 (or any 3x4 vs 2x4 recount) as the significance claim. Those cells are correlated within analyst.

## Specificity

Word-order conclusions (1-4) require recovery on the real corpus **and** "no consistent order" / undetermined on the scrambled corpus.

At analyst level that dissociation holds: 3/3 real vs 0/2 scrambled. Qualitatively, scrambled analysts did not reconstruct a uniform initial-type, prenominal-NP, possessed-before-possessor, VO grammar. D imposed mixed / low-confidence fragments; E declined almost every order claim.

(5) no copula and (6) affix shape are order-independent. In this gloss-blind panel they did **not** survive scramble as a clean positive finding (D treated `ka`/`ti` as a copula; E left both undetermined). They are not evidence of linear syntax. Do not count them in the 2x2.

## Against chance / honest limit

The 2026-07 coin-flip products are not reused. Analysts shared one corpus (real or scrambled) and one form-only inventory, so they are not independent coin flips. The inferential claim is the analyst-level Fisher above. Shared corpus still measures reproducibility of a reading from the data, not designer intent.

Wilson intervals on 18/18 from SYN-1 are historical. This panel is not 18/18.

## Historical SYN-1 / SYN-2 (not gloss-blind)

2026-07 analysts received surface lines **plus English translations and a token glossary**. Analyst-level table from those files: **3/3 vs 0/2, Fisher p = 0.10**. Rule-level 12/12 vs 0/8 (p about 7.9 x 10^-6) is withdrawn as a significance claim (pseudoreplication). Label: historical / not gloss-blind. Full writeup: `SYNTAX_EXPERIMENT_LOG.md`.

The gloss-blind 2x2 landed on the same counts and the same p. That is not a reason to treat SYN-1 as gloss-blind, and it is not a reason to call p = 0.10 significant. The qualitative match to the six §3 conclusions is weaker without English.

## Sentence-level probability bands

Remain **withdrawn as translation confidence**. Recovery-scored token PPVs are not in use as translation confidence. Frechet lower bound, if ever quoted, is max(0, sum p_i - n + 1); upper is min p_i. Do not call an independence product a floor.

## Reproduce / resume

```
python3 syntax_rerun_build_packets.py
```

Re-issue `syntax_rerun_brief.md` plus `syntax_rerun_corpus_real.txt` (or the scrambled file, unnamed as scrambled) plus `syntax_rerun_tokens_form_only.csv` to fresh isolated agents. Score against the six conclusions only after sheets exist. Analyst-level 2x2; Fisher one-sided. More analysts would tighten p; they would not turn this N=5 table into a large-N claim.
