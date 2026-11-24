# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 6/40 | 15.0% | 12.63 s | 92 | 34 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | window4 | 1/10 | 10.0% | 11.92 s | 66 | 9 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | window4 | 2/10 | 20.0% | 11.4 s | 80.5 | 8 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | window4 | 3/10 | 30.0% | 14.38 s | 113 | 7 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | window4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 0/40 | 0 | 6 | 34 | — | — |
| pillars-70x42 | 50% | 12 | window4 | 0/10 | 0 | 1 | 9 | — | — |
| pillars-70x42 | 75% | 12 | window4 | 0/10 | 0 | 2 | 8 | — | — |
| pillars-70x42 | 90% | 12 | window4 | 0/10 | 0 | 3 | 7 | — | — |
| pillars-70x42 | 95% | 12 | window4 | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 15 | — | — | — | 0 / 0 |
| pillars-70x42 | 50% | window4 | 10 | — | — | — | 0 / 0 |
| pillars-70x42 | 75% | window4 | 20 | — | — | — | 0 / 0 |
| pillars-70x42 | 90% | window4 | 30 | — | — | — | 0 / 0 |
| pillars-70x42 | 95% | window4 | 0 | — | — | — | 0 / 0 |
