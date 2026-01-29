# Dataset Overview

## Dataset used (current)
**Rivalytics - SaaS Subscription and Churn Analytics dataset**

Local path: available locally (not committed to git).

This dataset is used solely to support the project decision by enabling the **four decision-critical metrics** defined in `analysis_pre_analysis_plan.md`:
1) churn concentration, 2) revenue at risk (MRR), 3) usage decay prior to churn, 4) support burden relative to revenue.

---

## Tables used

### 1) Accounts
File: `ravenstack_accounts.csv`

Used for:
- account identity
- signup date (tenure anchor)

### 2) Subscriptions
File: `ravenstack_subscriptions.csv`

Used for:
- MRR allocation by account-month (directional “revenue at risk”)

### 3) Churn events
File: `ravenstack_churn_events.csv`

Used for:
- churn event timing (churn month)

### 4) Feature usage
File: `ravenstack_feature_usage.csv`

Used for:
- usage signals over time
- usage decay in periods leading up to churn

### 5) Support tickets
File: `ravenstack_support_tickets.csv`

Used for:
- support interactions over time
- support burden (cohort comparison)

---

## Derived analysis panel (how metrics are computed)
To enable cohort-level comparisons, we build a derived **account × month** panel (not committed to git):
- `outputs/rivalytics_panel_account_month.csv`

This panel contains (per account-month):
- tenure month and cohort label (early/mid/late)
- churn-month flag
- MRR
- usage metrics
- support ticket counts

---

## Cohort definitions (locked)
- **Early tenure:** 0–3 months
- **Mid tenure:** 4–12 months
- **Late tenure:** 12+ months (context only)

Primary comparison is **early vs mid**.

---

## Explicit assumptions (dataset-level)
- **MRR in the month prior to churn** is a reasonable directional proxy for cohort-level “revenue at risk”.
- **Tenure at churn month** is a meaningful proxy for lifecycle stage.
- Directional differences are sufficient for a one-quarter, one-choice decision.

---

## Known limitations (must be stated)
- Support-ticket data is **sparse** for many accounts; for interpretability we use incidence-style measures (e.g., “% of churned accounts with any tickets”) instead of relying only on tickets/$MRR medians.
- This dataset is observational; it does not provide causal impact of interventions (by design-this is a decision-architecture project).

---

## Non-goals (explicit)
- predicting individual churn probability
- ML models / churn scoring
- exhaustive exploration / dashboarding

The dataset is sufficient if it enables a **clear, defensible choice** between onboarding improvements vs mid-tenure retention using only decision-critical evidence.
