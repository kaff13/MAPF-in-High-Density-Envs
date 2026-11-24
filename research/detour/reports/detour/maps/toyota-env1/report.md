# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| all | — | — | detour | 40/40 | 100.0% | 0.03207 s | 14.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | detour | 10/10 | 100.0% | 0.01636 s | 11.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | detour | 10/10 | 100.0% | 0.02644 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | detour | 10/10 | 100.0% | 0.06676 s | 19 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | detour | 10/10 | 100.0% | 0.05387 s | 24 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 40/40 | 0 | 0 | 0 | 1.004x | 0 |
| toyota-env1 | 50% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.12x | 0 |
| toyota-env1 | 75% | 2 | detour | 10/10 | 0 | 0 | 0 | 1.074x | -0.5 |
| toyota-env1 | 90% | 2 | detour | 10/10 | 0 | 0 | 0 | 0.949x | 0 |
| toyota-env1 | 95% | 2 | detour | 10/10 | 0 | 0 | 0 | 0.9824x | -1 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | detour | 0 | 0 | 0.3918 | 0 | 40 / 40 |
| toyota-env1 | 50% | detour | 0 | 0 | 9.509 | 0 | 10 / 10 |
| toyota-env1 | 75% | detour | 0 | 0 | 6.57 | 2.941 | 10 / 10 |
| toyota-env1 | 90% | detour | 0 | 0 | -5.37 | 0 | 10 / 10 |
| toyota-env1 | 95% | detour | 0 | 0 | -1.963 | 4.773 | 10 / 10 |
