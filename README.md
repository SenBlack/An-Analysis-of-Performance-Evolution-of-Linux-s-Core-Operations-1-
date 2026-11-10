# CS340 Paper Reproduction

Name: 申伟华  
Student ID: 1240021926

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

## First week

This week I created the repository, recorded the paper and the original code commit, and wrote this README. I have not installed a new kernel and I have not run the benchmark yet, so there are no results. Next week I will clone LEBench and try it on the Linux version already installed on the machine.

## How to run the original code

From the original README:

1. Clone https://github.com/LinuxPerfStudy/LEBench
2. Run `python get_kern.py`
3. Run `sudo python run.py`

The results are CSV files in the LEBench folder. More detail is in `EXPERIMENTS.md` in that repository.

I have not modified any original files.
