# Pre-Analysis Plan  
Project 1: Decision-Centric Analytics

---

## Purpose of This Document

This pre-analysis plan exists to **lock analytical intent before any calculations are performed**.

Its role is to ensure that:
- Analysis remains decision-driven
- Metrics are selected for leverage, not availability
- Results are interpretable in the context of a single constrained decision

Any analysis performed outside this plan must be explicitly justified or excluded.

---

## Decision Being Supported

**Decision:**  
Allocate limited improvement budget toward either:
- Onboarding and early-stage activation improvements, or
- Retention incentives and enhanced support for mid-tenure customers.

The analysis must clearly favor **one** option under realistic assumptions.

---

## Primary Analytical Question

Which customer tenure segment offers the **highest marginal impact on churn reduction and revenue protection**, given constrained resources?

---

## Tenure Segmentation Strategy

Customers will be segmented into **three tenure cohorts**:

1. **Early Tenure**
   - 0–3 months
   - Represents onboarding and activation phase

2. **Mid Tenure**
   - 4–12 months
   - Represents established but not fully embedded customers

3. **Late Tenure**
   - 12+ months
   - Included for context only, not as a primary intervention target

Primary comparison is between **Early Tenure** and **Mid Tenure** cohorts.

Late tenure customers are excluded from decision prioritization due to:
- Higher switching costs
- Lower marginal intervention leverage

---

## Decision-Critical Metrics

Only the following metrics are considered decision-critical.

### 1. Churn Concentration
- Churn rate by tenure cohort
- Share of total churn events by cohort

**Decision relevance:**  
Identifies where churn is most concentrated.

---

### 2. Revenue at Risk
- Monthly recurring revenue (MRR) associated with churned customers
- Revenue-at-risk aggregated by tenure cohort

**Decision relevance:**  
Determines which intervention protects more revenue.

---

### 3. Usage Decay Prior to Churn
- Change in usage metrics in periods leading up to churn
- Comparison of decay patterns between cohorts

**Decision relevance:**  
Indicates whether churn is driven by early failure to activate or later erosion of value.

---

### 4. Support Burden Relative to Revenue
- Support interactions per unit of revenue by cohort

**Decision relevance:**  
Identifies cost asymmetries that affect intervention efficiency.

---

## Explicitly Excluded Metrics

The following metrics will **not** be used, even if available:

- Aggregate engagement metrics without cohort segmentation
- Vanity metrics (e.g., total logins, total users)
- Long-term trend lines without decision thresholds
- Metrics that do not change the comparative outcome

If a metric does not materially change the decision, it is excluded by default.

---

## Analytical Methods (Allowed)

- Cohort-based aggregation
- Comparative ratios and percentages
- Directional trend analysis
- Threshold-based reasoning

---

## Analytical Methods (Disallowed)

- Predictive modeling
- Individual churn scoring
- Machine learning
- Over-parameterized statistical models
- Optimization algorithms

This project values **clarity over sophistication**.

---

## Assumptions

The following assumptions are accepted for the purpose of this decision:

- Usage decline precedes churn events
- Tenure is a meaningful proxy for lifecycle stage
- Directional differences are sufficient to justify prioritization
- Intervention impact is proportional within cohorts

All assumptions must be stated explicitly in the final write-up.

---

## Interpretation Rules

- Results will be interpreted comparatively, not absolutely
- Precision beyond decision relevance is unnecessary
- Ambiguous results must be acknowledged, not smoothed over

If results do not clearly favor one option, the outcome must reflect that.

---

## Completion Criteria for Analysis

The analysis phase is considered complete when:

- The decision can be justified using no more than the defined metrics
- Additional metrics would not materially change the conclusion
- The reasoning can be explained verbally in under two minutes
- A senior stakeholder could act without requesting further analysis

---

## Guardrails Against Drift

The analysis must stop if:
- New metrics are added without decision justification
- The focus shifts from comparison to explanation
- The work begins to resemble exploration rather than evaluation

This plan exists to prevent that.

---

End of Pre-Analysis Plan