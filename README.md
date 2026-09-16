# The Vaal Tongue

Welcome. This is a fan reconstruction of the **Vaal language** from *Path of Exile* and *Path of Exile 2*. It treats in-game Vaal as a Mesoamerican-sourced constructed language: a **Yucatec Maya** core, a **Classical Nahuatl** layer, a thin **K'iche'** seam, and **Spanish** loans. The project reverse-engineers the spoken and written Vaal corpus into attested dictionary roots, writes down every competing reading, and then tests those readings instead of asserting them.

If you play PoE and have an ear for languages, or if you work with Mesoamerican languages and are curious how a game corpus behaves under the same discipline, you can read this cold. The typeset PDF is the intended first page.

## Where to start

1. **Read the PDF:** [`The_Vaal_Tongue.pdf`](The_Vaal_Tongue.pdf) at this repository root. Copies also live in [`Vaal Translation/build/`](Vaal%20Translation/build/) and [`PDF Building/`](PDF%20Building/).
2. **Then the master Markdown**, if you want to search, quote, or follow citations: the canonical file is [`Vaal Translation/Vaal_Reconstruction.md`](Vaal%20Translation/Vaal_Reconstruction.md). The repository-root [`Vaal_Reconstruction.md`](Vaal_Reconstruction.md) is a sync copy of that same document, kept byte-identical. Do not treat the two as independent drafts.

The reconstruction covers five Vaal texts (the Atziri Chant, the Cuachic Vault Litany, the Commander's temple barks, the Drill Sergeant catechism, and stray captures), a combined lexicon, a grammar read from Vaal's own word order, and the statistical checks in master §17.

## Honest current standing

The Vaal lines on the page are stable. The English translations and word-by-word readings are hypotheses with thin measured support. The table below is live post-blocker standing from the master Overview and §17. It does not inflate. An older "not random noise at 10^-15" display is withdrawn; it is historical only (master §17.10), not current canon.

Where a result is a range, three readings are given for **that same metric**: **pessimistic** is the lower 95% bound (or a stricter counting rule), **average** is the point estimate, **optimistic** is the upper 95% bound (or a looser counting rule). When two independent-translation arms exist, both are shown (method-notes / dictionaries-only). Chance tests and the grammar panel are yes/no small-sample tests, not three invented shares.

| Check | Pessimistic | Average | Optimistic |
|---|---|---|---|
| Hardened share of the 78-word lexicon | 0.7% | 2 of 78 = 2.6% (*xefe*, *Quecholli*) | 8.9% |
| Chance test, lookup must recover the declared sense | fails to reject noise (p = 1 / 0.9991) | any dictionary hit still not significant at 0.05 (p = 0.09494 / 0.3069) | even the more generous any-hit reading fails to reject chance |
| Independent translation vs published English, match or partial | 24.2% / 23.1% | about 29% both arms (29.4% / 28.2%) | 35.3% / 34.1% |
| Published lines graded fully secure | 0.0% | 0 of 51 | 7.0% |
| Grammar recovered without this project's English (real lines vs scrambled) | not significant | 3 of 3 vs 0 of 2, Fisher p = 0.10 | a single small-sample test, not a range |

A **match** is an independent translation that makes the same claim about the same people or events as the published English (wording may differ). A **partial** is the same claim with different wording, or a small mix-up of who did what. **Match or partial** adds those two grades. **Secure** means every important word on the line is hardened. Only two lexicon rows currently pass both hardening gates: Spanish *xefe* "chief, commander" and Nahuatl *Quecholli* (the weapon-month / precious-feather bird). The name *Ixchel* stays the Godstealer in the lexicon; the strict lookup found a medicinal-herb gloss, so that name is not counted as hardened. Possession order is not locked. Full detail, including working / fragile line grades and leave-one-text-out, is in master §1 and §17.

## Method, in brief

Three layers, each tested rather than merely asserted.

- **Lexicon (master §9).** Each committed word is traced to a named primary dictionary (Cordemex for Yucatec, Karttunen / Molina / the Florentine Codex for Nahuatl, and so on). Search is form-first: start from the letters and their sounds, not from the English already on the page. A word is **hardened (H)** only if a blind lookup recovers this project's declared root, language, and sense, and no strong rival meaning was written down. Most of the 78 entries are committed hypotheses, not certified.
- **Syntax (master §3).** The grammar is read from Vaal's own distribution (clause-initial type marking, dependents before the noun, verb before object where a verb governs one). It is never imported from Yucatec or Nahuatl and then "confirmed." Analysts who did not see this project's English recovered word-order regularities on real lines and not on scrambled ones; that gap is not statistically significant on this small panel.
- **Orthography (master §2.6, §17.9).** Recurring source-to-Vaal spelling correspondences are collected and sorted into stricter and looser operations. A phonetic phonology from in-game audio is deliberately out of scope. Anyone with that specialist skill is welcome to take it up; the present ceiling is orthographic.

## Repository map

This is the short map. It is not a catalogue of every analysis worksheet.

| Path | What it is |
|---|---|
| `The_Vaal_Tongue.pdf` | Typeset reconstruction. Start here. |
| `Vaal Translation/Vaal_Reconstruction.md` | Canonical master document (18 sections). |
| `Vaal_Reconstruction.md` | Sync copy of that master. Never edit it independently. |
| `Vaal Translation/README.md` | Maintenance, expansion, and the longer inner map. |
| `Vaal Translation/AGENTS.md` | Operating rules for anyone (or any agent) editing the reconstruction. |
| `Vaal Translation/analysis/` | Experiment protocols, results, and proof for §17. |
| `Vaal Translation/build/` | PDF pipeline, fonts, and a copy of the PDF. Instructions: `BUILD.md`. |
| `PDF Building/` | Alternate copy of the same PDF build tree. |
| `Vaal Translation/sources/` | Dictionaries and lore used to check roots. Large copyrighted dictionaries are gitignored. |
| `Maya_Dictionary_Sources.md` | Catalogue of Maya dictionary PDFs. |

## How to rebuild the PDF

The PDF is a primary deliverable, not a byproduct. Point at [`Vaal Translation/build/BUILD.md`](Vaal%20Translation/build/BUILD.md) for the self-contained recipe (Python, WeasyPrint, fonts). In short: keep `build_pdf.py`, the current master, and the `fonts/` folder together, then run `python3 build_pdf.py`. After a rebuild, the same PDF should land at repo root, in `Vaal Translation/build/`, and in `PDF Building/`.

## Fan work, not official

This is independent fan scholarship. It is not affiliated with, endorsed by, or associated with Grinding Gear Games. Path of Exile, Path of Exile 2, and the Vaal setting are their work. The reconstructions here are hypotheses about that invented language, offered with sources and error bars, not as an official decipherment.

## If you want to maintain or extend this

Humans who will edit files should read [`Vaal Translation/README.md`](Vaal%20Translation/README.md) for maintenance, versioning against game patches, and how to add a token or a line. Anyone (including an automated agent) who will change the reconstruction should read [`Vaal Translation/AGENTS.md`](Vaal%20Translation/AGENTS.md) first. Hard rules there include: do not rewrite published translations or approved glosses; keep the parent copy byte-identical with the canonical master; no em dashes, middots, or emojis anywhere.
