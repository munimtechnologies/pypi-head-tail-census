#!/usr/bin/env python3
"""Reproduce the head-line tally of the PyPI head-vs-tail study corpus.

Reads ``studies.csv`` (the open, CC BY 4.0 register of pre-registered PyPI
head-vs-tail metadata studies) and prints the exact numbers quoted in the
corpus meta-post, so anyone can regenerate them from the data instead of
trusting a hand count:

    "Of N directional pre-registered predictions, only H held."

Usage:
    python meta_tally.py [path/to/studies.csv]

Outcome vocabulary (the ``outcome`` column of studies.csv):
    HELD, REVERSED, NULL, REPLICATION-FAILED  -> directional predictions
    DESCRIPTIVE, METHOD                        -> non-directional studies

A study is "directional" when it pre-registered a "popular head is richer /
more modern / cleaner" prediction. DESCRIPTIVE and METHOD studies made no
such directional claim. A directional prediction "held" only when its
outcome is HELD; REVERSED, NULL and REPLICATION-FAILED did not. The public
5-way grouping folds METHOD into the descriptive bucket.

Standard library only.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter

DIRECTIONAL = {"HELD", "REVERSED", "NULL", "REPLICATION-FAILED"}
NON_DIRECTIONAL = {"DESCRIPTIVE", "METHOD"}
KNOWN_OUTCOMES = DIRECTIONAL | NON_DIRECTIONAL


def tally(outcomes):
    """Return the corpus tally from an iterable of outcome strings."""
    counts = Counter(o.strip().upper() for o in outcomes)
    unknown = set(counts) - KNOWN_OUTCOMES
    if unknown:
        raise ValueError(f"unknown outcome value(s): {sorted(unknown)}")
    directional_total = sum(counts[o] for o in DIRECTIONAL)
    grouped = {
        "reversed": counts["REVERSED"],
        "held": counts["HELD"],
        "null": counts["NULL"],
        "replication_failed": counts["REPLICATION-FAILED"],
        "descriptive": counts["DESCRIPTIVE"] + counts["METHOD"],
    }
    return {
        "total_studies": sum(counts.values()),
        "raw_counts": dict(counts),
        "grouped_5way": grouped,
        "directional_total": directional_total,
        "directional_held": counts["HELD"],
    }


def read_outcomes(path):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or "outcome" not in reader.fieldnames:
            raise ValueError(f"no 'outcome' column in {path}; found {reader.fieldnames}")
        return [row["outcome"] for row in reader]


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    path = argv[1] if len(argv) > 1 else os.path.join(here, "studies.csv")
    result = tally(read_outcomes(path))
    g = result["grouped_5way"]
    print(f"studies.csv: {result['total_studies']} studies")
    print(
        "5-way grouping (METHOD folded into descriptive): "
        f"{g['reversed']} reversed, {g['held']} held, {g['null']} null, "
        f"{g['replication_failed']} replication-failed, {g['descriptive']} descriptive"
    )
    print(
        f"Directional predictions: {result['directional_held']} of "
        f"{result['directional_total']} held."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
