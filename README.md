# Reproduction: An Analysis of Performance Evolution of Linux’s Core Operations

CS340 Operating Systems, 2026–2027. This repository reproduces selected results from:

Xiang (Jenny) Ren, Kirk Rodrigues, Luyuan Chen, Camilo Vega, Michael Stumm, and Ding Yuan. 2019. *An Analysis of Performance Evolution of Linux’s Core Operations.* In *Proceedings of the 27th ACM Symposium on Operating Systems Principles (SOSP ’19)*. https://doi.org/10.1145/3341301.3359640

Paper PDF: https://www.eecg.toronto.edu/~stumm/Papers/Ren-sosp-19.pdf

## Group member (this repository)

| Name | Student ID | GitHub |
| --- | --- | --- |
| 申伟华 | 1240021926 | https://github.com/SenBlack |

Other group members are not listed yet. Add them here when the group is complete. Each member must commit from their own GitHub account. Every commit message must contain that member’s student ID and full name.

## What the paper claims

The paper measures the latency of core Linux kernel operations with LEBench across kernels 3.0 through 4.20. It reports that many operations became slower, that 11 kernel changes explain the large movements, and that turning those changes off speeds up Redis, Apache, and Nginx.

Claims this reproduction will test, each tied to a result in the paper:

1. **Core-operation latency rose after Linux 4.0.** Figure 1(a) reports percentage change versus kernel 4.0. The text states that `select` is 100% slower than it was two years earlier, and that most measured operations are slower than on 4.0.
2. **Eleven changes account for the major slowdowns.** Figure 1(b) marks when each change is enabled: cgroup memory controller, missing CPU idle states, hugepages disabled, forced context tracking, TLB layout specification, fault around, user page-fault handling, randomized SLAB freelist, hardened usercopy, the Meltdown patch, and the Spectre patch. Sections 3 and 4 describe them.
3. **Disabling those changes speeds application workloads.** Section 5 reports speedups of up to 56% (Redis), 33% (Apache), and 34% (Nginx).

Week 1 does not report measurements. The first experiment will target claim 1 on a reduced set of kernels and tests. Claims 2 and 3 stay in scope only if the course machines can boot more than one kernel.

## Starting code

Upstream benchmark (Apache License 2.0, University of Toronto, 2019):

- Repository: https://github.com/LinuxPerfStudy/LEBench
- Starting commit: `6aa7801a107d26e45eb65c7d827c7ea08059a3d3` (`HEAD` of `master` as recorded on 1 November 2026)
- Experiment write-up: `EXPERIMENTS.md` in that commit
- Kernel images and config backups: https://github.com/LinuxPerfStudy/ExperimentSetup

This course repository does not vendor the upstream tree. `scripts/fetch_lebench.sh` clones that commit into `third_party/LEBench/`, which is gitignored. Files we later change will be listed in this README under **Modified files**. None are modified yet.

The upstream license text is in `LICENSE`.

## Repository layout

```
README.md                  purpose, setup, how to run, expected output
LICENSE                    Apache License 2.0 from LEBench
.gitignore
Makefile                   env, fetch, and (later) benchmark targets
docs/week1.md              what week 1 contains and what it does not
scripts/fetch_lebench.sh   clone the pinned upstream commit
scripts/record_environment.sh
                          print OS, kernel, compiler, and Python versions
```

## Setup

These steps use only tools named below. They do not install a new kernel.

Requirements:

- Git
- Python 3 (upstream `run.py` is Python)
- A C compiler (`gcc` or `cc`) for later LEBench builds
- `make`

The paper’s full run used Ubuntu 16.04.6 LTS and dozens of mainline kernels from 3.0.7 through 4.20.13 on an HP DL160 G9 (Xeon E5-2630 v3, 128 GB DDR4, SSD). Reproducing that hardware is not assumed. Record the machine you actually use:

```bash
make env
```

Fetch the pinned LEBench sources (network required):

```bash
make fetch
```

That writes `third_party/LEBench/` at commit `6aa7801a107d26e45eb65c7d827c7ea08059a3d3`.

## Build and run

Upstream build and run, after `make fetch`, from the cloned tree:

```bash
cd third_party/LEBench
python3 get_kern.py
sudo python3 run.py
```

`run.py` expects a crontab entry that reboots through the kernel list. Read `third_party/LEBench/README.md` and `EXPERIMENTS.md` before starting a reboot loop. Do not point those files at a hard-coded home directory; set `LEBENCH_DIR` to the absolute path of `third_party/LEBench` on that machine.

Week 1 stops at fetch and environment recording. A later commit will add a single-kernel LEBench target that does not reboot the host.

## Expected output and runtime

`make env` prints one block of version lines to the terminal and returns immediately.

`make fetch` clones one Git repository. On a normal campus network this finishes within a few minutes. It prints the checked-out commit and exits 0. It does not produce latency numbers.

A full upstream run writes CSV files inside the LEBench directory and can take many hours because it reboots across kernel versions. Those CSVs are gitignored. When we publish a number, the log that produced it will be committed under `results/` and named in the report.

## Deviations planned for a reduced run

| Item | Paper setting | Setting we expect to use | Reason |
| --- | --- | --- | --- |
| Kernel count | 36 versions, 3.0 through 4.20 | A few versions, including 4.0 as the Figure 1 baseline, plus one earlier and one later kernel if they boot | Building and rebooting 36 kernels does not fit the course timeline. |
| Hardware | HP DL160 G9, E5-2630 v3, 128 GB | Whatever machine or VM the group can boot | The paper’s server is not available. Section 6 of the paper already checks a second machine, so a different CPU is a stated limitation, not a silent change. |
| Workload scale | All LEBench tests in Figure 1 | `select`, `mmap`, and context switch first | These are the operations the paper highlights as large slowdowns. |

Any deviation that is actually used in a measured run will be copied into the final report with the setting that was used, not only the plan above.

## Modified files

None. Upstream files stay in the ignored clone until a commit says otherwise.
