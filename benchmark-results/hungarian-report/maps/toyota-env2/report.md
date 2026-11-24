# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 20/20 | 100.0% | 0.04443 s | 22 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 20/20 | 100.0% | 0.04358 s | 24.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 5/5 | 100.0% | 0.01485 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 100.0% | 0.01214 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | candidate | 5/5 | 100.0% | 0.04183 s | 21 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 5/5 | 100.0% | 0.03805 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 5/5 | 100.0% | 0.08642 s | 25 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 100.0% | 0.0975 s | 26 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | candidate | 5/5 | 100.0% | 0.07885 s | 33 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 5/5 | 100.0% | 0.05472 s | 33 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 20/20 | 0 | 0 | 0 | 0.9382x | 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.233x | 0 |
| toyota-env2 | 75% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9195x | 4 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9568x | 0 |
| toyota-env2 | 95% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.8143x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 0 | 0 | -6.633 | 0 | 20 / 20 |
| toyota-env2 | 50% | candidate | 0 | 0 | 18.88 | 0 | 5 / 5 |
| toyota-env2 | 75% | candidate | 0 | 0 | -8.756 | -17.39 | 5 / 5 |
| toyota-env2 | 90% | candidate | 0 | 0 | -4.51 | 0 | 5 / 5 |
| toyota-env2 | 95% | candidate | 0 | 0 | -22.8 | 0 | 5 / 5 |
