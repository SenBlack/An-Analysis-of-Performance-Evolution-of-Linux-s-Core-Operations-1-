# CS340 Paper Reproduction

Name: 申伟华, 唐诗恒

Student ID: 1240021926, 1240037734

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
