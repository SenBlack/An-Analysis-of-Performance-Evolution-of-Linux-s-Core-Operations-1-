#!/usr/bin/env python3
"""Compare two LEBench CSV logs.

The CSV stores seconds, one statistic per line:

    test name kbest:,<seconds>,
    test name average:,<seconds>,

The table is written in microseconds. The ratio is the second file divided
by the first. A ratio above 1 means the second kernel is slower.

    python week2/compare_results.py
    python week2/compare_results.py results/a.csv results/b.csv
"""

import statistics
import sys
from pathlib import Path

CALIBRATION = {"ref", "cpu"}


def parse_csv(path):
    kernel = None
    order = []
    values = {}
    text = Path(path).read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(",,"):
            continue
        parts = [part.strip() for part in line.split(",")]
        if parts[0].startswith("Test Name"):
            kernel = parts[1]
            continue
        if parts[0].endswith(":") and len(parts) > 1 and parts[1]:
            name = parts[0][:-1]
            values[name] = float(parts[1])
            order.append(name)
    if kernel is None:
        raise SystemExit(f"{path} has no Test Name row")
    return kernel, order, values


def base_names(order):
    names = []
    index = 0
    while index < len(order):
        label = order[index]
        if not label.endswith(" kbest"):
            raise SystemExit(f"expected a kbest row, found {label}")
        names.append(label[: -len(" kbest")])
        index += 2
    return names


def fmt_us(seconds):
    return f"{seconds * 1e6:.3f}"


def fmt_ratio(ratio):
    return f"{ratio:.3f}"


def build_table(left_name, left, right_name, right, names):
    ratios = []
    kernel_ratios = []
    table_rows = [
        "| Test | "
        f"{left_name} kbest (us) | {right_name} kbest (us) | kbest ratio | "
        f"{left_name} average (us) | {right_name} average (us) | average ratio |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    slower = 0
    for name in names:
        k_left = left[name + " kbest"]
        k_right = right[name + " kbest"]
        a_left = left[name + " average"]
        a_right = right[name + " average"]
        k_ratio = k_right / k_left
        a_ratio = a_right / a_left
        ratios.append(k_ratio)
        if name not in CALIBRATION:
            kernel_ratios.append(k_ratio)
        if k_ratio > 1:
            slower += 1
        table_rows.append(
            f"| {name} | {fmt_us(k_left)} | {fmt_us(k_right)} | "
            f"{fmt_ratio(k_ratio)} | {fmt_us(a_left)} | {fmt_us(a_right)} | "
            f"{fmt_ratio(a_ratio)} |"
        )

    text = [
        f"# LEBench {left_name} vs {right_name}",
        "",
        "CSV values are seconds. This table shows microseconds "
        "(seconds times 1,000,000).",
        f"Ratio = {right_name} / {left_name}. A ratio above 1 means "
        f"{right_name} is slower.",
        "",
        "Each column comes from one `OS_Eval` process. `kbest` and "
        "`average` are that process's own statistics. They are not the "
        "mean and standard deviation of three separate runs.",
        "",
        "## Summary",
        "",
        f"- Rows with higher kbest on {right_name}: {slower} of {len(names)}.",
        f"- Rows with higher kbest, leaving out `ref` and `cpu`: "
        f"{sum(ratio > 1 for ratio in kernel_ratios)} of {len(kernel_ratios)}.",
        f"- Median kbest ratio, all rows: {statistics.median(ratios):.3f}.",
        f"- Median kbest ratio, without `ref` and `cpu`: "
        f"{statistics.median(kernel_ratios):.3f}.",
        "",
        "`ref` and `cpu` are LEBench's calibration rows. "
        "`context siwtch` is LEBench's own spelling.",
        "",
        *table_rows,
    ]
    return "\n".join(text) + "\n", slower, len(names)


def main():
    script_dir = Path(__file__).resolve().parent
    default_dir = script_dir / "results"
    if len(sys.argv) == 1:
        left_path = default_dir / "LEBenchoutput.5.15.0-203-generic.csv"
        right_path = default_dir / "LEBenchoutput.6.8.0-138-generic.csv"
    elif len(sys.argv) == 3:
        left_path = Path(sys.argv[1])
        right_path = Path(sys.argv[2])
    else:
        raise SystemExit("usage: compare_results.py [left.csv right.csv]")

    left_kernel, left_order, left_values = parse_csv(left_path)
    right_kernel, right_order, right_values = parse_csv(right_path)
    names = base_names(left_order)
    missing = [name for name in names if name + " kbest" not in right_values]
    if missing:
        raise SystemExit("second CSV is missing: " + ", ".join(missing))

    table, slower, total = build_table(
        left_kernel, left_values, right_kernel, right_values, names
    )
    out_path = default_dir / "comparison.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(table, encoding="utf-8", newline="\n")
    print(f"wrote {out_path}")
    print(f"kbest slower on {right_kernel}: {slower} of {total}")


if __name__ == "__main__":
    main()
