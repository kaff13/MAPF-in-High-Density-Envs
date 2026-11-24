# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 40/40 | 100.0% | 0.06681 s | 17 | 0 / 0 / 0 / 0 |
| all | — | — | window4 | 40/40 | 100.0% | 0.05887 s | 18.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 10/10 | 100.0% | 0.01838 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | window4 | 10/10 | 100.0% | 0.01703 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | phans | 10/10 | 100.0% | 0.08668 s | 15.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 75% | 2 | window4 | 10/10 | 100.0% | 0.05309 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 10/10 | 100.0% | 0.1215 s | 23 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | window4 | 10/10 | 100.0% | 0.1017 s | 25.5 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | phans | 10/10 | 100.0% | 0.06681 s | 35 | 0 / 0 / 0 / 0 |
| toyota-env2 | 95% | 2 | window4 | 10/10 | 100.0% | 0.06255 s | 35 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 40/40 | 0 | 0 | 0 | 1.01x | 0 |
| toyota-env2 | 50% | 2 | window4 | 10/10 | 0 | 0 | 0 | 0.952x | 0 |
| toyota-env2 | 75% | 2 | window4 | 10/10 | 0 | 0 | 0 | 1.324x | 0.5 |
| toyota-env2 | 90% | 2 | window4 | 10/10 | 0 | 0 | 0 | 1.013x | 2 |
| toyota-env2 | 95% | 2 | window4 | 10/10 | 0 | 0 | 0 | 0.99x | 0 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 0 | 0 | 0.9573 | 0 | 40 / 40 |
| toyota-env2 | 50% | window4 | 0 | 0 | -5.056 | 0 | 10 / 10 |
| toyota-env2 | 75% | window4 | 0 | 0 | 24.44 | -2.941 | 10 / 10 |
| toyota-env2 | 90% | window4 | 0 | 0 | 1.262 | -9.936 | 10 / 10 |
| toyota-env2 | 95% | window4 | 0 | 0 | -1.01 | 0 | 10 / 10 |
