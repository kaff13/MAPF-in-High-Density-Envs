# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.0209 s | 17.5 | 0 / 0 / 0 / 0 |
| all | — | — | phans_bfs | 40/40 | 100.0% | 0.0253 s | 17.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.007506 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans_bfs | 10/10 | 100.0% | 0.008379 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.01275 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans_bfs | 10/10 | 100.0% | 0.0153 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.02978 s | 21.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans_bfs | 10/10 | 100.0% | 0.03585 s | 21.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.02305 s | 28.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans_bfs | 10/10 | 100.0% | 0.02802 s | 28.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans_bfs | 40/40 | 0 | 0 | 0 | 0.8644x | 0 |
| toyota-env1 | 50% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.9076x | 0 |
| toyota-env1 | 75% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8624x | 0 |
| toyota-env1 | 90% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8629x | 0 |
| toyota-env1 | 95% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8309x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | phans_bfs | 0 | 0 | -15.68 | 0 | 40 / 40 |
| toyota-env1 | 50% | phans_bfs | 0 | 0 | -10.19 | 0 | 10 / 10 |
| toyota-env1 | 75% | phans_bfs | 0 | 0 | -15.96 | 0 | 10 / 10 |
| toyota-env1 | 90% | phans_bfs | 0 | 0 | -15.92 | 0 | 10 / 10 |
| toyota-env1 | 95% | phans_bfs | 0 | 0 | -20.36 | 0 | 10 / 10 |
