#!/usr/bin/env python3
"""Generate one seeded blind worksheet.

Default: historical filenames blind_test_worksheet_s{seed}.csv (2026-07 epoch).
--rerun: write blind_test_worksheet_rerun_s{seed}.csv using the de-duplicated
generator (shared seen-set across the five protocol seeds).

If --rerun is used for a single seed before the full five-seed set exists,
this script generates the whole five-seed rerun set (same as
generate_pseudo_vaal.py --rerun) so cross-seed uniqueness is preserved.
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_pseudo_vaal import (  # noqa: E402
    SEEDS,
    generate_archive,
    generate_rerun,
    spanish_set,
)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("seed", type=int)
    p.add_argument("--rerun", action="store_true",
                   help="write rerun filenames; do not touch 2026-07 archives")
    args = p.parse_args(argv)
    spanish = spanish_set()
    if args.rerun:
        if args.seed not in SEEDS:
            print(f"warning: seed {args.seed} is not one of the protocol seeds {SEEDS}",
                  file=sys.stderr)
        generate_rerun(spanish)
        print(f"seed {args.seed}: rerun worksheets for all protocol seeds (shared uniqueness)")
        return
    generate_archive(args.seed, args.seed + 1, spanish, force=False)
    print(f"seed {args.seed}: archive path (refuses overwrite unless generate_pseudo_vaal.py --force)")


if __name__ == "__main__":
    main()
