# T-M methodology packet (form-first / anti-forcing / palette)

This file is the methodology an independent translator may use, together with HARDENING_PROTOCOL.md and TIGHTENED_LATITUDE.md in this packet. It is stripped of finished English translations of the numbered corpus. Do not open the master document, section 9, committed_readings.csv, other sheets, or any gold key.

## What this language is treated as

A Mesoamerican-sourced constructed language. Tokens are resolved against attested dictionary roots. This is scholarship, not fan fiction. Opaque stays opaque.

## Source palette (search order)

Every token is resolved by searching candidate languages in this fixed priority:

1. Yucatec Maya (core layer, most content roots, articles, presentatives)
2. Classical Nahuatl (divinity, place-names, negation, several adjectives)
3. Highland Maya, K'iche' (thin seam, surfaces only where the first two cannot account for a sound, for example a surface /r/)
4. Romance, Spanish (loans for abstract and martial concepts)
5. Xinkan and Nahuan (Pipil/Nawat) as secondary candidate pools

## Hard rules

1. No em dashes, no middots, no emojis. Use commas, colons, parentheses, or regular hyphens.
2. **Anti-forcing.** Opaque tokens are reported as opaque. Never propose an etymology without an attested primary-source root that matches both form and semantics. Squinting until it fits is prohibited. Whole-line **abstain** is allowed.
2a. **Root search is form-first; never gloss-led.** Start from the surface form and its phonology. Enumerate attested roots that fit the form. Read off what those roots mean and follow where the best-attested, sensical ones lead. Do not search a dictionary for words that mean what you already wish the token meant.
2b. Confidence taxonomy (for your own notes, not a lexicon edit): **H** hardened (both gates in HARDENING_PROTOCOL.md), **C** attested but latitude-dependent, **S** soft candidate, **O** opaque. You are translating; you are not promoting tokens into a committed lexicon. You do not have a predeclared answer key. Use Gate 1 as a bar for trusting a hit: an attested root plus a same-language affix must account for the surface under TIGHTENED_LATITUDE.md, with no unexplained residue, if you mark a reading high-confidence.
3. Primary-source attestation required: Cordemex, Karttunen/Molina/Florentine-style Nahuatl lists, Christenson K'iche', Campbell Pipil/Nawat, Spanish-Maya wordlists as attached.
4. Competing readings are logged in notes, not silently discarded.
5. Distinguish romanization artifacts from morphology. A spelling tail such as a final -uks or -s is not automatically a morpheme.
6. Semantic field constrains the search. Use **surrounding attested tokens** to bound a choice among form-fitting roots. Do not constrain a token with an English translation you already assigned to that same token.
7. Do not invent citations or lore.

## Diagnostics (phonology, not translations)

- Word-initial Gua-/Gue- may signal Nahuatl cua-/cui- /kʷ/ (colonial Spanish orthography).
- Word-initial or loan-only /d/, /f/, /r/, /g/ flag a non-core source: /r/ points to K'iche', /f/ and /d/ to Spanish loans, silent /g/ to Nahuatl.
- Prefer `dict_lookup.py` over guessed roots. Try `--latitude strict` first; `--latitude loose` only if strict misses. `--access online` includes the attached Nahuatl 1100 wordlist.

## What you must not do

- Do not open Vaal_Reconstruction.md, section 9, section 17, committed_readings.csv, other translators' sheets, or translation_battery_gold.csv.
- Do not copy English from memory of Path of Exile subtitles or wikis. Translate from the surface and the dictionaries in front of you.
- Do not force a fluent English sentence when the line is opaque. Abstain.
