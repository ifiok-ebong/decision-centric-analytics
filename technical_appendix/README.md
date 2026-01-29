# Technical Appendix (Optional)

This folder is intentionally separated from the main case study to preserve the decision-centric focus of the project.

It exists for one reason.
To show proof-of-execution for readers who want to see how the decision-critical artifacts could be produced from raw tables.

What you will find here:
- One SQL query that demonstrates CTE structure, window functions, cohort-at-event logic, and null handling.
- One small Python script that builds an account-month panel and reproduces the decision table from the local dataset.

Notes:
- The raw dataset is not committed.
- These scripts are optional implementation details.


Safety: the Python script writes to `outputs/technical_appendix_decision_table.md` so it cannot overwrite the canonical decision artifact (`outputs/rivalytics_decision_table.md`).
