# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 29/40 | 72.5% | 7.047 s | 56 | 11 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | window4 | 10/10 | 100.0% | 4.538 s | 44 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | window4 | 7/10 | 70.0% | 5.449 s | 52 | 3 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | window4 | 5/10 | 50.0% | 13.19 s | 77 | 5 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | window4 | 7/10 | 70.0% | 10.13 s | 99 | 3 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 14/40 | 2 | 15 | 9 | 1.456x | 0 |
| toyota-env4 | 50% | 12 | window4 | 8/10 | 0 | 2 | 0 | 1.727x | -0.5 |
| toyota-env4 | 75% | 12 | window4 | 0/10 | 0 | 7 | 3 | — | — |
| toyota-env4 | 90% | 12 | window4 | 0/10 | 1 | 5 | 4 | — | — |
| toyota-env4 | 95% | 12 | window4 | 6/10 | 1 | 1 | 2 | 1.311x | 2 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 32.5 | 81.25 | 30.68 | 0 | 14 / 14 |
| toyota-env4 | 50% | window4 | 20 | 25 | 42.06 | 1.064 | 8 / 8 |
| toyota-env4 | 75% | window4 | 70 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | window4 | 40 | 400 | — | — | 0 / 0 |
| toyota-env4 | 95% | window4 | 0 | 0 | 23.7 | -2.198 | 6 / 6 |
