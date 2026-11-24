# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 40/40 | 100.0% | 0.03387 s | 16 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | h2 | 10/10 | 100.0% | 0.01595 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | h2 | 10/10 | 100.0% | 0.02638 s | 12.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | h2 | 10/10 | 100.0% | 0.06097 s | 20 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | h2 | 10/10 | 100.0% | 0.05288 s | 26.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 40/40 | 0 | 0 | 0 | 1.119x | 0 |
| toyota-env1 | 50% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.124x | 0 |
| toyota-env1 | 75% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.241x | 0 |
| toyota-env1 | 90% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.102x | 1 |
| toyota-env1 | 95% | 2 | h2 | 10/10 | 0 | 0 | 0 | 1.079x | 1 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h2 | 0 | 0 | 10.65 | 0 | 40 / 40 |
| toyota-env1 | 50% | h2 | 0 | 0 | 11.02 | 0 | 10 / 10 |
| toyota-env1 | 75% | h2 | 0 | 0 | 19.42 | 0 | 10 / 10 |
| toyota-env1 | 90% | h2 | 0 | 0 | 9.233 | -7.738 | 10 / 10 |
| toyota-env1 | 95% | h2 | 0 | 0 | 7.151 | -3.929 | 10 / 10 |
