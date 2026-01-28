# Decision Table (1% sample; cohort plan locked)

Cohorts: Early=0–3 months, Mid=4–12 months. (Late shown for context only.)
Churn timing proxy: churn month = last month with tx_rows>0.

| Metric | Early (0–3m) | Mid (4–12m) | Notes |
|---|---:|---:|---|
| Customers (denominator) | 716 | 2,301 | Cohort at timing proxy |
| Churned customers | 145 | 124 | From train label; mapped to cohort at timing proxy |
| Churn rate | 20.3% | 5.4% | Label over study window (not month-by-month) |
| Revenue-at-risk proxy | 84,455 | 66,147 | Sum actual_amount_paid over last 3 months up to churn month (churned only) |
| Usage decay prior to churn (median) | n/a | -13.43% | pct change of total_secs (m-1 vs avg(m-3,m-2)); early n=0 under proxy |
| Usage decay prior to churn (trimmed mean 10%) | n/a | -1.03% | Robust mean; reduces outlier impact |

## Immediate read
- Early churn count: 145 vs Mid: 124.
- Early revenue-at-risk proxy: 84,455 vs Mid: 66,147.
- Usage-decay signal is currently only measurable for Mid (early lacks 3-month pre-history under the churn-month proxy).

## Next refinement (to remove proxy risk)
- Reconstruct churn event month using KKBox labeling logic (instead of last tx month) so early cohort gets a valid pre-window.
- Recompute revenue-at-risk as “next 1–3 months expected value” at churn event, not just trailing paid amount.