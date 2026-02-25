"""Reproduce the 4-row decision table from the local Rivalytics dataset.

This script is optional proof of execution.
It reads local CSVs (not committed) and writes a markdown decision table.

Safety:
- This script writes to outputs/technical_appendix_decision_table.md.
- It does not overwrite the canonical decision artifact in outputs/rivalytics_decision_table.md.

Usage:
  python3 technical_appendix/python/reproduce_decision_table.py \
    --data-dir /path/to/saas-subscription-churn-analytics \
    --out-dir outputs

Tested with Python 3.12.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def yyyymm(d: date) -> str:
    return d.strftime("%Y%m")


def month_start(d: date) -> date:
    return date(d.year, d.month, 1)


def add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return date(y, m, 1)


def months_between(a: date, b: date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def cohort_from_tenure_m(t: int) -> str:
    # Locked cohorts: early 0-3 months, mid 4-12 months, late 13+ months
    if t <= 3:
        return "early"
    if 4 <= t <= 12:
        return "mid"
    return "late"


def pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def median(nums: list[float]) -> float | None:
    if not nums:
        return None
    nums = sorted(nums)
    n = len(nums)
    mid = n // 2
    if n % 2 == 1:
        return float(nums[mid])
    return float((nums[mid - 1] + nums[mid]) / 2)


@dataclass
class UsagePoint:
    month: str
    usage: float


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    data_dir = args.data_dir
    out_dir = args.out_dir

    accounts_path = f"{data_dir}/ravenstack_accounts.csv"
    subs_path = f"{data_dir}/ravenstack_subscriptions.csv"
    churn_path = f"{data_dir}/ravenstack_churn_events.csv"
    usage_path = f"{data_dir}/ravenstack_feature_usage.csv"
    tickets_path = f"{data_dir}/ravenstack_support_tickets.csv"

    # 1) Load signup dates
    signup: dict[str, date] = {}
    with open(accounts_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            sd = parse_date(row.get("signup_date", ""))
            if sd:
                signup[row["account_id"]] = sd

    # 2) Load churn dates (earliest per account)
    churn_date: dict[str, date] = {}
    with open(churn_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            cd = parse_date(row.get("churn_date", ""))
            if not cd:
                continue
            aid = row["account_id"]
            if aid not in churn_date or cd < churn_date[aid]:
                churn_date[aid] = cd

    # 3) Allocate MRR to account-months (directional)
    rev_mrr: defaultdict[tuple[str, str], float] = defaultdict(float)
    with open(subs_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            aid = row["account_id"]
            sd = parse_date(row.get("start_date", ""))
            ed = parse_date(row.get("end_date", "")) or churn_date.get(aid)
            if not sd:
                continue
            try:
                mrr = float(row.get("mrr_amount") or 0)
            except ValueError:
                mrr = 0.0
            if not ed:
                ed = sd

            cur = month_start(sd)
            endm = month_start(ed)
            while cur <= endm:
                rev_mrr[(aid, yyyymm(cur))] += mrr
                cur = add_months(cur, 1)

    # 4) Usage monthly aggregation (use usage_duration_secs if present; else session_duration_minutes*60)
    usage_by_acct_month: defaultdict[tuple[str, str], float] = defaultdict(float)
    with open(usage_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            aid = row.get("account_id")
            ud = parse_date(row.get("usage_date", ""))
            if not aid or not ud:
                continue
            m = yyyymm(month_start(ud))

            val = 0.0
            if row.get("usage_duration_secs") not in (None, ""):
                try:
                    val = float(row.get("usage_duration_secs") or 0)
                except ValueError:
                    val = 0.0
            else:
                # fallback to minutes
                try:
                    val = float(row.get("session_duration_minutes") or 0) * 60.0
                except ValueError:
                    val = 0.0

            usage_by_acct_month[(aid, m)] += val

    # 5) Support tickets: whether any ticket in last 3 months pre-churn
    tickets_months_by_acct: defaultdict[str, set[str]] = defaultdict(set)
    with open(tickets_path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            aid = row.get("account_id")
            sd = parse_date(row.get("submitted_at", ""))
            if not aid or not sd:
                continue
            tickets_months_by_acct[aid].add(yyyymm(month_start(sd)))

    # 6) Compute decision metrics by cohort at churn
    churn_share = Counter()
    rev_risk = Counter()

    # usage decay: for churned accounts, compare m-1 vs m-2 usage (monthly aggregated)
    usage_decay_values: defaultdict[str, list[float]] = defaultdict(list)

    # support burden: % churned accts with any ticket in last 3 months pre-churn
    any_ticket_count = Counter()

    for aid, cd in churn_date.items():
        if aid not in signup:
            continue

        churn_m = month_start(cd)
        churn_key = yyyymm(churn_m)
        tenure = months_between(month_start(signup[aid]), churn_m)
        cohort = cohort_from_tenure_m(tenure)
        churn_share[cohort] += 1

        # revenue at risk: MRR in month prior to churn
        prev_m = add_months(churn_m, -1)
        rev_risk[cohort] += rev_mrr.get((aid, yyyymm(prev_m)), 0.0)

        # usage decay: compare m-1 vs m-2 usage
        m1 = add_months(churn_m, -1)
        m2 = add_months(churn_m, -2)
        u1 = usage_by_acct_month.get((aid, yyyymm(m1)))
        u2 = usage_by_acct_month.get((aid, yyyymm(m2)))
        if u1 is not None and u2 is not None and u2 and u2 != 0:
            decay = (u1 - u2) / u2
            usage_decay_values[cohort].append(float(decay))

        # support burden: any ticket in last 3 months pre-churn (months m-3..m-1)
        window = {yyyymm(add_months(churn_m, -i)) for i in (1, 2, 3)}
        ticket_months = tickets_months_by_acct.get(aid, set())
        if window.intersection(ticket_months):
            any_ticket_count[cohort] += 1

    total_churn = sum(churn_share.values())
    if total_churn == 0:
        raise SystemExit("No churn events found. Cannot compute decision table.")

    # Compute medians
    def fmt_pct(x: float) -> str:
        return pct(x)

    def fmt_int(x: float) -> str:
        return f"{int(round(x)):,}"

    early_share = churn_share["early"] / total_churn
    mid_share = churn_share["mid"] / total_churn

    early_rev = rev_risk["early"]
    mid_rev = rev_risk["mid"]

    early_decay = median(usage_decay_values["early"])
    mid_decay = median(usage_decay_values["mid"])

    early_support = any_ticket_count["early"] / churn_share["early"] if churn_share["early"] else 0.0
    mid_support = any_ticket_count["mid"] / churn_share["mid"] if churn_share["mid"] else 0.0

    out_path = f"{out_dir}/technical_appendix_decision_table.md"

    md: list[str] = []
    md.append("# Decision Table - Rivalytics dataset (account-month panel)")
    md.append("")
    md.append("This is an appendix-only reproduction. Canonical artifact: outputs/rivalytics_decision_table.md")
    md.append("")
    md.append("| Criterion (decision-critical) | Early (0–3m) | Mid (4–12m) | Which wins? |")
    md.append("|---|---:|---:|---|")
    md.append(
        f"| Share of churn events | {fmt_pct(early_share)} | {fmt_pct(mid_share)} | "
        f"{'Early' if churn_share['early'] > churn_share['mid'] else 'Mid'} |"
    )
    md.append(
        f"| Revenue at risk (Total MRR, prev month) | {fmt_int(early_rev)} | {fmt_int(mid_rev)} | "
        f"{'Mid' if mid_rev > early_rev else 'Early'} |"
    )

    def fmt_decay(x: float | None) -> str:
        if x is None:
            return "NA"
        return f"{x*100:.1f}%"

    md.append(
        f"| Usage decay before churn (median, m-1 vs m-2) | {fmt_decay(early_decay)} | {fmt_decay(mid_decay)} | "
        f"{'Early' if (early_decay is not None and mid_decay is not None and early_decay < mid_decay) else 'Mid'} |"
    )
    md.append(
        f"| Support burden (any tickets in last 3 months pre-churn) | {fmt_pct(early_support)} | {fmt_pct(mid_support)} | "
        f"{'Mid' if mid_support > early_support else 'Early'} |"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print("WROTE", out_path)


if __name__ == "__main__":
    main()
