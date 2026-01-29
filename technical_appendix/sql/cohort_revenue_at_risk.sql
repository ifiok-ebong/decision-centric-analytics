-- Technical Appendix: cohorting and revenue-at-risk (directional)
-- Purpose: show proof-of-execution without changing the decision-centric artifact.
--
-- Requirements demonstrated:
-- - CTE structuring
-- - Window functions
-- - Cohort-at-event logic (cohort at churn month)
-- - Null handling
--
-- Assumptions:
-- - input tables exist with schemas similar to the Rivalytics dataset
-- - churn month is derived from churn_date
-- - MRR is available per subscription row

WITH churn_events AS (
  SELECT
    account_id,
    DATE_TRUNC('month', churn_date)::date AS churn_month
  FROM churn_events
  WHERE churn_date IS NOT NULL
),

accounts AS (
  SELECT
    account_id,
    signup_date::date AS signup_date
  FROM accounts
  WHERE signup_date IS NOT NULL
),

-- Allocate MRR to account-months based on subscription active months.
-- This is directional and intentionally minimal.
subscription_months AS (
  SELECT
    s.account_id,
    DATE_TRUNC('month', gs)::date AS month,
    COALESCE(s.mrr_amount, 0)::numeric AS mrr
  FROM subscriptions s
  CROSS JOIN LATERAL generate_series(
    DATE_TRUNC('month', s.start_date)::date,
    DATE_TRUNC('month', COALESCE(s.end_date, (SELECT churn_month FROM churn_events ce WHERE ce.account_id = s.account_id)))::date,
    interval '1 month'
  ) gs
  WHERE s.start_date IS NOT NULL
),

account_month_mrr AS (
  SELECT
    account_id,
    month,
    SUM(mrr) AS mrr
  FROM subscription_months
  GROUP BY 1, 2
),

panel AS (
  SELECT
    a.account_id,
    m.month,
    -- tenure in months
    ((DATE_PART('year', m.month) - DATE_PART('year', a.signup_date)) * 12
      + (DATE_PART('month', m.month) - DATE_PART('month', a.signup_date)))::int AS tenure_months,
    CASE
      WHEN ((DATE_PART('year', m.month) - DATE_PART('year', a.signup_date)) * 12
            + (DATE_PART('month', m.month) - DATE_PART('month', a.signup_date))) <= 2 THEN 'early'
      WHEN ((DATE_PART('year', m.month) - DATE_PART('year', a.signup_date)) * 12
            + (DATE_PART('month', m.month) - DATE_PART('month', a.signup_date))) BETWEEN 3 AND 11 THEN 'mid'
      ELSE 'late'
    END AS cohort,
    COALESCE(m.mrr, 0) AS mrr,
    CASE WHEN ce.churn_month = m.month THEN 1 ELSE 0 END AS is_churn_month
  FROM accounts a
  JOIN account_month_mrr m
    ON m.account_id = a.account_id
  LEFT JOIN churn_events ce
    ON ce.account_id = a.account_id
),

-- For churned accounts, take MRR in the month prior to churn as revenue-at-risk proxy.
revenue_at_risk AS (
  SELECT
    account_id,
    cohort,
    churn_month,
    -- month prior via window
    LAG(mrr) OVER (PARTITION BY account_id ORDER BY month) AS mrr_prev_month,
    is_churn_month
  FROM panel p
  JOIN churn_events ce
    USING (account_id)
  WHERE p.month <= ce.churn_month
)

SELECT
  cohort,
  COUNT(*) FILTER (WHERE is_churn_month = 1) AS churn_events,
  SUM(COALESCE(mrr_prev_month, 0)) FILTER (WHERE is_churn_month = 1) AS revenue_at_risk_mrr_prev_month
FROM revenue_at_risk
GROUP BY 1
ORDER BY 1;
