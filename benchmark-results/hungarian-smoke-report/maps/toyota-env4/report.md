# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 39/40 | 97.5% | 9.037 s | 60 | 1 / 0 / 0 / 0 |
| all | — | — | candidate | 40/40 | 100.0% | 28.12 s | 64 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 10/10 | 100.0% | 2.92 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | candidate | 10/10 | 100.0% | 1.967 s | 44.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 9/10 | 90.0% | 24.65 s | 50 | 1 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | candidate | 10/10 | 100.0% | 24.18 s | 52 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 10/10 | 100.0% | 13.24 s | 69.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | candidate | 10/10 | 100.0% | 39.75 s | 70 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 10/10 | 100.0% | 6.324 s | 103.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | candidate | 10/10 | 100.0% | 55.86 s | 103.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 39/40 | 0 | 1 | 0 | 0.4407x | 2 |
| toyota-env4 | 50% | 12 | candidate | 10/10 | 0 | 0 | 0 | 1.434x | 0.5 |
| toyota-env4 | 75% | 12 | candidate | 9/10 | 0 | 1 | 0 | 1.62x | 2 |
| toyota-env4 | 90% | 12 | candidate | 10/10 | 0 | 0 | 0 | 0.3342x | 4.5 |
| toyota-env4 | 95% | 12 | candidate | 10/10 | 0 | 0 | 0 | 0.1446x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 2.5 | 2.564 | -126.9 | -4 | 39 / 39 |
| toyota-env4 | 50% | candidate | 0 | 0 | 29.09 | -1 | 10 / 10 |
| toyota-env4 | 75% | candidate | 10 | 11.11 | 38.27 | -4 | 9 / 9 |
| toyota-env4 | 90% | candidate | 0 | 0 | -199.2 | -7.129 | 10 / 10 |
| toyota-env4 | 95% | candidate | 0 | 0 | -592.5 | 0 | 10 / 10 |
