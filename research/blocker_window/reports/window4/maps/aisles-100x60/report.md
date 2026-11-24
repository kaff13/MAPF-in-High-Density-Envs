# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | window4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | window4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | window4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | window4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | window4 | 0/40 | 0 | 0 | 40 | — | — |
| aisles-100x60 | 50% | 12 | window4 | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 75% | 12 | window4 | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 90% | 12 | window4 | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 95% | 12 | window4 | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | window4 | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 50% | window4 | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 75% | window4 | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 90% | window4 | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 95% | window4 | 0 | — | — | — | 0 / 0 |
