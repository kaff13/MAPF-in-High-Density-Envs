# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| all | — | — | engineering | 5/40 | 12.5% | 12.39 s | 126 | 35 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | engineering | 5/10 | 50.0% | 12.39 s | 126 | 5 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | engineering | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | engineering | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | engineering | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 0/40 | 0 | 5 | 35 | — | — |
| aisles-100x60 | 50% | 12 | engineering | 0/10 | 0 | 5 | 5 | — | — |
| aisles-100x60 | 75% | 12 | engineering | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 90% | 12 | engineering | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 95% | 12 | engineering | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | engineering | 12.5 | — | — | — | 0 / 0 |
| aisles-100x60 | 50% | engineering | 50 | — | — | — | 0 / 0 |
| aisles-100x60 | 75% | engineering | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 90% | engineering | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 95% | engineering | 0 | — | — | — | 0 / 0 |
