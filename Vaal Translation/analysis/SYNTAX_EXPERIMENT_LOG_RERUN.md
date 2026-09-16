# Syntax experiment log (re-run epoch)

This file is the placeholder required by `EXPERIMENT_RERUN_PROTOCOL.md`. It is **not** a completed panel and it does not contain p-values.

The 2026-07 panel in `SYNTAX_EXPERIMENT_LOG.md` remains the historical record. That panel gave analysts surface lines, English translations, and a token glossary. The published rule-level Fisher (12/12 vs 0/8) is withdrawn as a significance claim. The analyst-level table from those files is 3/3 vs 0/2, Fisher p = 0.10.

## Why this cell is still pending

The re-run protocol requires a **gloss-blind** panel: analysts receive surface lines and a form-only token list (orthography, no project English glosses, no section 3 conclusions). Isolation still applies: derive grammar from Vaal distribution, never from palette grammar. Scoring unit is analyst by corpus, not analyst by rule.

No such panel was run in this epoch. Inventing analyst sheets or a Fisher table would fake results.

## Pending checklist

- [ ] Gloss-blind real panel (target: at least 3 analysts).
- [ ] Gloss-blind scrambled panel (target: at least 2 analysts, preferably matched N). Document the scramble seed; 1729 is the archived control seed.
- [ ] Analyst-level 2x2 and Fisher p. Do not publish a rule-level table as the p-value.
- [ ] Per-conclusion confirm / partial / refute from surface strings alone.
- [ ] Sentence-level probability bands remain **withdrawn as translation confidence** until recovery-scored token PPVs exist; even then report Frechet bounds correctly (lower = max(0, sum p_i - n + 1), upper = min p_i). Do not call an independence product a floor.

Until the boxes above are ticked, quote qualitative reproducibility from the historical log if needed, and do not attach a new significance claim to syntax.
