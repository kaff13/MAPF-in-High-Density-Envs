# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 28/30 | 93.3% | 12.68 s | 72.5 | 2 / 0 / 0 / 0 |
| all | — | — | candidate | 26/30 | 86.7% | 51.62 s | 67 | 4 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 8/10 | 80.0% | 79.11 s | 49 | 2 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | candidate | 10/10 | 100.0% | 32.28 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 10/10 | 100.0% | 13.84 s | 67 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | candidate | 7/10 | 70.0% | 52.26 s | 67 | 3 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 10/10 | 100.0% | 6.051 s | 98 | 0 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | candidate | 9/10 | 90.0% | 82.17 s | 95 | 1 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 24/30 | 4 | 2 | 0 | 0.2358x | 1.5 |
| toyota-env3 | 75% | 12 | candidate | 8/10 | 0 | 2 | 0 | 3.267x | 0 |
| toyota-env3 | 90% | 12 | candidate | 7/10 | 3 | 0 | 0 | 0.2355x | 7 |
| toyota-env3 | 95% | 12 | candidate | 9/10 | 1 | 0 | 0 | 0.07543x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | -6.667 | -7.143 | -324 | -1.503 | 24 / 24 |
| toyota-env3 | 75% | candidate | 20 | 25 | 69.34 | 0.1751 | 8 / 8 |
| toyota-env3 | 90% | candidate | -30 | -30 | -324.7 | -10.53 | 7 / 7 |
| toyota-env3 | 95% | candidate | -10 | -10 | -1226 | 0 | 9 / 9 |
