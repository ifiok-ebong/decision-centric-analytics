# Dataset Overview

## Dataset Type
Representative subscription business dataset  
(Synthetic but designed to reflect realistic SaaS dynamics)

---

## Time Span
12 consecutive months of customer activity

---

## Purpose of the Dataset
The dataset exists solely to support a **churn intervention decision** by enabling:

- Tenure-based segmentation
- Estimation of revenue-at-risk
- Analysis of usage behavior preceding churn

---

## Tables Included

### 1. Customers
- `customer_id`
- `plan_type`
- `company_size`
- `industry`
- `start_date`
- `tenure_months`

### 2. Usage
- `customer_id`
- `month`
- `active_users`
- `core_feature_usage`
- `login_frequency`

### 3. Revenue
- `customer_id`
- `month`
- `monthly_recurring_revenue`
- `expansion_amount`
- `contraction_amount`

### 4. Churn
- `customer_id`
- `churn_flag`
- `churn_month`

---

## Key Assumptions
- Usage signals precede churn events
- Tenure is a meaningful segmentation dimension
- Revenue contribution varies significantly by cohort
- Directional accuracy is sufficient for decision-making

---

## Known Limitations
- No qualitative customer feedback included
- No experimental intervention data
- External market or competitive effects are not modeled

---

## Explicit Non-Goals
- Predicting individual churn probability
- Building a machine learning model
- Maximizing statistical precision

The dataset is considered sufficient if it allows a **clear comparison** between early-tenure and mid-tenure churn dynamics.

---