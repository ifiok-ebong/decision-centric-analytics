# Dataset Verification — rivalytics/saas-subscription-and-churn-analytics-dataset

Location (workspace): `/home/ubuntu/clawd/saas-subscription-churn-analytics/`

## Files found
- `ravenstack_accounts.csv`
- `ravenstack_subscriptions.csv`
- `ravenstack_churn_events.csv`
- `ravenstack_feature_usage.csv`
- `ravenstack_support_tickets.csv`

## Hard requirements checklist (PASS/FAIL)

| Requirement (from plan) | Present? | Evidence (columns) | Notes |
|---|---|---|---|
| Customer identifier | **PASS** | `account_id` across all tables | Consistent join key |
| Tenure / cohort timing | **PASS** | `signup_date` (accounts), `start_date`/`end_date` (subscriptions) | Tenure derivable at any date |
| Churn flag | **PASS** | `churn_flag` (accounts/subscriptions), plus `ravenstack_churn_events.csv` | Redundant sources (good) |
| Churn date / month | **PASS** | `churn_date` (churn_events), `end_date` (subscriptions) | We can choose a single canonical definition |
| Revenue / MRR | **PASS** | `mrr_amount`, `arr_amount` (subscriptions) | Directly supports revenue-at-risk |
| Usage signals over time | **PASS** | `usage_date`, `usage_count`, `usage_duration_secs` (feature_usage) | Event-level; can aggregate monthly |
| Support interactions | **PASS** | `submitted_at`, `closed_at`, `priority`, `resolution_time_hours`, `first_response_time_minutes` (support_tickets) | Ticket-level; can count per month and compute burden |

## Verdict
**PASS** — This dataset contains all decision-critical inputs required by the pre-analysis plan (including support interactions). It is suitable for the decision-centric analysis.

## Immediate next step (recommended)
Define the canonical churn event date for cohorting (choose one):
- Use `ravenstack_churn_events.churn_date` when present (preferred), else
- fall back to `ravenstack_subscriptions.end_date`.

Then build the minimal monthly panel at the **account_id × month** level:
- churn concentration by cohort (early 0–3m, mid 4–12m)
- revenue at risk by cohort (MRR/ARR)
- usage decay leading up to churn (monthly aggregates)
- support burden per revenue (tickets + resolution time per MRR)
