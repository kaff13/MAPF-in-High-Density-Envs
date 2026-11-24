# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 40/40 | 100.0% | 0.05004 s | 16.5 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | detour | 10/10 | 100.0% | 0.01489 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | detour | 10/10 | 100.0% | 0.04455 s | 14.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | detour | 10/10 | 100.0% | 0.1268 s | 22 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | detour | 10/10 | 100.0% | 0.06086 s | 33.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 40/40 | 0 | 0 | 0 | 1.031x | 0 |
| toyota-env2 | 50% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.007x | 0 |
| toyota-env2 | 75% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.284x | -1 |
| toyota-env2 | 90% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.005x | 0 |
| toyota-env2 | 95% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.031x | -1.5 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | detour | 0 | 0 | 3.002 | 0 | 40 / 40 |
| toyota-env2 | 50% | detour | 0 | 0 | 0.6709 | 0 | 10 / 10 |
| toyota-env2 | 75% | detour | 0 | 0 | 22.1 | 6.066 | 10 / 10 |
| toyota-env2 | 90% | detour | 0 | 0 | 0.4571 | 0 | 10 / 10 |
| toyota-env2 | 95% | detour | 0 | 0 | 3.002 | 4.94 | 10 / 10 |
