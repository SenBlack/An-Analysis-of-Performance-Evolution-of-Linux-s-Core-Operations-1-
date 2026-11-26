# Reproduction Setup Guide
This document records all commands to set up and run LEBench inside the Ubuntu VM.
We will collect raw latency CSV data under Linux 4.0.5 and Linux 4.15.0-112 respectively.

| Item | Paper Original Setup | Our Setup | Deviation / Reason |
| ---- | ---- | ---- | ---- |
| Guest OS | Ubuntu16.04 on physical Xeon E5 server | Ubuntu16.04 on VirtualBox VM | Resolved earlier boot failure of old 4.x kernels on Ubuntu 22.04. OS version matches the paper, but we add virtualization overhead. |
| Kernels | v4.0.5 baseline + series of later kernels | v4.0.5 and v4.15.0-112 | Reduced test set: only two kernels instead of 36. |
| Measurement | Multiple repeated runs for statistics | Single run per kernel | Results are for reference only, without statistical error bars. |
