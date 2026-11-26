# Week 4: LEBench — Comparing System Call Latency on Linux 4.0.5 and Linux 4.15.0-112
## Overview
This week’s work replicates the LEBench benchmark suite to evaluate system call latency across two different Linux kernel versions.
The experiment is carried out inside an Ubuntu virtual machine, running on UTM for Apple M3 Mac.
We focus on the **kbest (best-case minimum latency)** of typical system calls, to understand how kernel changes, security patches and code optimizations affect low-level system performance.

## Background
Linux kernels keep evolving. Newer versions introduce security features, memory management updates and algorithm optimizations.
These changes do not always improve speed: some simple system calls may become faster, while operations like fork may gain extra overhead from safety checks.
LEBench is a lightweight kernel benchmark designed to measure the latency of basic OS primitives, which fits our goal of comparing kernel performance trade-offs.

## Environment
- Host: Apple M3 Mac (18GB RAM)
- Virtualization: UTM
- Guest OS: Ubuntu
- Benchmark: LEBench, fixed commit `6aa7801a107d26e45eb65c7d827c7ea08059a3d3`
- Compiler: GCC
- Metric: kbest latency (minimum observed latency after sampling)

## File structure & Explanation
1. `analysis/comparison_table.md`
    Contains the complete bash script to pull, compile and run LEBench.
    It also includes our measured latency table, ratio calculation and interpretation of results.
    You can see raw commands, CSV output steps and our analysis of performance differences between two kernels.

2. `slides.md`
    This is the presentation material for our 1-minute segment in the group presentation.
    It covers three required topics: system architecture, data collection, and key engineering trade-offs.
    The script is timed to around 60 seconds and follows the marking rubric.

3. `notes.md`
    Prepared Q&A notes for the presentation.
    It lists common questions the marker may ask, including definitions, experiment limitations and root causes of observed results.
    This helps us respond accurately during the Q&A part.

## Limitation of this experiment
Our current measurement is based on a single run, without repeated trials for statistical averaging.
Virtualization on UTM also introduces scheduling noise, which may affect the precision of latency data.
These limitations are noted in our analysis and presentation.

## Core takeaway
Kernel updates involve trade-offs between security and raw performance.
New security checks add overhead to fork, while some other paths such as thread creation receive code-level optimizations and become faster.
