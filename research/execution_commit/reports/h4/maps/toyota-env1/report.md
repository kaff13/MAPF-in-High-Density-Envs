# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 40/40 | 100.0% | 0.02461 s | 16 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | h4 | 10/10 | 100.0% | 0.01318 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | h4 | 10/10 | 100.0% | 0.02234 s | 14 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | h4 | 10/10 | 100.0% | 0.05426 s | 21.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | h4 | 10/10 | 100.0% | 0.03835 s | 30 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 40/40 | 0 | 0 | 0 | 1.331x | 1 |
| toyota-env1 | 50% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.297x | 0 |
| toyota-env1 | 75% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.481x | 0 |
| toyota-env1 | 90% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.252x | 3.5 |
| toyota-env1 | 95% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.526x | 3.5 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h4 | 0 | 0 | 24.89 | -5.208 | 40 / 40 |
| toyota-env1 | 50% | h4 | 0 | 0 | 22.85 | 0 | 10 / 10 |
| toyota-env1 | 75% | h4 | 0 | 0 | 31.91 | 0 | 10 / 10 |
| toyota-env1 | 90% | h4 | 0 | 0 | 20.09 | -13.48 | 10 / 10 |
| toyota-env1 | 95% | h4 | 0 | 0 | 34.47 | -13.15 | 10 / 10 |
