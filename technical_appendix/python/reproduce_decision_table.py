"""Reproduce the decision table from the local Rivalytics dataset.

This script is optional proof-of-execution.
It reads local CSVs (not committed) and writes a markdown decision table into outputs/.

Usage:
  python3 technical_appendix/python/reproduce_decision_table.py \
    --data-dir /path/to/saas-subscription-churn-analytics \
    --out-dir outputs
"""

import argparse
import csv
from collections import defaultdict, Counter
from datetime import datetime, date


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def yyyymm(d: date) -> str:
    return d.strftime("%Y%m")


def month_start(d: date) -> date:
    return date(d.year, d.month, 1)


def months_between(a: date, b: date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def cohort_from_tenure_m(t: int) -> str:
    if t <= 2:
        return "early"
    if 3 <= t <= 11:
        return "mid"
    return "late"


def median(vals):
    vals = sorted(vals)
    n = len(vals)
    if n == 0:
        return None
    mid = n // 2
    return vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2


def pct(x):
    return f"{x*100:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    data_dir = args.data_dir
    out_dir = args.out_dir

    accounts_path = f"{data_dir}/ravenstack_accounts.csv"
    subs_path = f"{data_dir}/ravenstack_subscriptions.csv"
    churn_path = f"{data_dir}/ravenstack_churn_events.csv"

    signup = {}
    with open(accounts_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            sd = parse_date(row.get("signup_date", ""))
            if sd:
                signup[row["account_id"]] = sd

    churn_date = {}
    with open(churn_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            cd = parse_date(row.get("churn_date", ""))
            if not cd:
                continue
            aid = row["account_id"]
            if aid not in churn_date or cd < churn_date[aid]:
                churn_date[aid] = cd

    # Allocate MRR to account-months
    rev_mrr = defaultdict(int)
    with open(subs_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            aid = row["account_id"]
            sd = parse_date(row.get("start_date", ""))
            ed = parse_date(row.get("end_date", "")) or churn_date.get(aid)
            if not sd:
                continue
            try:
                mrr = int(float(row.get("mrr_amount") or 0))
            except ValueError:
                mrr = 0
            if not ed:
                ed = sd
            cur = month_start(sd)
            endm = month_start(ed)
            while cur <= endm:
                rev_mrr[(aid, yyyymm(cur))] += mrr
                y = cur.year + (cur.month // 12)
                m = (cur.month % 12) + 1
                cur = date(y, m, 1)

    # Build cohort at churn + revenue at risk (prev month)
    churn_share = Counter()
    rev_risk = Counter()

    for aid, cd in churn_date.items():
        if aid not in signup:
            continue
        churn_m = yyyymm(cd)
        tenure = months_between(month_start(signup[aid]), month_start(cd))
        cohort = cohort_from_tenure_m(tenure)
        churn_share[cohort] += 1

        # prev month
        idx_year = int(churn_m[:4])
        idx_mon = int(churn_m[4:6])
        prev = date(idx_year, idx_mon, 1)
        prev = date(prev.year - 1, 12, 1) if prev.month == 1 else date(prev.year, prev.month - 1, 1)
        prev_m = yyyymm(prev)
        rev_risk[cohort] += rev_mrr.get((aid, prev_m), 0)

    total_churn = sum(churn_share.values())

    out_path = f"{out_dir}/rivalytics_decision_table.md"
    md = []
    md.append("# Decision Table — Rivalytics dataset (account-month panel)")
    md.append("")
    md.append("Cohorts: Early=0–3 months, Mid=4–12 months, Late=12+ months (context).")
    md.append("Event month: churn month if churned else last observed month.")
    md.append("")
    md.append("| Criterion (decision-critical) | Early (0–3m) | Mid (4–12m) | Which wins? |")
    md.append("|---|---:|---:|---|")
    md.append(f"| Share of churn events | {pct(churn_share['early']/total_churn)} | {pct(churn_share['mid']/total_churn)} | {'Early' if churn_share['early']>churn_share['mid'] else 'Mid'} |")
    md.append(f"| Revenue at risk (Total MRR, prev month) | {rev_risk['early']:,} | {rev_risk['mid']:,} | {'Mid' if rev_risk['mid']>rev_risk['early'] else 'Early'} |")
    md.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print("WROTE", out_path)


if __name__ == "__main__":
    main()
