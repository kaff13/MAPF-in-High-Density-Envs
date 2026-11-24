# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.02049 s | 19 | 0 / 0 / 0 / 0 |
| all | — | — | phans_bfs | 40/40 | 100.0% | 0.02294 s | 19 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.006213 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans_bfs | 10/10 | 100.0% | 0.006793 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.0157 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans_bfs | 10/10 | 100.0% | 0.01835 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.03515 s | 24.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans_bfs | 10/10 | 100.0% | 0.04274 s | 24.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.0225 s | 33 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans_bfs | 10/10 | 100.0% | 0.02686 s | 33 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans_bfs | 40/40 | 0 | 0 | 0 | 0.8768x | 0 |
| toyota-env2 | 50% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.9008x | 0 |
| toyota-env2 | 75% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8725x | 0 |
| toyota-env2 | 90% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.862x | 0 |
| toyota-env2 | 95% | 2 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8721x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | phans_bfs | 0 | 0 | -14.05 | 0 | 40 / 40 |
| toyota-env2 | 50% | phans_bfs | 0 | 0 | -11.02 | 0 | 10 / 10 |
| toyota-env2 | 75% | phans_bfs | 0 | 0 | -14.61 | 0 | 10 / 10 |
| toyota-env2 | 90% | phans_bfs | 0 | 0 | -16.01 | 0 | 10 / 10 |
| toyota-env2 | 95% | phans_bfs | 0 | 0 | -14.66 | 0 | 10 / 10 |
