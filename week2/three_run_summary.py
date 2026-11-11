#!/usr/bin/env python3
"""Rebuild the three-run mean table from the saved LEBench logs.

Per-test times come from the six CSV files in week2/three-runs/.
Wall-clock times are not in those CSV files. They come from wallclock.txt,
which records the final "Test took" line of each OS_Eval run.

The standard deviation is the sample standard deviation, divided by n-1.
CSV times are seconds. The per-test table is in microseconds.

    python week2/three_run_summary.py
"""

import statistics
import sys
from pathlib import Path

RUNS = (1, 2, 3)
KERNELS = ("5.15.0-203-generic", "6.8.0-138-generic")


def parse_csv(path):
    kernel = None
    order = []
    values = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split(",")]
        if parts[0].startswith("Test Name"):
            kernel = parts[1]
            continue
        if not parts[0].endswith(":") or len(parts) < 2 or not parts[1]:
            continue
        label = parts[0][:-1].strip()
        for stat in ("kbest", "average"):
            marker = " " + stat
            if label.endswith(marker):
                name = " ".join(label[: -len(marker)].split())
                values[(name, stat)] = float(parts[1])
                if stat == "kbest":
                    order.append(name)
                break
        else:
            raise SystemExit(f"{path} has an unrecognized row: {label}")
    if kernel is None:
        raise SystemExit(f"{path} has no Test Name row")
    return kernel, order, values


def parse_wallclock(path):
    times = {kernel: [] for kernel in KERNELS}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        kernel, _run, seconds = line.split()
        times[kernel].append(float(seconds))
    for kernel in KERNELS:
        if len(times[kernel]) != len(RUNS):
            raise SystemExit(f"{path} needs {len(RUNS)} times for {kernel}")
    return times


def fmt(value):
    return f"{value:.3f}"


def build(run_dir):
    parsed = {}
    order = None
    for kernel in KERNELS:
        runs = []
        for number in RUNS:
            path = run_dir / f"{kernel}-run{number}.csv"
            found, names, values = parse_csv(path)
            if found != kernel:
                raise SystemExit(f"{path} says {found}, expected {kernel}")
            if order is None:
                order = names
            elif names != order:
                raise SystemExit(f"{path} has a different test order")
            runs.append(values)
        parsed[kernel] = runs

    wall = parse_wallclock(run_dir / "wallclock.txt")
    lines = [
        "# LEBench three-run means",
        "",
        "Each number is the mean of three separate `OS_Eval` runs.",
        "The value after ± is the sample standard deviation, divided by n-1.",
        "Times in the CSV files are seconds. This table uses microseconds.",
        "Ratio = 6.8 mean / 5.15 mean. A ratio above 1 means 6.8 is slower.",
        "",
        "Regenerate this file with `python week2/three_run_summary.py`.",
        "",
        "## Wall clock",
        "",
        "| Kernel | Run 1 (s) | Run 2 (s) | Run 3 (s) | Mean (s) | "
        "Sample standard deviation (s) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for kernel in KERNELS:
        samples = wall[kernel]
        lines.append(
            f"| {kernel} | {fmt(samples[0])} | {fmt(samples[1])} | "
            f"{fmt(samples[2])} | {fmt(statistics.mean(samples))} | "
            f"{fmt(statistics.stdev(samples))} |"
        )

    lines.extend(
        [
            "",
            "## Per-test kbest",
            "",
            "| Test | 5.15 mean (us) | 5.15 sd (us) | 6.8 mean (us) | "
            "6.8 sd (us) | kbest ratio | 5.15 average mean (us) | "
            "6.8 average mean (us) | average ratio |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for name in order:
        cells = []
        means = {}
        for stat in ("kbest", "average"):
            for kernel in KERNELS:
                samples = [
                    run[(name, stat)] * 1e6 for run in parsed[kernel]
                ]
                mean = statistics.mean(samples)
                means[(kernel, stat)] = mean
                cells.extend((fmt(mean), fmt(statistics.stdev(samples))))
        kbest_ratio = means[(KERNELS[1], "kbest")] / means[(KERNELS[0], "kbest")]
        average_ratio = (
            means[(KERNELS[1], "average")] / means[(KERNELS[0], "average")]
        )
        lines.append(
            f"| {name} | {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} | "
            f"{fmt(kbest_ratio)} | {cells[4]} | {cells[6]} | {fmt(average_ratio)} |"
        )
    return "\n".join(lines) + "\n"


def main():
    script_dir = Path(__file__).resolve().parent
    run_dir = script_dir / "three-runs"
    if len(sys.argv) == 2:
        run_dir = Path(sys.argv[1])
    elif len(sys.argv) != 1:
        raise SystemExit("usage: three_run_summary.py [three-runs-directory]")
    text = build(run_dir)
    out_path = run_dir / "summary.md"
    out_path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
