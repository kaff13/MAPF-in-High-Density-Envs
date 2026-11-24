# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 30/40 | 75.0% | 6.895 s | 55.5 | 10 / 0 / 0 / 0 |
| all | — | — | phans | 24/40 | 60.0% | 7.384 s | 58 | 16 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | detour | 10/10 | 100.0% | 1.44 s | 44.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 4.124 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | detour | 3/10 | 30.0% | 12.39 s | 43 | 7 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 1/10 | 10.0% | 5.247 s | 38 | 9 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | detour | 8/10 | 80.0% | 10.94 s | 57.5 | 2 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 6/10 | 60.0% | 13.13 s | 61.5 | 4 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | detour | 9/10 | 90.0% | 7.341 s | 84 | 1 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 7/10 | 70.0% | 10.35 s | 89 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 23/40 | 1 | 7 | 9 | 1.403x | -2 |
| toyota-env3 | 50% | 12 | detour | 10/10 | 0 | 0 | 0 | 1.883x | 0 |
| toyota-env3 | 75% | 12 | detour | 1/10 | 0 | 2 | 7 | 1.368x | -2 |
| toyota-env3 | 90% | 12 | detour | 5/10 | 1 | 3 | 1 | 1.403x | -3 |
| toyota-env3 | 95% | 12 | detour | 7/10 | 0 | 2 | 1 | 1.118x | -3 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | detour | 15 | 25 | 28.73 | 3.571 | 23 / 23 |
| toyota-env3 | 50% | detour | 0 | 0 | 46.72 | 0 | 10 / 10 |
| toyota-env3 | 75% | detour | 20 | 200 | 26.92 | 5.263 | 1 / 1 |
| toyota-env3 | 90% | detour | 20 | 33.33 | 28.73 | 4.651 | 5 / 5 |
| toyota-env3 | 95% | detour | 20 | 28.57 | 10.56 | 4.286 | 7 / 7 |
