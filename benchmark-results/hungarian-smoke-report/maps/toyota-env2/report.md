# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 45/45 | 100.0% | 0.008869 s | 14 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 45/45 | 100.0% | 0.01049 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 10% | 2 | phans | 5/5 | 100.0% | 0.005381 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 10% | 2 | candidate | 5/5 | 100.0% | 0.004167 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 20% | 2 | candidate | 5/5 | 100.0% | 0.004543 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 20% | 2 | phans | 5/5 | 100.0% | 0.005179 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 30% | 2 | phans | 5/5 | 100.0% | 0.006095 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 30% | 2 | candidate | 5/5 | 100.0% | 0.005863 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 40% | 2 | candidate | 5/5 | 100.0% | 0.00708 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 40% | 2 | phans | 5/5 | 100.0% | 0.006716 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 5/5 | 100.0% | 0.007621 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 100.0% | 0.008 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 60% | 2 | candidate | 5/5 | 100.0% | 0.01371 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 60% | 2 | phans | 5/5 | 100.0% | 0.01002 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 70% | 2 | phans | 5/5 | 100.0% | 0.0153 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 70% | 2 | candidate | 5/5 | 100.0% | 0.0166 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env2 | 80% | 2 | candidate | 5/5 | 100.0% | 0.03725 s | 21 | 0 / 0 / 0 / 0 |
| toyota-env2 | 80% | 2 | phans | 5/5 | 100.0% | 0.03571 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 5/5 | 100.0% | 0.04581 s | 25 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 100.0% | 0.05129 s | 26 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 45/45 | 0 | 0 | 0 | 1.002x | 0 |
| toyota-env2 | 10% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.175x | 0 |
| toyota-env2 | 20% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.141x | 0 |
| toyota-env2 | 30% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.8887x | 0 |
| toyota-env2 | 40% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9486x | 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9748x | 0 |
| toyota-env2 | 60% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.7842x | 0 |
| toyota-env2 | 70% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9216x | 2 |
| toyota-env2 | 80% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9587x | 5 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.018x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 0 | 0 | 0.176 | 0 | 45 / 45 |
| toyota-env2 | 10% | candidate | 0 | 0 | 14.93 | 0 | 5 / 5 |
| toyota-env2 | 20% | candidate | 0 | 0 | 12.39 | 0 | 5 / 5 |
| toyota-env2 | 30% | candidate | 0 | 0 | -12.53 | 0 | 5 / 5 |
| toyota-env2 | 40% | candidate | 0 | 0 | -5.414 | 0 | 5 / 5 |
| toyota-env2 | 50% | candidate | 0 | 0 | -2.583 | 0 | 5 / 5 |
| toyota-env2 | 60% | candidate | 0 | 0 | -27.52 | 0 | 5 / 5 |
| toyota-env2 | 70% | candidate | 0 | 0 | -8.506 | -8.696 | 5 / 5 |
| toyota-env2 | 80% | candidate | 0 | 0 | -4.306 | -20.83 | 5 / 5 |
| toyota-env2 | 90% | candidate | 0 | 0 | 1.786 | 0 | 5 / 5 |
