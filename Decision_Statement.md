# Decision Statement

## Decision owner
Executive Leadership Team (CEO, Head of Growth, Head of Customer Success)

---

## Decision (one sentence)
Prioritize **mid-tenure retention (4–12 months)** over onboarding improvements for the next quarter because it protects **more revenue at risk**, while churn concentration is roughly split between early and mid tenure.

---

## Constraints
- Budget allows only one initiative to be meaningfully funded
- Implementation window is one quarter
- Engineering and operations capacity is fixed
- Partial funding of both options is not viable

---

## Alternatives considered

### Option A: Onboarding improvements (0–3 months)
- Improve early activation
- Reduce churn within the first 90 days
- Decrease time-to-value for new customers

### Option B: Mid-tenure retention (4–12 months)
- Offer targeted retention incentives
- Improve customer support experience
- Reduce churn among established customers

---

## Decision-critical evidence (only)
Source: `outputs/rivalytics_decision_table.md`

- **Churn concentration (share of churn events):** Early **46.6%** vs Mid **44.0%** (near-tie)
- **Revenue at risk (Total MRR, month prior to churn):** Early **798,415** vs Mid **1,407,419** → **Mid**
- **Usage decay prior to churn (median):** Early **-37.2%** vs Mid **-11.1%** (early shows sharper decline; activation failure signal)
- **Support burden (any tickets in last 3 months pre-churn):** Early **11.0%** vs Mid **37.4%** (mid higher incidence)

---

## Decision rule applied
Per `analysis_pre_analysis_plan.md`, **revenue at risk is primary**. When churn concentration is split, prioritize the cohort where a constrained intervention protects more recurring revenue.

---

## Explicit assumptions (must hold)
- MRR in the month prior to churn is a reasonable directional proxy for “revenue at risk” for cohort comparison.
- Tenure cohort at churn month is a meaningful proxy for lifecycle stage.
- Directional differences are sufficient for this quarter’s one-choice decision.

---

## What would change the decision
- If a revised revenue-at-risk definition (e.g., next-3-months MRR) flips the cohort ranking.
- If churn concentration shifts materially (e.g., early becomes the clear majority of churn events).
