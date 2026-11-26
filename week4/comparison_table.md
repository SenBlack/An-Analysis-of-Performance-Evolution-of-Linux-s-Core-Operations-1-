# Comparison: v4.0.5 vs v4.15.0-112 (kbest latency)
| test | v4.0.5 kbest (s) | v4.15 kbest (s) | ratio (v4.15 / v4.0) |
| ---- | ---- | ---- | ---- |
| ref | 0.000000120 | 0.000000050 | 0.417 |
| cpu | 0.004292636 | 0.004284857 | 0.998 |
| getpid | 0.000000170 | 0.000000120 | 0.706 |
| context switch | 0.000002004 | 0.000002989 | 1.492 |
| send | 0.000002690 | 0.000002500 | 0.929 |
| recv | 0.000002410 | 0.000003200 | 1.328 |
| big send | 0.000005501 | 0.000005342 | 0.971 |
| big recv | 0.000004258 | 0.000004590 | 1.078 |
| fork | 0.000029205 | 0.000045183 | 1.547 |
| thr create | 0.000022740 | 0.000011833 | 0.520 |
| big fork | 0.000483440 | 0.000613354 | 1.269 |
| huge fork | 0.001202813 | 0.001641392 | 1.365 |


> Note: "context siwtch" in raw log is typo for context switch.

We observe higher latency for fork-family operations in Linux 4.15, likely caused by additional security mechanisms.
Thread creation is optimized and faster in 4.15. Simple lightweight syscalls such as getpid also gain minor speedups.

## Description
This file contains the full reproducible shell script for setting up and running the LEBench benchmark.
We build the benchmark tool, execute the OS_Eval test program, and export measurement results into CSV files.
The table below shows the measured kbest latency for a set of core operating system primitives under Linux 4.0.5 and Linux 4.15.0-112.
The ratio column equals `latency_4.15 / latency_4.0.5`.
A ratio > 1 means the operation becomes slower in the newer kernel; a ratio < 1 means it runs faster.

## Experiment Setup Script
```bash
uname -a
lsb_release -a
gcc --version
cd ~
git clone https://github.com/LinuxPerfStudy/LEBench.git
cd LEBench
git checkout 6aa7801a107d26e45eb65c7d827c7ea08059a3d3
export LEBENCH_DIR="$PWD/"
echo "$LEBENCH_DIR"
make -C TEST_DIR
ls -l TEST_DIR/OS_Eval
./TEST_DIR/OS_Eval 0 run1
mv output.run1.csv ~/lebench-run1.csv

./TEST_DIR/OS_Eval 0 run2
mv output.run2.csv ~/lebench-run2.csv

./TEST_DIR/OS_Eval 0 run3
mv output.run3.csv ~/lebench-run3.csv
ls -l ~/lebench-run*.csv
head -n 40 ~/lebench-run1.csv
