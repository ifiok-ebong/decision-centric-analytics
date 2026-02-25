# Technical Appendix (Optional)

This folder is intentionally separated from the main case study to preserve the decision-centric focus of the project.

It exists for one reason.
To show proof-of-execution for readers who want to see how the decision-critical artifacts could be produced from raw tables.

What you will find here:
- One SQL query that demonstrates CTE structure, window functions, cohort-at-event logic, and null handling.
- One small Python script that builds an account-month panel and reproduces the decision table from the local dataset.

Notes:
Tested with Python 3.12.
- The raw dataset is not committed.
- These scripts are optional implementation details.


Safety: the Python script writes to `outputs/technical_appendix_decision_table.md` so it cannot overwrite the canonical decision artifact (`outputs/rivalytics_decision_table.md`).

## Data acquisition

This appendix expects the Rivalytics Ravenstack dataset downloaded locally (raw CSVs are not committed).

Kaggle dataset slug:
- `rivalytics/saas-subscription-and-churn-analytics-dataset`

Expected files under your `--data-dir`:
- `ravenstack_accounts.csv`
- `ravenstack_subscriptions.csv`
- `ravenstack_churn_events.csv`
- `ravenstack_feature_usage.csv`
- `ravenstack_support_tickets.csv`

Example download (Kaggle CLI):
```bash
kaggle datasets download -d rivalytics/saas-subscription-and-churn-analytics-dataset -p /path/to/saas-subscription-churn-analytics --unzip
```

Then run:
```bash
python3 technical_appendix/python/reproduce_decision_table.py --data-dir /path/to/saas-subscription-churn-analytics --out-dir outputs
```

