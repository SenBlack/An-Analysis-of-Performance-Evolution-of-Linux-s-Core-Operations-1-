# LEBench 5.15.0-203-generic vs 6.8.0-138-generic

CSV values are seconds. This table shows microseconds (seconds times 1,000,000).
Ratio = 6.8.0-138-generic / 5.15.0-203-generic. A ratio above 1 means 6.8.0-138-generic is slower.

Each column comes from one `OS_Eval` process. `kbest` and `average` are that process's own statistics. They are not the mean and standard deviation of three separate runs.

## Summary

- Rows with higher kbest on 6.8.0-138-generic: 41 of 42.
- Rows with higher kbest, leaving out `ref` and `cpu`: 39 of 40.
- Median kbest ratio, all rows: 1.257.
- Median kbest ratio, without `ref` and `cpu`: 1.251.

`ref` and `cpu` are LEBench's calibration rows. `context siwtch` is LEBench's own spelling.

| Test | 5.15.0-203-generic kbest (us) | 6.8.0-138-generic kbest (us) | kbest ratio | 5.15.0-203-generic average (us) | 6.8.0-138-generic average (us) | average ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ref | 0.017 | 0.025 | 1.471 | 0.026 | 0.032 | 1.231 |
| cpu | 2028.130 | 2547.997 | 1.256 | 2112.216 | 3182.288 | 1.507 |
| getpid | 0.359 | 0.454 | 1.265 | 0.398 | 0.564 | 1.417 |
| context siwtch | 4.233 | 5.322 | 1.257 | 4.587 | 7.584 | 1.653 |
| send | 0.759 | 0.788 | 1.038 | 0.977 | 1.118 | 1.144 |
| recv | 0.706 | 0.816 | 1.156 | 0.813 | 1.025 | 1.261 |
| big send | 9.087 | 10.858 | 1.195 | 10.482 | 14.531 | 1.386 |
| big recv | 6.812 | 8.017 | 1.177 | 8.738 | 9.388 | 1.074 |
| fork | 54.361 | 71.134 | 1.309 | 92.184 | 134.822 | 1.463 |
| fork Child | 78.975 | 103.719 | 1.313 | 131.642 | 172.453 | 1.310 |
| thr create | 5.540 | 8.452 | 1.526 | 42.621 | 49.919 | 1.171 |
| thr create Child | 10.718 | 11.933 | 1.113 | 61.905 | 70.647 | 1.141 |
| big fork | 1740.710 | 2554.212 | 1.467 | 2040.311 | 3648.769 | 1.788 |
| big fork Child | 1807.535 | 2786.576 | 1.542 | 2136.467 | 3872.923 | 1.813 |
| huge fork | 3619.558 | 4946.797 | 1.367 | 3982.643 | 6964.648 | 1.749 |
| huge fork Child | 3794.083 | 5211.892 | 1.374 | 4173.455 | 7212.584 | 1.728 |
| small write | 0.961 | 1.147 | 1.194 | 1.157 | 1.334 | 1.153 |
| small read | 0.656 | 0.754 | 1.149 | 0.905 | 0.872 | 0.964 |
| small mmap | 0.838 | 1.345 | 1.605 | 1.017 | 1.643 | 1.616 |
| small munmap | 2.692 | 3.350 | 1.244 | 3.163 | 4.662 | 1.474 |
| small page fault | 1.298 | 1.593 | 1.227 | 4.339 | 7.428 | 1.712 |
| mid write | 3.792 | 4.311 | 1.137 | 4.520 | 5.447 | 1.205 |
| mid read | 2.231 | 2.423 | 1.086 | 2.600 | 2.603 | 1.001 |
| mid mmap | 0.811 | 1.494 | 1.842 | 0.909 | 1.892 | 2.081 |
| mid munmap | 6.773 | 8.646 | 1.277 | 7.852 | 12.614 | 1.606 |
| mid page fault | 1.871 | 2.605 | 1.392 | 5.420 | 10.054 | 1.855 |
| big write | 545.057 | 662.075 | 1.215 | 788.144 | 1159.261 | 1.471 |
| big read | 354.238 | 381.669 | 1.077 | 401.349 | 412.019 | 1.027 |
| big mmap | 0.845 | 1.533 | 1.814 | 0.986 | 2.419 | 2.453 |
| big munmap | 111.377 | 154.823 | 1.390 | 129.813 | 209.537 | 1.614 |
| big page fault | 2.470 | 3.187 | 1.290 | 7.524 | 10.790 | 1.434 |
| huge write | 7601.507 | 8527.758 | 1.122 | 8197.745 | 9543.875 | 1.164 |
| huge read | 11543.982 | 15562.267 | 1.348 | 12513.794 | 19014.681 | 1.519 |
| huge mmap | 0.923 | 1.628 | 1.764 | 1.054 | 2.504 | 2.376 |
| huge munmap | 1325.229 | 1824.689 | 1.377 | 1388.740 | 2415.588 | 1.739 |
| huge page fault | 2.496 | 3.315 | 1.328 | 17.897 | 13.788 | 0.770 |
| select | 1.474 | 1.316 | 0.893 | 2.185 | 2.371 | 1.085 |
| poll | 1.050 | 1.099 | 1.047 | 1.458 | 1.443 | 0.990 |
| epoll | 1.034 | 1.086 | 1.050 | 1.374 | 1.531 | 1.114 |
| select big | 81.513 | 89.079 | 1.093 | 184.867 | 183.292 | 0.991 |
| poll big | 80.386 | 88.206 | 1.097 | 185.083 | 184.451 | 0.997 |
| epoll big | 82.873 | 91.926 | 1.109 | 241.648 | 184.216 | 0.762 |
