# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 24/40 | 60.0% | 7.384 s | 58 | 16 / 0 / 0 / 0 |
| all | — | — | potential2 | 29/40 | 72.5% | 7.421 s | 55 | 11 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 4.124 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | potential2 | 10/10 | 100.0% | 2.804 s | 45.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | potential2 | 3/10 | 30.0% | 10.75 s | 43 | 7 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 1/10 | 10.0% | 5.247 s | 38 | 9 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | potential2 | 7/10 | 70.0% | 10 s | 56 | 3 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 6/10 | 60.0% | 13.13 s | 61.5 | 4 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | potential2 | 9/10 | 90.0% | 7.458 s | 84 | 1 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 7/10 | 70.0% | 10.35 s | 89 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 23/40 | 1 | 6 | 10 | 1.061x | -2 |
| toyota-env3 | 50% | 12 | potential2 | 10/10 | 0 | 0 | 0 | 1.142x | -0.5 |
| toyota-env3 | 75% | 12 | potential2 | 1/10 | 0 | 2 | 7 | 0.3613x | 1 |
| toyota-env3 | 90% | 12 | potential2 | 5/10 | 1 | 2 | 2 | 1.035x | -5 |
| toyota-env3 | 95% | 12 | potential2 | 7/10 | 0 | 2 | 1 | 1.217x | -3 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | potential2 | 12.5 | 20.83 | 5.744 | 2.247 | 23 / 23 |
| toyota-env3 | 50% | potential2 | 0 | 0 | 9.783 | 1.042 | 10 / 10 |
| toyota-env3 | 75% | potential2 | 20 | 200 | -176.8 | -2.632 | 1 / 1 |
| toyota-env3 | 90% | potential2 | 10 | 16.67 | 3.352 | 6.667 | 5 / 5 |
| toyota-env3 | 95% | potential2 | 20 | 28.57 | 17.8 | 3.571 | 7 / 7 |
