# Project Challenges / Gotchas Log

Purpose: capture the real-world friction we hit while building this KKBox churn decision-centric analysis, so we can anticipate issues, avoid repeating mistakes, and keep the workflow reproducible.

> Conventions
> - **Symptom**: what we observed
> - **Cause**: likely root cause
> - **Fix / Mitigation**: what we did (or should do next time)
> - **Prevention**: checklist item / rule to follow

---

## 27 Jan 2026 — Data acquisition & extraction

### 1) Huge competition download size (8.34 GB zip)
- **Symptom:** Long download and large on-disk footprint.
- **Cause:** The Kaggle competition bundle is multi-GB and contains multiple dataset variants (v1/v2).
- **Fix / Mitigation:** Downloaded successfully; later switched to downloading a single file (`user_logs.csv.7z`) instead of the full zip.
- **Prevention:** Prefer `kaggle competitions download -f <file>` for targeted files when possible.

### 2) Disk exhaustion during extraction (`errno=28 No space left on device`)
- **Symptom:** `7z` extraction failed while extracting `user_logs.csv.7z`.
- **Cause:** `user_logs.csv.7z` expands to a very large CSV; keeping the full zip + multiple `.7z` archives + extracted CSVs simultaneously exceeded disk.
- **Fix / Mitigation:**
  - Deleted large archives once not needed.
  - Avoided full extraction of `user_logs.csv`.
  - Used **streaming extract** (`7z x -so`) + filter to create a smaller sampled file.
- **Prevention:**
  - Never fully extract `user_logs` on small disks.
  - Keep a rule: **extract only what you need**, and delete archives promptly.
  - Check free space with `df -h` before large operations.

### 3) Hidden dependency: pandas not installed
- **Symptom:** Python step failed with `ModuleNotFoundError: No module named 'pandas'`.
- **Cause:** Environment didn’t include pandas (and we avoid installing packages without explicit permission).
- **Fix / Mitigation:** Rewrote sampling using Python standard library (`csv`, `hashlib`) to avoid pandas dependency.
- **Prevention:** Use stdlib-first scripts unless we’ve explicitly set up a Python environment.

### 4) Script bug: env vars not passed into Python subprocess
- **Symptom:** `KeyError: 'RAW'` when Python tried `os.environ['RAW']`.
- **Cause:** Shell variables weren’t exported; Python subprocess didn’t see them.
- **Fix / Mitigation:** Passed paths directly into the heredoc via string interpolation (or explicitly `export RAW=...`).
- **Prevention:**
  - Prefer explicit path arguments.
  - If using env vars, `export` them before launching Python.

### 5) Long-running stream-filter phase with little/no progress output
- **Symptom:** After download, the job appeared “stuck”; no new console output while filtering.
- **Cause:** Streaming parse/filter is CPU + I/O heavy and our script didn’t emit periodic progress.
- **Fix / Mitigation:** Monitored:
  - output file growth (`ls -lh`)
  - writer process via `lsof`
  - disk via `df -h`
- **Prevention:** Add lightweight progress logging (e.g., print every N rows) for long-running filters.

### 6) Intermittent truncated/mangled exec output
- **Symptom:** One status command returned garbled output that looked like the command itself.
- **Cause:** Tool output truncation/formatting oddity.
- **Fix / Mitigation:** Re-ran a smaller, more targeted check.
- **Prevention:** When output is garbled, re-run minimal commands (single-purpose checks).

---

## Current dataset artifacts (post-mitigation)

Saved locally (path omitted).
- `train.csv` (~45 MB)
- `members_v3.csv` (~409 MB)
- `transactions.csv` (~1.7 GB)
- `msno_sample_1pct.txt` (~435 KB; 9,879 users)
- `user_logs_sample_1pct.csv` (~183 MB)

Archives were deleted after extraction/sampling to conserve disk.

---

## To append next
- Any issues during: monthly aggregation, churn label alignment, tenure definitions, cohort splits, leakage risks, and decision table construction.
