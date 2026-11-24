# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 1/40 | 2.5% | 12.49 s | 66 | 39 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | h2 | 1/10 | 10.0% | 12.49 s | 66 | 9 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | h2 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | h2 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | h2 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 0/40 | 0 | 1 | 39 | — | — |
| pillars-70x42 | 50% | 12 | h2 | 0/10 | 0 | 1 | 9 | — | — |
| pillars-70x42 | 75% | 12 | h2 | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 90% | 12 | h2 | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 95% | 12 | h2 | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h2 | 2.5 | — | — | — | 0 / 0 |
| pillars-70x42 | 50% | h2 | 10 | — | — | — | 0 / 0 |
| pillars-70x42 | 75% | h2 | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 90% | h2 | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 95% | h2 | 0 | — | — | — | 0 / 0 |
