# Week 2: first LEBench runs

Student: TANG SHIHENG
Student ID: 1240037734
Date: 2026-11-10

## What this week measured

LEBench was run once on each Ubuntu kernel that boots in this VirtualBox guest.

| Kernel | How it was installed | Result | Wall-clock time |
| --- | --- | --- | --- |
| 5.15.0-203-generic | installed with `apt` | one full run | 1619.62 s (27.0 min) |
| 6.8.0-138-generic | default kernel of this guest | one full run | 2238.18 s (37.3 min) |

The guest is Ubuntu 22.04.5 LTS. VirtualBox is running on a Mac, and the guest disk is on an external Lenovo SSD. From `~/LEBench` the command was:

```bash
sudo LEBENCH_DIR=$HOME/LEBench ./OS_Eval 0 $(uname -r)
```

`OS_Eval` segfaults when `LEBENCH_DIR` is unset. `$(uname -r)` is what the CSV stores as `Test Name`, so the kernel name in each file is the kernel that was running.

The screenshots in `screenshots/` were taken after `OS_Eval` returned to the shell prompt `tang@tang-VirtualBox:~/LEBench/TEST_DIR`. The guest clock reads 11:02 for the 5.15 run and 11:49 for the 6.8 run, both on 10 November. The last lines on those screens are the polling tests. The line above `Performing test select` belongs to the previous test. The final `Test took` line is the whole program.

| Test | Iterations | 5.15.0-203-generic | 6.8.0-138-generic |
| --- | ---: | ---: | ---: |
| select | 100000 | 5.713 s | 6.367 s |
| poll | 100000 | 4.466 s | 4.554 s |
| epoll | 100000 | 5.839 s | 6.975 s |
| select big | 10000 | 46.780 s | 55.973 s |
| poll big | 10000 | 47.016 s | 57.055 s |
| epoll big | 10000 | 64.868 s | 73.309 s |
| whole `OS_Eval` |  | 1619.620 s | 2238.183 s |

These wall-clock lines are the time for that whole test loop. They are not the per-operation `kbest` values in the CSV.

## Kernels with no numbers

Linux 4.4.302 and Linux 4.15.18 were compiled and installed in this same guest. Both stop while booting, at `Loading initial ramdisk`. Neither run produced a LEBench CSV.

4.15 needed four source fixes before it would compile against this Ubuntu 22.04 guest: `STACK_VALIDATION`, `RETPOLINE`, `PF_MAX` in the SELinux `classmap.h`, and `-fcommon` in `arch/x86/boot/compressed/Makefile`. The kernel package installed. The boot still stops at the ramdisk line. 4.4.302 stops at the same line. The paper's setup is Ubuntu 16.04 on a physical HP server. This guest is Ubuntu 22.04 in VirtualBox, so these two builds are an environment mismatch on this machine. They will not be rebuilt in this same guest. Another group member will try 4.4.302 and 4.15.18 on a different machine.

`screenshots/grub-4.4.302-selected.jpg` is the GRUB menu with `Ubuntu, with Linux 4.4.302` selected. `screenshots/4.4.302-loading-initial-ramdisk.png` is that boot stopped at `Loading initial ramdisk`. `screenshots/grub-4.15.18-selected.jpg` is the same menu with `Ubuntu, with Linux 4.15.18` selected. `screenshots/4.15.18-loading-initial-ramdisk.png` is that boot stopped at `Loading Linux 4.15.18` / `Loading initial ramdisk`. There is no separate `uname -r` screenshot. The kernel name is on the GRUB line, on the `Loading Linux ...` line, and in the CSV `Test Name` row for the two runs that finished.

## How this run differs from the paper

| Item | Paper | This run | Why |
| --- | --- | --- | --- |
| Machine | HP server, Xeon E5-2630 v3, 128 GB, local SSD | VirtualBox guest on a Mac, disk on an external SSD | Course machine |
| OS | Ubuntu 16.04.6 | Ubuntu 22.04.5 guest | Same |
| Kernels | Ubuntu mainline 3.0.7 through 4.20.13, baseline 4.0.5 | 4.4.302 and 4.15.18 do not boot; measured 5.15.0-203-generic and 6.8.0-138-generic | The kernels from the paper's range hang in this VM. 5.15 and 6.8 boot |
| Kernel build | The paper's mainline packages and configs | Ubuntu `generic` kernels, security mitigations left on | The self-built 4.4 and 4.15 kernels do not boot |
| Runs | Repeated samples inside LEBench, many versions | Three separate `OS_Eval` runs on each kernel that boots | Mean and sample standard deviation are in `three-runs/summary.md` |
| Code | LEBench commit `6aa7801a107d26e45eb65c7d827c7ea08059a3d3` | Same commit on the guest, at `~/LEBench`. No LEBench source files were changed | The guest `git rev-parse HEAD` matches the starting commit in the repository README |

## Result

The numbers below are run 1 only. Each booting kernel now has three runs, and the mean ± sample standard deviation is in `three-runs/summary.md`. On those means, 6.8 is still slower on 41 of 42 `kbest` rows. The median ratio is 1.22, and the mean wall-clock times are 1629.37 ± 16.23 seconds and 2150.53 ± 113.56 seconds.

On run 1 alone, 6.8 is slower than 5.15. In the `kbest` column, 41 of 42 rows are higher on 6.8. Leaving out the `ref` and `cpu` calibration rows, 39 of 40 are higher, and the median of those 40 ratios is 1.25. The one lower `kbest` is `select`, at 0.89 times the 5.15 time. The `select` average is 1.09 times the 5.15 average, so that cell is not a speedup. The full table is `results/comparison.md`. Rebuild it with:

```bash
python week2/compare_results.py
```

The wall-clock ratio is 2238.18 / 1619.62 = 1.38. The suite took about 38% longer on 6.8.

The size of the gap depends on the test:

- `mmap` is the large gap. `kbest` is 1.60 times on small, 1.84 times on mid, 1.81 times on big, and 1.76 times on huge. The averages move the same way, and big `mmap` average reaches 2.45 times.
- Larger `fork` tests are next. `big fork` `kbest` is 1.47 times and its average is 1.79 times. `huge fork` average is 1.75 times.
- `getpid` and context switch `kbest` are both 1.26 times. The userspace `cpu` row is also 1.26 times, so a gap of about 1.2 times is the size the virtual machine itself can produce between these two runs. `mmap` and the larger `fork` tests sit above that.
- `select`, `poll`, and `epoll` stay between 0.89 and 1.11 on `kbest`. That spread is smaller than the `cpu` row.

Averages move around more than `kbest`. `huge page fault` average is 0.77 times and `epoll big` average is 0.76 times, while both `kbest` values are still higher on 6.8 (1.33 and 1.11). One run is too little to read those average drops as speedups. On both kernels the page-fault and `fork` averages sit well above `kbest`, which is the slow samples inside the virtual machine.

## What this decides

The paper's main figure compares Linux 3.0 through 4.20 with Linux 4.0 on a physical server. Both kernels measured here are newer than that range, and the two builds from inside that range do not boot. Figure 1 stays inconclusive on this data.

This week shows a smaller claim. On one virtual machine, with Ubuntu's own kernels and three runs each, 6.8.0-138-generic is slower than 5.15.0-203-generic on 41 of 42 `kbest` rows. The extra cost is largest for `mmap` and for `fork` of a larger process. `select` is the one row whose three-run mean is lower on 6.8, at 0.91 times the 5.15 mean.

## Files

- `results/LEBenchoutput.5.15.0-203-generic.csv` — text copied from the guest
- `results/LEBenchoutput.6.8.0-138-generic.csv` — same rows as the guest log; see `results/SOURCE.txt`
- `results/comparison.md` — table written by `compare_results.py`
- `results/SOURCE.txt` — where each file came from
- `screenshots/5.15.0-203-generic-finished.jpg` — 5.15 run finished, 1619.62 s
- `screenshots/6.8.0-138-generic-finished.jpg` — 6.8 run finished, 2238.18 s
- `screenshots/grub-4.4.302-selected.jpg` — GRUB, 4.4.302 selected
- `screenshots/4.4.302-loading-initial-ramdisk.png` — 4.4.302 stopped at `Loading initial ramdisk`
- `screenshots/grub-4.15.18-selected.jpg` — GRUB, 4.15.18 selected
- `screenshots/4.15.18-loading-initial-ramdisk.png` — 4.15.18 stopped at `Loading initial ramdisk`
- `three-runs/` — six original CSV logs, three per booting kernel, plus `summary.md` and `wallclock.txt`

## Still open

The three runs for 5.15 and 6.8 are done. The extension is not. The plan is to repeat LEBench on 5.15 with one boot setting changed, `mitigations=off`, and compare it with the three default runs above.

`context siwtch` is the label LEBench prints. The table keeps that spelling so each row matches the CSV.
