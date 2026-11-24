# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 6.111 s | 57.5 | 0 / 0 / 0 / 0 |
| all | — | — | phans_bfs | 40/40 | 100.0% | 8.035 s | 57.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 2.646 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans_bfs | 10/10 | 100.0% | 3.027 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 10/10 | 100.0% | 22.04 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans_bfs | 10/10 | 100.0% | 24.24 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 10/10 | 100.0% | 10.08 s | 67 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans_bfs | 10/10 | 100.0% | 11.75 s | 67 | 0 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 10/10 | 100.0% | 4.846 s | 98 | 0 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans_bfs | 10/10 | 100.0% | 6.782 s | 98 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans_bfs | 40/40 | 0 | 0 | 0 | 0.8296x | 0 |
| toyota-env3 | 50% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8587x | 0 |
| toyota-env3 | 75% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8992x | 0 |
| toyota-env3 | 90% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8358x | 0 |
| toyota-env3 | 95% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.7396x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | phans_bfs | 0 | 0 | -20.53 | 0 | 40 / 40 |
| toyota-env3 | 50% | phans_bfs | 0 | 0 | -16.48 | 0 | 10 / 10 |
| toyota-env3 | 75% | phans_bfs | 0 | 0 | -11.22 | 0 | 10 / 10 |
| toyota-env3 | 90% | phans_bfs | 0 | 0 | -19.65 | 0 | 10 / 10 |
| toyota-env3 | 95% | phans_bfs | 0 | 0 | -35.21 | 0 | 10 / 10 |
