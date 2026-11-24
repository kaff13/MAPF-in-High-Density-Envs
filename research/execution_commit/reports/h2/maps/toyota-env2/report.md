# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| all | — | — | h2 | 40/40 | 100.0% | 0.05066 s | 19 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | h2 | 10/10 | 100.0% | 0.01509 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | h2 | 10/10 | 100.0% | 0.05315 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | h2 | 10/10 | 100.0% | 0.08954 s | 24.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | h2 | 10/10 | 100.0% | 0.05066 s | 38 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 40/40 | 0 | 0 | 0 | 1.279x | 1 |
| toyota-env2 | 50% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.188x | 0 |
| toyota-env2 | 75% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.22x | 0.5 |
| toyota-env2 | 90% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.441x | 2 |
| toyota-env2 | 95% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.283x | 3.5 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h2 | 0 | 0 | 21.84 | -6.559 | 40 / 40 |
| toyota-env2 | 50% | h2 | 0 | 0 | 15.73 | 0 | 10 / 10 |
| toyota-env2 | 75% | h2 | 0 | 0 | 17.79 | -3.333 | 10 / 10 |
| toyota-env2 | 90% | h2 | 0 | 0 | 30.36 | -7.294 | 10 / 10 |
| toyota-env2 | 95% | h2 | 0 | 0 | 22.06 | -8.611 | 10 / 10 |
