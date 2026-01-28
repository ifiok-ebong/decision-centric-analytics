# Step 6 — Assumption stress test (Rivalytics)

Purpose: test whether the recommendation flips under reasonable variations (robustness, not precision).

## Revenue-at-risk timing variations (primary)

| Definition | Early total | Mid total | Winner |
|---|---:|---:|---|
| (A) MRR in month prior to churn (baseline) | 798,415 | 1,407,419 | Mid |
| (B) Avg MRR over last 3 months prior to churn | 344,260 | 1,171,414 | Mid |
| (C) MRR in churn month | 1,531,562 | 1,709,038 | Mid |

**Result:** recommendation does **not** flip under these revenue-at-risk timing variations (Mid remains higher).

## Usage-decay window variations (secondary)

- (A) m-1 vs m-2 (baseline median): early=-37.2%, mid=-11.1%
- (B) avg(last3) vs avg(prev3) (median; requires >=6 months history): early=n/a, mid=7.1%

## “Decision flips only if…”
- Based on tested variations, the decision would flip only if a materially different revenue-at-risk definition reverses the Early vs Mid ranking (not observed here).
