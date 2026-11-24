# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 40/40 | 100.0% | 0.01184 s | 15 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | engineering | 10/10 | 100.0% | 0.006606 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | engineering | 10/10 | 100.0% | 0.01068 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | engineering | 10/10 | 100.0% | 0.02131 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | engineering | 10/10 | 100.0% | 0.01675 s | 26.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 40/40 | 0 | 0 | 0 | 3.06x | 0 |
| toyota-env1 | 50% | 2 | engineering | 10/10 | 0 | 0 | 0 | 2.963x | 0 |
| toyota-env1 | 75% | 2 | engineering | 10/10 | 0 | 0 | 0 | 2.811x | 0 |
| toyota-env1 | 90% | 2 | engineering | 10/10 | 0 | 0 | 0 | 3.273x | 0 |
| toyota-env1 | 95% | 2 | engineering | 10/10 | 0 | 0 | 0 | 3.149x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | engineering | 0 | 0 | 67.31 | 0 | 40 / 40 |
| toyota-env1 | 50% | engineering | 0 | 0 | 66.25 | 0 | 10 / 10 |
| toyota-env1 | 75% | engineering | 0 | 0 | 64.4 | 0 | 10 / 10 |
| toyota-env1 | 90% | engineering | 0 | 0 | 69.43 | 0 | 10 / 10 |
| toyota-env1 | 95% | engineering | 0 | 0 | 68.21 | 0 | 10 / 10 |
