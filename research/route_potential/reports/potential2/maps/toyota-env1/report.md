# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| all | — | — | potential2 | 40/40 | 100.0% | 0.04282 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | potential2 | 10/10 | 100.0% | 0.02165 s | 9.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | potential2 | 10/10 | 100.0% | 0.04001 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | potential2 | 10/10 | 100.0% | 0.07884 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | potential2 | 10/10 | 100.0% | 0.05512 s | 26.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 40/40 | 0 | 0 | 0 | 0.8117x | 0 |
| toyota-env1 | 50% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.7672x | 0 |
| toyota-env1 | 75% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.7552x | -1 |
| toyota-env1 | 90% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.9054x | 0 |
| toyota-env1 | 95% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.9912x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | potential2 | 0 | 0 | -23.21 | 0 | 40 / 40 |
| toyota-env1 | 50% | potential2 | 0 | 0 | -30.35 | 0 | 10 / 10 |
| toyota-env1 | 75% | potential2 | 0 | 0 | -32.42 | 7.179 | 10 / 10 |
| toyota-env1 | 90% | potential2 | 0 | 0 | -10.75 | 0 | 10 / 10 |
| toyota-env1 | 95% | potential2 | 0 | 0 | -1.087 | 0 | 10 / 10 |
