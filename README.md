# Decision-Centric Analysis

**Positioning:** *Direction sets the ceiling. Execution only helps you reach it.*

**Most dashboards increase debate.** This project shows how to force a retention decision with four decision-critical metrics and explicit trade-offs.

### What this proves
- I define decisions with constraints and reversal conditions (not KPIs).
- I design minimal analytics that reduce uncertainty and compel action.
- I translate cohort + revenue evidence into an executive recommendation.

Fast pitch (<2 minutes): `outputs/two_minute_script.md`
## Purpose
This project demonstrates how analytics should be designed to support a **real, constrained business decision** - not to showcase dashboards, tools, or technical sophistication.

The primary objective is to show judgment:
- how decisions are defined
- how irrelevant information is excluded
- how analytics constrains choices rather than expanding them

## Core question
**How does analytics fail when dashboards are built without an explicit decision, and how does decision clarity change what data, metrics, and visuals are required?**

## How to read this repo (60 seconds)
1) Read `outputs/executive_summary_one_page.md` (one screen).
2) If you want the logic, read `outputs/rivalytics_decision_table.md` + `Decision_Statement.md`.
3) If you want robustness, read `outputs/stress_test_summary.md`.
4) If you want the <2 minute version, read `outputs/two_minute_script.md`.

Note: `README.md` is the main artifact; `CASE_STUDY.md` mirrors it for portability.


## Key outputs (inline)

### Decision (one sentence)
Prioritize **mid-tenure retention (4–12 months)** over onboarding improvements for the next quarter because it protects **more revenue at risk**, while churn concentration is roughly split between early and mid tenure.

### Minimal decision table (decision-critical only)

| Criterion (decision-critical) | Early tenure (0–3m) | Mid tenure (4–12m) | Which side wins? |
|---|---:|---:|---|
| Share of churn events | 46.6% | 44.0% | Early |
| Revenue at risk (Total MRR, prev month) | 798,415 | 1,407,419 | Mid |
| Usage decay before churn (median, m-1 vs m-2) | -37.2% | -11.1% | Early |
| Support burden (any tickets in last 3 months pre-churn) | 11.0% | 37.4% | Mid |

### Robustness (Step 6)
Revenue-at-risk timing variations did **not** flip the recommendation (Mid remains higher). Full summary: `outputs/stress_test_summary.md`.

Full artifacts:
- `outputs/executive_summary_one_page.md`
- `outputs/rivalytics_decision_table.md`
- `Decision_Statement.md`
- `outputs/two_minute_script.md`
## What this is / is not
**This is:**
- a decision-first analytics case study
- a demonstration of problem framing and analytical restraint
- an applied example of translating data into executive action
- a portfolio artifact intended for senior reviewers and hiring managers

**This is not:**
- a dashboard showcase
- a tool demonstration
- a data cleaning / feature engineering exercise
- a machine learning project
- a tutorial
- a KPI catalog

Any work that does not directly support a decision is excluded.

---

## 1) Decision statement

### Decision owner
Executive Leadership Team (CEO, Head of Growth, Head of Customer Success)

### Decision (one sentence)
Allocate limited improvement budget for the next quarter toward **one** of:
- **Option A:** onboarding and early-stage activation improvements, or
- **Option B:** retention incentives and enhanced support for mid-tenure customers.

### Constraints
- Budget allows only one initiative to be meaningfully funded
- Implementation window is one quarter
- Engineering and operations capacity is fixed
- Partial funding of both options is not viable

### What would change the decision
The decision changes if evidence shows:
- churn is disproportionately concentrated in one tenure segment
- revenue-at-risk is materially higher in one segment
- usage decay precedes churn more strongly in one segment
- intervention leverage differs meaningfully between segments

### Success criteria
The decision is successful if it:
- targets the customer segment with the highest marginal impact on churn reduction
- protects the greatest amount of at-risk recurring revenue
- can be justified without requiring additional data collection

Time horizon: next quarter (3 months)

---

## 2) Business context (anonymized)

### Industry
B2B SaaS

### Business model
- Subscription-based recurring revenue
- Tiered pricing plans (Basic, Pro, Enterprise)
- Optional monthly add-ons

### Customer profile
- SMB and mid-market
- Multi-user accounts
- Usage intensity varies by plan and tenure

### Current situation
Customer acquisition is stable, but leadership observes:
- gradual churn increase over the past 12 months
- slowing net revenue growth due to retention pressure
- internal debate over where intervention should focus

### Strategic tension
Two plausible narratives compete:
- **Growth:** churn is primarily driven by poor early activation
- **Customer Success:** churn is driven by declining value among established customers

Resources do not allow both to be addressed simultaneously.

### Why this matters
Retention interventions are expensive and path-dependent. Choosing wrong:
- wastes budget
- delays impact
- reinforces organizational misalignment

Analytics is expected to reduce uncertainty and support a clear, defensible trade-off.

---

## 3) Why “dashboard-first” analytics fails (before → after)

### Before (failure mode)
A dashboard-first team will ship a retention dashboard with:
- dozens of engagement metrics (logins, feature clicks, DAU/WAU/MAU)
- global averages that erase tenure differences
- trend lines without thresholds
- filters that create multiple “truths”

Result: both teams can cherry-pick a metric to justify their preferred narrative. **More measurement, less decision.**

### After (decision-first)
Decision-first analytics produces a single, constrained artifact:
- one tenure comparison (early vs mid)
- four decision-critical metrics only
- explicit assumptions and “what would change the decision”

Result: **less measurement, more action.**

---

## 4) Analytics scope and pre-analysis plan (locked intent)

### Primary analytical question
Which tenure segment offers the **highest marginal impact on churn reduction and revenue protection**, given constrained resources?

### Tenure segmentation
- **Early tenure:** 0–3 months (onboarding/activation)
- **Mid tenure:** 4–12 months (established but not fully embedded)
- **Late tenure:** 12+ months (context only; not a primary intervention target)

Primary comparison: **early vs mid tenure**.

### Decision-critical metrics (only)
1) **Churn concentration**
- churn rate by cohort
- share of churn events by cohort

2) **Revenue at risk**
- MRR associated with churned customers
- revenue-at-risk aggregated by cohort

3) **Usage decay prior to churn**
- change in usage signals leading up to churn
- cohort comparison of decay patterns

4) **Support burden relative to revenue**
- support interactions per unit of revenue by cohort

### Explicitly excluded
- aggregate engagement metrics without cohort segmentation
- vanity metrics
- long trend lines without decision thresholds
- any metric that does not materially change the comparative outcome

### Allowed methods
- cohort aggregation
- comparative ratios/percentages
- directional trends
- threshold-based reasoning

### Disallowed methods
- predictive modeling / churn scoring
- machine learning
- optimization algorithms

---

## 5) Dataset (current)

## What gets messier in production data (and what I still would not analyze)
This case study uses a representative dataset to demonstrate decision architecture. In production SaaS data, measurement becomes messier, but the **decision structure and metric discipline remain the same**.

What gets messier:
- **Entity definitions:** account vs workspace vs subscription; cohorting must anchor on one decision-relevant entity.
- **MRR definition drift:** discounts, annual prepay normalization, upgrades/downgrades; revenue-at-risk must be defined consistently.
- **Churn semantics:** logo churn vs revenue churn vs contraction; the decision must pick the churn definition that matches the budget goal.
- **Support signal leakage:** tickets split across channels (email, chat, CSM notes); sparse tickets require interpretable proxies (incidence) rather than fragile ratios.
- **Instrumentation gaps:** usage events change with product releases; decay signals must be checked for measurement artifacts.

What I still would not do:
- expand to dozens of engagement metrics
- build a dashboard with exploratory filters
- add modeling/churn scoring to avoid making the trade-off

Even with messy production data, the metric set stays minimal; only the measurement plumbing changes.


**Dataset used:** Rivalytics - SaaS Subscription and Churn Analytics dataset.

Used only to support the decision by enabling the four decision-critical metrics:
- churn concentration
- revenue at risk (MRR)
- usage decay prior to churn
- support burden relative to revenue

Derived analysis panel (not committed): an account × month panel built from raw tables to support cohort comparisons.

---

## 6) Decision-forcing artifact

This artifact is designed to force a choice using only decision-critical evidence.

### Minimal decision table (filled)

| Criterion (decision-critical) | Early tenure (0–3m) | Mid tenure (4–12m) | Which side wins? |
|---|---:|---:|---|
| Share of churn events | 46.6% | 44.0% | Early |
| Revenue at risk (Total MRR, prev month) | 798,415 | 1,407,419 | Mid |
| Usage decay before churn (median, m-1 vs m-2) | -37.2% | -11.1% | Early |
| Support burden (any tickets in last 3 months pre-churn) | 11.0% | 37.4% | Mid |

Full artifact: `outputs/rivalytics_decision_table.md`

One-page executive summary: `outputs/executive_summary_one_page.md`

### Decision rule
Per `analysis_pre_analysis_plan.md`, **revenue at risk is primary**. When churn concentration is split, prioritize the cohort where a constrained intervention protects more recurring revenue.

### Robustness check (Step 6)
Revenue-at-risk timing variations did **not** flip the recommendation. Summary: `outputs/stress_test_summary.md`.

---

## 7) Assumptions (must remain explicit)
- usage decline precedes churn
- tenure is a meaningful proxy for lifecycle stage
- directional differences are sufficient for decision-making
- intervention impact is proportional within cohorts

Hidden assumptions are considered a project failure.

---

## 8) Distilled insights (generalizable)
- **If the decision isn’t crisp, analytics will expand the debate surface area.**
- **Cohorts beat averages** when the decision is about lifecycle (tenure).
- **Revenue-at-risk is a forcing function**: it turns “where churn happens” into “where the business bleeds.”
- **When evidence conflicts, don’t smooth it - rank it.** Here: revenue-at-risk is primary; usage decay is secondary.
- **Use interpretable proxies and label them.** Directional truth > false precision.
- **A good artifact makes disagreement expensive** by constraining what can be argued.

## 9) Completion conditions
This project is complete when:
- the decision is clearly supported
- additional metrics would not materially change the outcome
- the write-up stands alone without verbal explanation
- the reasoning can be explained verbally in under 2 minutes

---

## Files
- `README.md` - master case study (this document)
- `CASE_STUDY.md` - copy of the master case study
- `Decision_Statement.md`, `Business_Context.md`, `Dataset_Overview.md`, `analysis_pre_analysis_plan.md` - source sections (kept for traceability)
