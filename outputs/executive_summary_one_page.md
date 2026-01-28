# One-page Executive Summary — Decision-Centric Analysis

## Decision (one sentence)
Prioritize **mid-tenure retention (4–12 months)** over onboarding improvements for the next quarter because it protects **more revenue at risk**, while churn concentration is roughly split between early and mid tenure.

## Why this decision (decision-critical evidence only)
Source: `outputs/rivalytics_decision_table.md`

- **Churn concentration (share of churn events):** Early **46.6%** vs Mid **44.0%** (near-tie)
- **Revenue at risk (Total MRR, month prior to churn):** Early **798,415** vs Mid **1,407,419** → **Mid**
- **Usage decay prior to churn (median):** Early **-37.2%** vs Mid **-11.1%** (early shows sharper decline; activation-failure signal)
- **Support burden (any tickets in last 3 months pre-churn):** Early **11.0%** vs Mid **37.4%** (mid higher incidence)

## Decision rule
Per `analysis_pre_analysis_plan.md`, **revenue at risk is primary**. When churn concentration is split, prioritize the cohort where a constrained intervention protects more recurring revenue.

## Robustness (Step 6)
Revenue-at-risk timing variations did **not** flip the recommendation (Mid remains higher):
- prior-month MRR → Mid wins
- 3-month average prior → Mid wins
- churn-month MRR → Mid wins

(See `outputs/stress_test_summary.md`.)

## What we are explicitly NOT doing
- No ML / churn scoring
- No dashboard sprawl
- No expanding beyond the four decision-critical metrics

## What would change the decision
- If a materially different revenue-at-risk definition reverses the Early vs Mid ranking.
- If churn concentration shifts materially toward early tenure.

## Immediate next-quarter action (what leadership can do now)
**Fund mid-tenure retention**:
- target high‑MRR 4–12 month accounts with retention offers + proactive success outreach
- prioritize accounts showing rising support interaction and stable-to-declining usage

## Two-minute version
See `outputs/two_minute_script.md`.
