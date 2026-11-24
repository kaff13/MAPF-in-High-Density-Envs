# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| all | — | — | h4 | 40/40 | 100.0% | 0.04625 s | 19.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | h4 | 10/10 | 100.0% | 0.01179 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | h4 | 10/10 | 100.0% | 0.05248 s | 17 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | h4 | 10/10 | 100.0% | 0.06865 s | 25 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | h4 | 10/10 | 100.0% | 0.05111 s | 44 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 40/40 | 0 | 0 | 0 | 1.361x | 2.5 |
| toyota-env2 | 50% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.372x | 1 |
| toyota-env2 | 75% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.292x | 2 |
| toyota-env2 | 90% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.635x | 3 |
| toyota-env2 | 95% | 2 | h4 | 10/10 | 0 | 0 | 0 | 1.255x | 9 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h4 | 0 | 0 | 26.51 | -13.81 | 40 / 40 |
| toyota-env2 | 50% | h4 | 0 | 0 | 27.07 | -9.583 | 10 / 10 |
| toyota-env2 | 75% | h4 | 0 | 0 | 22.49 | -12.13 | 10 / 10 |
| toyota-env2 | 90% | h4 | 0 | 0 | 38.82 | -13.69 | 10 / 10 |
| toyota-env2 | 95% | h4 | 0 | 0 | 20.34 | -24.04 | 10 / 10 |
