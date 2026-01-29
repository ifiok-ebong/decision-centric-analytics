# Decision Table - Rivalytics dataset (account-month panel)

Cohorts: Early=0–3 months, Mid=4–12 months, Late=12+ months (context).
Event month: churn month if churned else last observed month.

| Criterion (decision-critical) | Early (0–3m) | Mid (4–12m) | Which wins? |
|---|---:|---:|---|
| Share of churn events | 46.6% | 44.0% | Early |
| Revenue at risk (Total MRR, prev month) | 798,415 | 1,407,419 | Mid |
| Usage decay before churn (median, m-1 vs m-2) | -37.2% | -11.1% | Early |
| Support burden (any tickets in last 3 months pre-churn) | 11.0% | 37.4% | Mid |

## Notes
- Revenue-at-risk uses MRR in month prior to churn (directional; aligns with pre-analysis plan).
- Support burden uses % of churned accounts with any tickets (more interpretable than tickets/$MRR medians, which are sparse/near-zero).
