# CS340 Paper Reproduction

Name: 申伟华, 唐诗恒, 吴浩，范博睿

Student ID: 1240021926, 1240037734, 1240025700，1240021391

## Paper

An Analysis of Performance Evolution of Linux's Core Operations  
Xiang (Jenny) Ren, Kirk Rodrigues, Luyuan Chen, Camilo Vega, Michael Stumm, and Ding Yuan  
SOSP 2019

- Paper: https://www.eecg.toronto.edu/~stumm/Papers/Ren-sosp-19.pdf
- Original code: https://github.com/LinuxPerfStudy/LEBench
- License: Apache License 2.0. A copy is in `LICENSE`.
- Starting commit: `6aa7801a107d26e45eb65c7d827c7ea08059a3d3`

## What the paper is about

The paper measures how long basic Linux operations take, for example system calls, page faults, and context switches. The authors use their benchmark, LEBench, on Linux 3.0 through 4.20, and compare each version with Linux 4.0. Figure 1 shows that many of these operations became slower. One example in the paper is `select`, which became about twice as slow. They also say that 11 kernel changes explain most of the slowdown. Those changes include security patches, such as Meltdown and Spectre, and a few configuration choices. Later in the paper they turn the 11 changes off and report faster Redis, Apache, and Nginx runs.

The original experiments used Ubuntu 16.04 on an HP server with an Intel Xeon E5-2630 v3 and 128 GB of memory. Our machines are different, so the numbers will not match exactly. I will still use the same benchmark and the same kind of comparison: our time versus the number in the paper.

## What I plan to reproduce

I will start with Figure 1, because it is the main result. Running all 36 kernel versions is too much for this course, so I plan to pick a few versions, including 4.0, and a few tests such as `select`, `mmap`, and context switch. Each test should be run at least three times, and I will write down the average. If that works, I can look at one of the 11 changes and see whether turning it off changes the result.

## First week (11/1-11/9)

This week I created the repository, recorded the paper and the original code commit, and wrote this README. I have not installed a new kernel and I have not run the benchmark yet, so there are no results. Next week I will clone LEBench and try it on the Linux version already installed on the machine.

## Second week (11/9-11/15)

This week we ran LEBench in our Ubuntu 22.04.5 VirtualBox guest. TANG SHIHENG (1240037734) did these runs. Each kernel that boots has three complete runs. The mean wall-clock time is 1629.37 ± 16.23 seconds on `5.15.0-203-generic` and 2150.53 ± 113.56 seconds on `6.8.0-138-generic`. The number after ± is the sample standard deviation. On the mean of the three `kbest` values, 6.8 is slower on 41 of 42 tests. The median ratio is 1.22. The six logs and the full table are in `week2/three-runs/`.

Linux 4.4.302 and 4.15.18 were compiled and installed in this guest. Both stop at `Loading initial ramdisk`, so they have no LEBench results. These two kernels will not be rebuilt in the same virtual machine. Another group member will try them on a different machine.

## Third week (11/16-11/22)

This week we finished the one-factor extension. The kernel stayed `5.15.0-203-generic`. The only change was the boot parameter `mitigations=off`, added in GRUB for that boot. All three runs finished before the guest was rebooted. The mean wall-clock time is 1383.43 ± 18.02 seconds, compared with 1629.37 ± 16.23 seconds for the three default 5.15 runs from week 2. On the mean of the three `kbest` values, turning mitigations off is faster on 36 of 42 tests. The median ratio is 0.81. The logs and the full table are in `week3/mitigations-off/`.

This supports the claim that security mitigations slow these core operations, on this VirtualBox guest and for this one boot parameter. It does not reproduce the paper's 11 separate changes. Figure 1 is still open, because 4.4.302 and 4.15.18 still do not boot here.

---

吴浩 (1240025700) checked the logs already stored in the repository. The check covers the six week 2 CSV files and the three week 3 `mitigations=off` files. It confirms each kernel label, checks that the `kbest` test names and their order match, checks that `cmdline.txt` records `mitigations=off`, and checks that `wallclock.txt` has three times. It also records a SHA-256 fingerprint for each CSV. This is not a new LEBench run. From the repository root:

```bash
python week3/reproducibility_check.py
```

The script is `week3/reproducibility_check.py`. The report is `week3/reproducibility_report.md`.

## Fourth week (11/23-11/29)

范博睿（1240021391）is responsible for this week's work. This week we focused on comparing system call latency between Linux 4.0.5 and Linux 4.15.0-112, using an Ubuntu virtual machine running inside UTM on Apple M3 hardware. We executed and documented this part of the reproduction work. We followed the LEBench workflow from the original SOSP 2019 paper and ran the OS_Eval benchmark on both kernel versions separately. Each kernel produces raw measurement data saved as CSV files, which record test names, kbest latency, average latency, maximum latency and sample counts.

We implemented one supporting Python scripts. `compare4.0vs4.15.py` loads the CSV results from the two kernels, aligns the benchmark tests, extracts kbest latency and calculates the ratio defined as latency_4.15 / latency_4.0.5. A ratio greater than 1 means the operation becomes slower in 4.15, while a ratio below 1 indicates performance improvement. 

From our measured results, all fork-family operations including fork, big fork and huge fork show higher latency on Linux 4.15. This matches the paper’s argument that new security mitigations and additional memory accounting logic introduce runtime overhead. In contrast, thread creation shows a noticeable speedup, and lightweight system calls such as getpid also gain minor latency reduction from kernel-side optimizations. Context switch and socket primitives like send and recv have mixed results.

All related artifacts are organized under `week4/`. This folder includes `reproduction-setup.md` with all shell commands for environment setup and benchmark execution, the comparison table and interpretation in `analysis/comparison_table.md`.



## How to run LEBench on our guest

The guest is Ubuntu 22.04.5 in VirtualBox. From the LEBench directory:

```bash
cd ~/LEBench/TEST_DIR
sudo LEBENCH_DIR=$HOME/LEBench ./OS_Eval 0 "$(uname -r)"
```

`OS_Eval` segfaults when `LEBENCH_DIR` is unset. With `LEBENCH_DIR=$HOME/LEBench` and no trailing slash, the log is written to `/home/tang/LEBenchoutput.<kernel>.csv`. Copy that file before starting another run of the same kernel, because the next run overwrites it.

Do not run `sudo python run.py` on this guest. That script changes GRUB and reboots. It can boot `4.4.302` or `4.15.18`, and both of those stop at `Loading initial ramdisk`.

The LEBench source is https://github.com/LinuxPerfStudy/LEBench at commit `6aa7801a107d26e45eb65c7d827c7ea08059a3d3`. We have not modified those source files. Rebuild the three-run table from the six CSV logs with:

```bash
python week2/three_run_summary.py
```
