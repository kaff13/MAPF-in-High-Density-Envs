# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 40/40 | 100.0% | 2.265 s | 63 | 0 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | engineering | 10/10 | 100.0% | 0.8628 s | 46.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | engineering | 10/10 | 100.0% | 3.012 s | 54 | 0 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | engineering | 10/10 | 100.0% | 2.84 s | 71 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | engineering | 10/10 | 100.0% | 2.014 s | 100 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 16/40 | 0 | 24 | 0 | 6.588x | 0 |
| toyota-env4 | 50% | 12 | engineering | 8/10 | 0 | 2 | 0 | 6.899x | 0 |
| toyota-env4 | 75% | 12 | engineering | 0/10 | 0 | 10 | 0 | — | — |
| toyota-env4 | 90% | 12 | engineering | 1/10 | 0 | 9 | 0 | 7.089x | 0 |
| toyota-env4 | 95% | 12 | engineering | 7/10 | 0 | 3 | 0 | 5.788x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | engineering | 60 | 150 | 84.82 | 0 | 16 / 16 |
| toyota-env4 | 50% | engineering | 20 | 25 | 85.48 | 0 | 8 / 8 |
| toyota-env4 | 75% | engineering | 100 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | engineering | 90 | 900 | 85.89 | 0 | 1 / 1 |
| toyota-env4 | 95% | engineering | 30 | 42.86 | 82.72 | 0 | 7 / 7 |
