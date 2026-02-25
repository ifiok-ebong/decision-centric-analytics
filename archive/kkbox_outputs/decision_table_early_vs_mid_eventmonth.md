# Decision Table (1% sample; event-month proxy)

Cohorts: Early=0–3 months, Mid=4–12 months.
Event month proxy: churned → month(max membership_expire_date).

| Metric | Early (0–3m) | Mid (4–12m) | Notes |
|---|---:|---:|---|
| Customers (denominator) | 658 | 2,307 | Cohort at event-month proxy |
| Churned customers | 87 | 130 | From train label; cohort at event-month proxy |
| Churn rate | 13.2% | 5.6% | Label window is global (not month-by-month) |
| Revenue-at-risk proxy (3mo forward) | 21,768 | 36,117 | 3×avg monthly paid over last 3 months up to event (churned only) |
| Usage decay prior to event (median) | n/a | 0.35% | total_secs m-1 vs avg(m-3,m-2) |


## Adaptive usage decay (so Early is measurable)
Source: usage_decay_adaptive_eventmonth_1pct.txt

- Early n=17 median=2.03%
- Mid   n=108 median=0.35%
