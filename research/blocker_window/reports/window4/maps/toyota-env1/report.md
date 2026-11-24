# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.03479 s | 15 | 0 / 0 / 0 / 0 |
| all | — | — | window4 | 40/40 | 100.0% | 0.0361 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 10/10 | 100.0% | 0.01857 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | window4 | 10/10 | 100.0% | 0.01911 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | phans | 10/10 | 100.0% | 0.02758 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 75% | 2 | window4 | 10/10 | 100.0% | 0.02714 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 10/10 | 100.0% | 0.07438 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | window4 | 10/10 | 100.0% | 0.05285 s | 20.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | phans | 10/10 | 100.0% | 0.05165 s | 26.5 | 0 / 0 / 0 / 0 |
| toyota-env1 | 95% | 2 | window4 | 10/10 | 100.0% | 0.05586 s | 25.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 40/40 | 0 | 0 | 0 | 1.026x | 0 |
| toyota-env1 | 50% | 2 | window4 | 10/10 | 0 | 0 | 0 | 1.022x | 0 |
| toyota-env1 | 75% | 2 | window4 | 10/10 | 0 | 0 | 0 | 1.127x | 0 |
| toyota-env1 | 90% | 2 | window4 | 10/10 | 0 | 0 | 0 | 0.9818x | 2 |
| toyota-env1 | 95% | 2 | window4 | 10/10 | 0 | 0 | 0 | 0.9769x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 0 | 0 | 2.56 | 0 | 40 / 40 |
| toyota-env1 | 50% | window4 | 0 | 0 | 2.159 | 0 | 10 / 10 |
| toyota-env1 | 75% | window4 | 0 | 0 | 11.24 | 0 | 10 / 10 |
| toyota-env1 | 90% | window4 | 0 | 0 | -2.231 | -9.545 | 10 / 10 |
| toyota-env1 | 95% | window4 | 0 | 0 | -2.364 | 0 | 10 / 10 |
