# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 20/20 | 100.0% | 0.04987 s | 19 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 20/20 | 100.0% | 0.05095 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 5/5 | 100.0% | 0.02297 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | candidate | 5/5 | 100.0% | 0.01709 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | candidate | 5/5 | 100.0% | 0.03285 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 5/5 | 100.0% | 0.02234 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 5/5 | 100.0% | 0.05422 s | 24 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | candidate | 5/5 | 100.0% | 0.09491 s | 25 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | candidate | 5/5 | 100.0% | 0.07657 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 5/5 | 100.0% | 0.04773 s | 34 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 20/20 | 0 | 0 | 0 | 0.904x | 1 |
| toyota-env1 | 50% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.169x | 0 |
| toyota-env1 | 75% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9242x | 4 |
| toyota-env1 | 90% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.8816x | 1 |
| toyota-env1 | 95% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.6967x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 0 | 0 | -10.67 | -6.137 | 20 / 20 |
| toyota-env1 | 50% | candidate | 0 | 0 | 14.47 | 0 | 5 / 5 |
| toyota-env1 | 75% | candidate | 0 | 0 | -8.204 | -33.33 | 5 / 5 |
| toyota-env1 | 90% | candidate | 0 | 0 | -13.43 | -4.167 | 5 / 5 |
| toyota-env1 | 95% | candidate | 0 | 0 | -43.53 | 0 | 5 / 5 |
