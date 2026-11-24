# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 40/40 | 100.0% | 0.06266 s | 17.5 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | potential2 | 10/10 | 100.0% | 0.0228 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | potential2 | 10/10 | 100.0% | 0.05774 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | potential2 | 10/10 | 100.0% | 0.1262 s | 22 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | potential2 | 10/10 | 100.0% | 0.08157 s | 35.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | potential2 | 40/40 | 0 | 0 | 0 | 0.8512x | 0 |
| toyota-env2 | 50% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.7581x | 0 |
| toyota-env2 | 75% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.981x | 0.5 |
| toyota-env2 | 90% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 1.132x | 0 |
| toyota-env2 | 95% | 2 | potential2 | 10/10 | 0 | 0 | 0 | 0.8221x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | potential2 | 0 | 0 | -17.51 | 0 | 40 / 40 |
| toyota-env2 | 50% | potential2 | 0 | 0 | -31.92 | 0 | 10 / 10 |
| toyota-env2 | 75% | potential2 | 0 | 0 | -2.701 | -5 | 10 / 10 |
| toyota-env2 | 90% | potential2 | 0 | 0 | 11.03 | 0 | 10 / 10 |
| toyota-env2 | 95% | potential2 | 0 | 0 | -21.69 | 0 | 10 / 10 |
