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

The paper measures how long basic Linux operations take, for example system calls and context switches. The authors use their benchmark, LEBench, on Linux 3.0 through 4.20. Figure 1 shows that many of these operations became slower. They also say that 11 kernel changes explain most of the slowdown.

## This week

This week I created the repository and wrote this README. I have not run the benchmark yet, so there are no results.

## How to run the original code

From the original README:

1. Clone https://github.com/LinuxPerfStudy/LEBench
2. Run `python get_kern.py`
3. Run `sudo python run.py`

The results are CSV files in the LEBench folder. More detail is in `EXPERIMENTS.md` in that repository.

I have not modified any original files.
