"""
Fulfillment Optimization — Exercise 1
======================================
Analyze inventory stock levels and fulfillment delays to identify
friction points and calculate reorder thresholds.

Data files (relative to this script):
    ../data/inventory_stock_levels.csv
    ../data/fulfillment_delay_report.csv

Usage:
    python exercise_1.py
"""

import csv
import math
from collections import defaultdict

# ──────────────────────────────────────────────
# Helper: load a CSV into a list of dicts
# ──────────────────────────────────────────────

def load_csv(relative_path):
    """Load a CSV file and return a list of row dicts."""
    rows = []
    with open(relative_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ──────────────────────────────────────────────
# Part 1 — Isolate fulfillment friction points
# ──────────────────────────────────────────────

def analyze_fulfillment_delays(records):
    """
    From the fulfillment delay report, compute:
      - Total shipments per carrier
      - On-time vs. delayed counts
      - Average delay (in days) for delayed shipments
      - Value at risk (declared_value of delayed shipments)
    """
    carrier_stats = defaultdict(lambda: {
        "total": 0,
        "on_time": 0,
        "delayed": 0,
        "exception": 0,
        "in_transit": 0,
        "delay_days": [],
        "value_at_risk": 0.0,
    })

    for row in records:
        carrier = row["carrier"]
        status = row["status"]
        declared_value = float(row["declared_value"]) if row["declared_value"] else 0.0

        cs = carrier_stats[carrier]
        cs["total"] += 1

        if status == "delivered":
            # Calculate delay days if we have both dates
            est = row["estimated_delivery"]
            actual = row["actual_delivery"]
            if est and actual:
                # Parse YYYY-MM-DD — simple day difference
                est_parts = [int(x) for x in est.split("-")]
                act_parts = [int(x) for x in actual.split("-")]
                est_days = est_parts[0] * 365 + est_parts[1] * 30 + est_parts[2]
                act_days = act_parts[0] * 365 + act_parts[1] * 30 + act_parts[2]
                delay = act_days - est_days
                if delay > 0:
                    cs["delayed"] += 1
                    cs["delay_days"].append(delay)
                    cs["value_at_risk"] += declared_value
                else:
                    cs["on_time"] += 1
            else:
                cs["on_time"] += 1
        elif status == "delayed":
            cs["delayed"] += 1
            cs["value_at_risk"] += declared_value
        elif status == "exception":
            cs["exception"] += 1
        elif status == "in_transit":
            cs["in_transit"] += 1

    return carrier_stats


def print_carrier_report(stats):
    """Print a carrier performance summary."""
    print("=" * 72)
    print("         CARRIER PERFORMANCE SUMMARY")
    print("=" * 72)
    print(f"{'Carrier':<20} {'Total':>6} {'On-Time':>8} {'Delayed':>8} "
          f"{'Avg Delay':>10} {'Exc/Trans':>10} {'Val@Risk':>12}")
    print("-" * 72)

    for carrier in sorted(stats.keys()):
        cs = stats[carrier]
        avg_delay = (
            sum(cs["delay_days"]) / len(cs["delay_days"])
            if cs["delay_days"]
            else 0
        )
        print(
            f"{carrier:<20} {cs['total']:>6} {cs['on_time']:>8} {cs['delayed']:>8} "
            f"{avg_delay:>8.1f}d  {cs['exception'] + cs['in_transit']:>6}   "
            f"${cs['value_at_risk']:>8.2f}"
        )
    print()


# ──────────────────────────────────────────────
# Part 2 — Calculate stock reorder thresholds
# ──────────────────────────────────────────────

def calculate_reorder_thresholds(inventory, fulfillment):
    """
    For each SKU-warehouse combo:
      - Determine the average carrier lead time from fulfillment data
      - Compute safety stock at 95% service level (Z = 1.65)
      - Calculate recommended reorder point
    """
    # Build lead time lookup from fulfillment data
    sku_lead_times = defaultdict(list)
    for row in fulfillment:
        sku = row["sku"]
        est = row["estimated_delivery"]
        ship = row["ship_date"]
        if est and ship:
            est_parts = [int(x) for x in est.split("-")]
            ship_parts = [int(x) for x in ship.split("-")]
            est_days = est_parts[0] * 365 + est_parts[1] * 30 + est_parts[2]
            ship_days = ship_parts[0] * 365 + ship_parts[1] * 30 + ship_parts[2]
            transit = est_days - ship_days
            if transit > 0:
                sku_lead_times[sku].append(transit)

    print("=" * 72)
    print("         REORDER THRESHOLD ANALYSIS")
    print("=" * 72)
    print(f"{'SKU':<10} {'Warehouse':<12} {'On Hand':>8} {'Cur ROP':>8} "
          f"{'Avg LT':>8} {'Safety Stk':>10} {'New ROP':>8} {'Status':>12}")
    print("-" * 72)

    alerts = []
    for row in inventory:
        sku = row["sku"]
        warehouse = row["warehouse"]
        stock = int(row["stock_on_hand"])
        current_rop = int(row["reorder_point"])
        supplier_lt = int(row["lead_time_days"])
        monthly_demand = int(row["monthly_demand"])

        # Use actual carrier lead time if available, else supplier lead time
        lt_list = sku_lead_times.get(sku, [])
        avg_lead_time = (
            sum(lt_list) / len(lt_list) if lt_list else float(supplier_lt)
        )

        # Standard deviation of lead times (or use 0.5 * avg as proxy)
        if len(lt_list) > 1:
            variance = sum((x - avg_lead_time) ** 2 for x in lt_list) / len(lt_list)
            stddev_lt = math.sqrt(variance)
        else:
            stddev_lt = avg_lead_time * 0.3  # default variability proxy

        # Daily demand approximation
        daily_demand = monthly_demand / 30.0

        # Safety stock at 95% service level (Z = 1.65)
        safety_stock = 1.65 * stddev_lt * daily_demand
        new_rop = int(avg_lead_time * daily_demand + safety_stock)

        # Determine status
        if stock <= 0:
            status = "OUT OF STOCK"
        elif stock < new_rop:
            status = "REORDER"
        elif stock < current_rop:
            status = "BELOW CUR ROP"
        else:
            status = "OK"

        if status != "OK":
            alerts.append((sku, warehouse, stock, current_rop, new_rop, status))

        print(
            f"{sku:<10} {warehouse:<12} {stock:>8} {current_rop:>8} "
            f"{avg_lead_time:>7.1f}d {safety_stock:>8.0f}   {new_rop:>8} {status:>12}"
        )

    print()

    # Summary
    print("=" * 72)
    print("         ACTION ITEMS")
    print("=" * 72)
    if alerts:
        print(f"{'SKU':<10} {'Warehouse':<12} {'On Hand':>8} {'Cur ROP':>8} "
              f"{'New ROP':>8} {'Issue':>16}")
        print("-" * 62)
        for sku, wh, stock, cur_rop, new_rop, status in alerts:
            print(f"{sku:<10} {wh:<12} {stock:>8} {cur_rop:>8} {new_rop:>8} {status:>16}")
    else:
        print("  No reorder alerts — all stock levels are adequate.")
    print()


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    # Load data
    print("Loading datasets...\n")
    inventory = load_csv("../data/inventory_stock_levels.csv")
    fulfillment = load_csv("../data/fulfillment_delay_report.csv")

    print(f"  inventory_stock_levels.csv  — {len(inventory)} rows loaded")
    print(f"  fulfillment_delay_report.csv — {len(fulfillment)} rows loaded\n")

    # Part 1 — Fulfillment friction points
    carrier_stats = analyze_fulfillment_delays(fulfillment)
    print_carrier_report(carrier_stats)

    # Part 2 — Reorder thresholds
    calculate_reorder_thresholds(inventory, fulfillment)


if __name__ == "__main__":
    main()
