#!/usr/bin/env python3
"""Fill a blind worksheet from form-first dictionary lookup.

Reads ONLY the worksheet (id, string). Does not open:
  blind_test_key_*, committed_readings.csv, master section 9/17,
  or any other agent's filled sheet.

Writes found, confidence, root, lang, gloss, residue, notes on every row.
A C row always has root/lang/gloss; empty C is never emitted.

Usage:
  python3 decode_blind.py --worksheet FILE --out FILE --latitude loose|strict --access offline|online
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dict_lookup as dl  # noqa: E402


def decode_rows(rows, latitude, access, blob):
    out = []
    for r in rows:
        surface = (r.get("string") or r.get("token") or "").strip()
        rec = dl.lookup(surface, latitude=latitude, access=access, blob=blob)
        row = {
            "id": r.get("id") or "",
            "string": surface,
            "found": rec["found"],
            "confidence": rec["confidence"],
            "root": rec["root"],
            "lang": rec["lang"],
            "gloss": rec["gloss"],
            "residue": rec["residue"],
            "notes": rec["notes"],
        }
        # Protocol: empty root/lang/gloss on a C is unscorable. Never emit that.
        if row["confidence"].lower() == "c" and not (row["root"] and row["lang"] and row["gloss"]):
            row["confidence"] = "none"
            row["found"] = "N"
            row["notes"] = (row["notes"] + "; demoted: C without root/lang/gloss").strip("; ")
        out.append(row)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worksheet", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--latitude", choices=["loose", "strict"], required=True)
    p.add_argument("--access", choices=["offline", "online"], required=True)
    p.add_argument("--token-col", default="string",
                   help="column holding the surface form (string or token)")
    args = p.parse_args(argv)
    blob = dl.load_index()
    with open(args.worksheet, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    # Allow token worksheets (Gate 1/2) that use 'token' not 'string'.
    for r in rows:
        if not (r.get("string") or "").strip():
            r["string"] = (r.get(args.token_col) or r.get("token") or "").strip()
    filled = decode_rows(rows, args.latitude, args.access, blob)
    fields = ["id", "string", "found", "confidence", "root", "lang", "gloss", "residue", "notes"]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in filled:
            w.writerow(row)
    n = len(filled)
    c = sum(1 for r in filled if r["confidence"].lower() == "c")
    s = sum(1 for r in filled if r["confidence"].lower() == "soft")
    print(f"wrote {args.out} n={n} C={c} soft={s} none={n-c-s} lat={args.latitude} access={args.access}")


if __name__ == "__main__":
    main()
