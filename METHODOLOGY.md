# Methodology and pre-registration protocol

## The study shape

Each of the 30 studies in [`studies.csv`](studies.csv) follows the same template:

1. **Pick one metadata or packaging axis** (a classifier, a `requires_dist` property, a
   README format, a release-timing pattern, etc.).
2. **State a directional prediction before measuring.** The default prior, taken from
   common developer intuition, was *"the popular head is richer / more modern / cleaner
   than the long tail."* The competing hypothesis was named explicitly in each write-up.
3. **Define two frames on the public PyPI index:**
   - **Head:** the most-downloaded packages (download rank from public counts).
   - **Tail:** a uniform-random sample of the entire PyPI index, drawn under a fixed
     integer seed so the draw is reproducible.
   Each write-up records its frame sizes and the head/tail overlap.
4. **Measure** the axis for every package in both frames by querying the public
   `https://pypi.org/pypi/<name>/json` endpoint and reading author-supplied metadata.
5. **Grade** the prediction against the result and publish — including when it reversed,
   came back null, or an external number failed to replicate.

## Data source and a caution

All measurements come from the public PyPI JSON API. Most of `info.*` is raw
author-supplied metadata (`keywords`, `requires_dist`, `classifiers`, `name`,
`version`, `urls`). **One field is not raw:** `info.project_urls` is *synthesized* by
the Warehouse backend, which manufactures a `Homepage` entry from the legacy
`Home-page` field. Study 14 documents this and is coded `METHOD` for that reason — you
cannot use `project_urls` to measure PEP 753 homepage migration.

A classifier or field being *present* is a signaling convention, not ground truth.
Several studies spot-check a handful of packages live to confirm the field means what it
appears to mean.

## Outcome coding rule

Each row's `outcome` is assigned by this rule, applied to the published headline:

- **REVERSED** — the result negated the pre-registered directional prediction: the
  measured gap favored the long tail where the head was predicted to lead, or vice
  versa (headlines of the form "No — the long tail does…", "reversed", "proved me
  wrong").
- **HELD** — the measured direction and a non-trivial magnitude matched the
  pre-registered prediction.
- **NULL** — no meaningful head-vs-tail gap, or a gap too small to support the
  prediction (razor-thin margins count as NULL, not HELD).
- **REPLICATION-FAILED** — the study was an external replication and the published
  number did not reproduce on fresh data.
- **DESCRIPTIVE / METHOD** — no directional prediction was posed (a baseline census or
  a measurement-validity finding).

The rule is deliberately simple so the counts in the README are reproducible from the
headlines alone. Every row carries its `devto_url`; re-grade any row you disagree with.

## Prior art and why this corpus is new

Individual facts about PyPI metadata are documented across PEPs, the Warehouse docs,
and ad-hoc blog posts. What is new here is a **single, pre-registered, uniform-random,
whole-ecosystem head-vs-tail program applied the same way across ~30 axes, with the
directional prediction fixed in advance and the outcome recorded whether it held or
not.** The resulting meta-observation — that the "popularity implies modernity/hygiene"
prior holds in only a minority of axes — is, to our knowledge, not reported elsewhere,
precisely because no one else has run the same frame across this many axes with
pre-registration and published the negatives.

Negative, null, and reversed results are first-class here: a cleanly-explained reversal
is treated as the most valuable outcome shape, not a failure.

## Limits

- Observational, not causal. "Popularity" is download rank, a noisy proxy.
- Outcome coding is a judgment against each headline; the rule above and the per-row
  URLs make it auditable and contestable.
- Exact percentages shift slightly with the download-rank snapshot and the tail seed;
  rely on direction and magnitude, not a single canonical figure.

---

Made with AI by autonomous agents working as MV2 of Munim, Inc.
