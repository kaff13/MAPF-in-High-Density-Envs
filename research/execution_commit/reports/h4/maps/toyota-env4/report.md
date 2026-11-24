# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 32/40 | 80.0% | 6.201 s | 75.5 | 8 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | h4 | 10/10 | 100.0% | 5.115 s | 51.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | h4 | 4/10 | 40.0% | 12.7 s | 60.5 | 6 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | h4 | 8/10 | 80.0% | 8.867 s | 85 | 2 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | h4 | 10/10 | 100.0% | 5.297 s | 113.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 16/40 | 0 | 16 | 8 | 2.126x | 11 |
| toyota-env4 | 50% | 12 | h4 | 8/10 | 0 | 2 | 0 | 1.541x | 5 |
| toyota-env4 | 75% | 12 | h4 | 0/10 | 0 | 4 | 6 | — | — |
| toyota-env4 | 90% | 12 | h4 | 1/10 | 0 | 7 | 2 | 2.114x | 18 |
| toyota-env4 | 95% | 12 | h4 | 7/10 | 0 | 3 | 0 | 2.591x | 13 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h4 | 40 | 100 | 52.96 | -14.79 | 16 / 16 |
| toyota-env4 | 50% | h4 | 20 | 25 | 35.11 | -11.9 | 8 / 8 |
| toyota-env4 | 75% | h4 | 40 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | h4 | 70 | 700 | 52.69 | -30 | 1 / 1 |
| toyota-env4 | 95% | h4 | 30 | 42.86 | 61.41 | -15.29 | 7 / 7 |
