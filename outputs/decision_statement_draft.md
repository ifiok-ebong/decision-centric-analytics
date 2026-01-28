# Decision Statement (Draft) — KKBox Retention Budget Allocation

## Decision (one sentence)
Prioritize **mid-tenure retention (4–12 months)** over early onboarding changes for the next quarter because it protects **more revenue at risk** per churned customer cohort in the observed window.

## Why this is the decision (decision-critical evidence)
Using the locked cohort definitions (Early = 0–3 months; Mid = 4–12 months) and a pragmatic churn-event proxy (churned → month of max `membership_expire_date`), the 1% sample shows:

- **Churned customers:** Early **87** vs Mid **130**
- **Churn rate (label window, cohort-at-event proxy):** Early **13.2%** vs Mid **5.6%**
- **Revenue-at-risk proxy (3 months forward):** Early **21,768** vs Mid **36,117**

Interpretation: although early-tenure churn rate is higher, the **mid-tenure segment carries more revenue at risk** under the current proxy, making it the higher-leverage place to spend a constrained budget if the goal is revenue protection.

## Decision-forcing framing (what we will NOT do)
We will **not** split the budget across early + mid cohorts this quarter. We will pick **one** primary target cohort and accept the trade-off.

## What must be true for this decision to hold (assumptions)
- The churn-event proxy (max `membership_expire_date`) is a reasonable approximation of the churn timing window.
- The revenue-at-risk proxy (3× average paid amount over the last 3 months) is directionally correct for comparing cohorts.

## Known limitations / next validation step
- Early cohort usage-decay is weakly estimated (few users with enough pre-history); we used an adaptive window to make it measurable.
- Next step is to replicate KKBox’s labeling logic more faithfully so the churn-event month is not proxy-based.

**Sources:**
- `outputs/decision_table_early_vs_mid_eventmonth.md`
- `outputs/decision_metrics_eventmonth_1pct.txt`
- `outputs/usage_decay_adaptive_eventmonth_1pct.txt`
