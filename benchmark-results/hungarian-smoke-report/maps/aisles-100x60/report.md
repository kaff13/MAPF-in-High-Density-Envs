# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 2/40 | 5.0% | 115.6 s | 136 | 38 / 0 / 0 / 0 |
| all | — | — | candidate | 6/40 | 15.0% | 120.6 s | 121.5 | 34 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | phans | 2/10 | 20.0% | 115.6 s | 136 | 8 / 0 / 0 / 0 |
| aisles-100x60 | 50% | 12 | candidate | 6/10 | 60.0% | 120.6 s | 121.5 | 4 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 75% | 12 | candidate | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 90% | 12 | candidate | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| aisles-100x60 | 95% | 12 | candidate | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 2/40 | 0 | 4 | 34 | 1.258x | -4 |
| aisles-100x60 | 50% | 12 | candidate | 2/10 | 0 | 4 | 4 | 1.258x | -4 |
| aisles-100x60 | 75% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 90% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 95% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 10 | 200 | 18.34 | 2.794 | 2 / 2 |
| aisles-100x60 | 50% | candidate | 40 | 200 | 18.34 | 2.794 | 2 / 2 |
| aisles-100x60 | 75% | candidate | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 90% | candidate | 0 | — | — | — | 0 / 0 |
| aisles-100x60 | 95% | candidate | 0 | — | — | — | 0 / 0 |
