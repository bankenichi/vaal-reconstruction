# T-D translator brief

You are one independent translator (dictionaries only). Seed / slot: see the sheet filename.

## Isolation

Open only:

- this packet directory (`translation_battery_TD_packet/`)
- dictionary files under `VAAL_DICT_DIR` or the hashed uploads (decode only)
- optional: `dict_lookup.py` as a string-search helper over those dictionaries

Do not open: the T-M methodology packet, AGENTS.md, HARDENING_PROTOCOL.md, TIGHTENED_LATITUDE.md, Vaal_Reconstruction.md, master section 9 or 17, committed_readings.csv, other translation_battery_T*.md/csv sheets, translation_battery_gold.csv, STATISTICAL_SUMMARY.md, or any file that dumps published English of these lines.

You do not have a project search order, form-first rule set, or latitude protocol. Use the dictionaries as a bilingual resource.

## Inputs

- `corpus.txt`: 51 numbered surface lines. No English.
- `token_lookup_dump.csv`: dictionary strings that match corpus token spellings (convenience index; you may also grep the dictionary files)
- `worksheet_template.csv`: empty sheet with line_id and vaal only

## Task

Write a best-effort English translation of every numbered line, using the dictionaries.

Fields: line_id, translation, confidence (high / medium / low / abstain), notes.

Notes may list per-token root / lang / gloss when found. You may use any dictionary hit you judge useful, including Spanish. You may abstain when you cannot make a line.

Tie-break among equally plausible hits with `random.Random(SEED).choice` after sorting by folded lemma length descending.

Formatting: no em dashes, middots, or emojis.

## Output

Write both:

- `Vaal Translation/analysis/translation_battery_TD_s{SEED}.csv`
- `Vaal Translation/analysis/translation_battery_TD_s{SEED}.md`

CSV header: `line_id,translation,confidence,notes`

The markdown file is the same table plus a one-line note naming the packet files you used. Translate all 51 lines. Do not score yourself against an external key.
