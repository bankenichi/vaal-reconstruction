# T-M translator brief

You are one independent translator (methodology on). Seed / slot: see the sheet filename.

## Isolation

Open only:

- this packet directory (`translation_battery_TM_packet/`)
- `dict_lookup.py` in `Vaal Translation/analysis/`
- dictionary files under `VAAL_DICT_DIR` or the hashed uploads (decode only)

Do not open: Vaal_Reconstruction.md, master section 9 or 17, committed_readings.csv, other translation_battery_T*.md/csv sheets, translation_battery_gold.csv, STATISTICAL_SUMMARY.md, NULL_MODEL_*, or any file that dumps published English of these lines.

## Inputs

- `corpus.txt`: 51 numbered surface lines. No English.
- `methodology.md`, `HARDENING_PROTOCOL.md`, `TIGHTENED_LATITUDE.md`
- `token_lookup_dump.csv`: form-first dictionary hits for corpus tokens (convenience; you may re-query `dict_lookup.py`)
- `worksheet_template.csv`: empty sheet with line_id and vaal only

## Task

Write a best-effort English translation of every numbered line.

Fields: line_id, translation, confidence (high / medium / low / abstain), notes.

Notes may list per-token root / lang / gloss when found. Prefer form-first lookup. Palette order: Yucatec, then Nahuatl, then K'iche', then Spanish, then Pipil/Nawat. Strict latitude first. Opaque stays opaque: abstain rather than force.

Tie-break among equally plausible hits with `random.Random(SEED).choice` after sorting by folded lemma length descending.

Formatting: no em dashes, middots, or emojis.

## Output

Write both:

- `Vaal Translation/analysis/translation_battery_TM_s{SEED}.csv`
- `Vaal Translation/analysis/translation_battery_TM_s{SEED}.md`

CSV header: `line_id,translation,confidence,notes`

The markdown file is the same table plus a one-line note naming the packet files you used. Translate all 51 lines. Do not score yourself against an external key.
