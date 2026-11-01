# Week 1 (checked Sunday 1 November 2026, 23:59)

Author of this week’s commit: 申伟华, 1240021926.

## Done

- Selected paper 9 from the CS340 paper list: Ren et al., SOSP 2019, LEBench.
- Recorded the upstream starting commit `6aa7801a107d26e45eb65c7d827c7ea08059a3d3` and the Apache License 2.0 terms that cover LEBench.
- Wrote the README so a later run can be followed without a hard-coded path: purpose, claims linked to Figure 1 and Section 5, fetch, environment record, and the reduced-scale plan.
- Added `scripts/record_environment.sh` and `scripts/fetch_lebench.sh`, wired through the Makefile.
- Added `.gitignore` so kernel trees, CSV results, build products, and credentials are not committed.

## Not done yet

- No latency numbers. Week 1 does not claim that Figure 1 was reproduced.
- LEBench has not been built on the course machine.
- Application speedups (Redis, Apache, Nginx) are not started.
- The group form (https://v.wjx.cn/vm/rZCQLSE.aspx) still has to be submitted by the group. This repository cannot submit that form.
