# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 19/40 | 47.5% | 6.226 s | 54 | 21 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | detour | 10/10 | 100.0% | 2.056 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | detour | 1/10 | 10.0% | 14.55 s | 45 | 9 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | detour | 2/10 | 20.0% | 13.04 s | 73 | 8 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | detour | 6/10 | 60.0% | 8.862 s | 95.5 | 4 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 13/40 | 3 | 6 | 18 | 1.809x | -1 |
| toyota-env4 | 50% | 12 | detour | 8/10 | 0 | 2 | 0 | 2.111x | -1 |
| toyota-env4 | 75% | 12 | detour | 0/10 | 0 | 1 | 9 | — | — |
| toyota-env4 | 90% | 12 | detour | 0/10 | 1 | 2 | 7 | — | — |
| toyota-env4 | 95% | 12 | detour | 5/10 | 2 | 1 | 2 | 1.54x | -4 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | detour | 7.5 | 18.75 | 44.73 | 2.381 | 13 / 13 |
| toyota-env4 | 50% | detour | 20 | 25 | 52.28 | 2.277 | 8 / 8 |
| toyota-env4 | 75% | detour | 10 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | detour | 10 | 100 | — | — | 0 / 0 |
| toyota-env4 | 95% | detour | -10 | -14.29 | 35.06 | 4.706 | 5 / 5 |
