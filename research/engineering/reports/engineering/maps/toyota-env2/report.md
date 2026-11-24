# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| all | — | — | engineering | 40/40 | 100.0% | 0.01825 s | 17 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | engineering | 10/10 | 100.0% | 0.006186 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | engineering | 10/10 | 100.0% | 0.01926 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | engineering | 10/10 | 100.0% | 0.03401 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | engineering | 10/10 | 100.0% | 0.01825 s | 35 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 40/40 | 0 | 0 | 0 | 3.762x | 0 |
| toyota-env2 | 50% | 2 | engineering | 10/10 | 0 | 0 | 0 | 3.037x | 0 |
| toyota-env2 | 75% | 2 | engineering | 10/10 | 0 | 0 | 0 | 4.351x | 0 |
| toyota-env2 | 90% | 2 | engineering | 10/10 | 0 | 0 | 0 | 4.143x | 0 |
| toyota-env2 | 95% | 2 | engineering | 10/10 | 0 | 0 | 0 | 3.349x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | engineering | 0 | 0 | 73.42 | 0 | 40 / 40 |
| toyota-env2 | 50% | engineering | 0 | 0 | 67.07 | 0 | 10 / 10 |
| toyota-env2 | 75% | engineering | 0 | 0 | 76.79 | 0 | 10 / 10 |
| toyota-env2 | 90% | engineering | 0 | 0 | 75.85 | 0 | 10 / 10 |
| toyota-env2 | 95% | engineering | 0 | 0 | 70.13 | 0 | 10 / 10 |
