# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 29/40 | 72.5% | 5.823 s | 63 | 11 / 0 / 0 / 0 |
| all | — | — | phans | 24/40 | 60.0% | 7.384 s | 58 | 16 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | h2 | 10/10 | 100.0% | 2.436 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 4.124 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | h2 | 1/10 | 10.0% | 3.979 s | 37 | 9 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 1/10 | 10.0% | 5.247 s | 38 | 9 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 6/10 | 60.0% | 13.13 s | 61.5 | 4 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | h2 | 9/10 | 90.0% | 7.254 s | 66 | 1 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 7/10 | 70.0% | 10.35 s | 89 | 3 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | h2 | 9/10 | 90.0% | 6.514 s | 92 | 1 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 24/40 | 0 | 5 | 11 | 1.614x | 1 |
| toyota-env3 | 50% | 12 | h2 | 10/10 | 0 | 0 | 0 | 1.254x | 0.5 |
| toyota-env3 | 75% | 12 | h2 | 1/10 | 0 | 0 | 9 | 1.319x | -1 |
| toyota-env3 | 90% | 12 | h2 | 6/10 | 0 | 3 | 1 | 1.942x | 0 |
| toyota-env3 | 95% | 12 | h2 | 7/10 | 0 | 2 | 1 | 1.612x | 2 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h2 | 12.5 | 20.83 | 38.02 | -1.367 | 24 / 24 |
| toyota-env3 | 50% | h2 | 0 | 0 | 20.23 | -0.8772 | 10 / 10 |
| toyota-env3 | 75% | h2 | 0 | 0 | 24.17 | 2.632 | 1 / 1 |
| toyota-env3 | 90% | h2 | 30 | 50 | 48.5 | -0.3295 | 6 / 6 |
| toyota-env3 | 95% | h2 | 20 | 28.57 | 37.96 | -2.247 | 7 / 7 |
