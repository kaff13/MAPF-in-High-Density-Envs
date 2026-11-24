# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 15/40 | 37.5% | 8.091 s | 57 | 25 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | potential2 | 8/10 | 80.0% | 4.545 s | 43.5 | 2 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | potential2 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | potential2 | 1/10 | 10.0% | 11.64 s | 57 | 9 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | potential2 | 6/10 | 60.0% | 8.541 s | 93 | 4 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 11/40 | 5 | 4 | 20 | 1.34x | -3 |
| toyota-env4 | 50% | 12 | potential2 | 6/10 | 2 | 2 | 0 | 1.206x | 1.5 |
| toyota-env4 | 75% | 12 | potential2 | 0/10 | 0 | 0 | 10 | — | — |
| toyota-env4 | 90% | 12 | potential2 | 0/10 | 1 | 1 | 8 | — | — |
| toyota-env4 | 95% | 12 | potential2 | 5/10 | 2 | 1 | 2 | 1.347x | -4 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | potential2 | -2.5 | -6.25 | 25.37 | 3.261 | 11 / 11 |
| toyota-env4 | 50% | potential2 | 0 | 0 | 16.03 | -3.423 | 6 / 6 |
| toyota-env4 | 75% | potential2 | 0 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | potential2 | 0 | 0 | — | — | 0 / 0 |
| toyota-env4 | 95% | potential2 | -10 | -14.29 | 25.77 | 4.444 | 5 / 5 |
