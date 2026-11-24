# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 7.059 s | 58.5 | 0 / 0 / 0 / 0 |
| all | — | — | phans_bfs | 40/40 | 100.0% | 8.124 s | 59.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 10/10 | 100.0% | 2.483 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans_bfs | 10/10 | 100.0% | 2.847 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 10/10 | 100.0% | 18.81 s | 48.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans_bfs | 10/10 | 100.0% | 21.77 s | 48.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 10/10 | 100.0% | 10.28 s | 69.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans_bfs | 10/10 | 100.0% | 10.39 s | 68.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 10/10 | 100.0% | 4.933 s | 103.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans_bfs | 10/10 | 100.0% | 6.309 s | 102.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans_bfs | 40/40 | 0 | 0 | 0 | 0.8477x | 0 |
| toyota-env4 | 50% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8599x | 0 |
| toyota-env4 | 75% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.9404x | 0 |
| toyota-env4 | 90% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8818x | 1.5 |
| toyota-env4 | 95% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.7835x | -0.5 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | phans_bfs | 0 | 0 | -17.97 | 0 | 40 / 40 |
| toyota-env4 | 50% | phans_bfs | 0 | 0 | -16.31 | 0 | 10 / 10 |
| toyota-env4 | 75% | phans_bfs | 0 | 0 | -6.656 | 0 | 10 / 10 |
| toyota-env4 | 90% | phans_bfs | 0 | 0 | -13.61 | -2.024 | 10 / 10 |
| toyota-env4 | 95% | phans_bfs | 0 | 0 | -27.76 | 0.4545 | 10 / 10 |
