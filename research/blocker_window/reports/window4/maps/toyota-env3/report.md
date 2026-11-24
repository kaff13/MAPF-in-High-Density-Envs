# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 24/40 | 60.0% | 7.384 s | 58 | 16 / 0 / 0 / 0 |
| all | — | — | window4 | 40/40 | 100.0% | 4.584 s | 59 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 4.124 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | window4 | 10/10 | 100.0% | 2.279 s | 45.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | window4 | 10/10 | 100.0% | 2.926 s | 51.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 1/10 | 10.0% | 5.247 s | 38 | 9 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | window4 | 10/10 | 100.0% | 6.594 s | 74.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 6/10 | 60.0% | 13.13 s | 61.5 | 4 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | window4 | 10/10 | 100.0% | 6.472 s | 91 | 0 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 7/10 | 70.0% | 10.35 s | 89 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 24/40 | 0 | 16 | 0 | 1.72x | 0 |
| toyota-env3 | 50% | 12 | window4 | 10/10 | 0 | 0 | 0 | 1.392x | 0 |
| toyota-env3 | 75% | 12 | window4 | 1/10 | 0 | 9 | 0 | 2.698x | -1 |
| toyota-env3 | 90% | 12 | window4 | 6/10 | 0 | 4 | 0 | 1.958x | 5 |
| toyota-env3 | 95% | 12 | window4 | 7/10 | 0 | 3 | 0 | 1.509x | -1 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 40 | 66.67 | 41.87 | 0 | 24 / 24 |
| toyota-env3 | 50% | window4 | 0 | 0 | 24.3 | 0 | 10 / 10 |
| toyota-env3 | 75% | window4 | 90 | 900 | 62.94 | 2.632 | 1 / 1 |
| toyota-env3 | 90% | window4 | 40 | 66.67 | 48.87 | -8.796 | 6 / 6 |
| toyota-env3 | 95% | window4 | 30 | 42.86 | 33.73 | 1.19 | 7 / 7 |
