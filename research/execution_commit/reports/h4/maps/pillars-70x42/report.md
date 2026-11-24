# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 3/40 | 7.5% | 13.27 s | 75 | 37 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | h4 | 2/10 | 20.0% | 11.14 s | 82 | 8 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | h4 | 1/10 | 10.0% | 13.27 s | 74 | 9 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | h4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | h4 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 0/40 | 0 | 3 | 37 | — | — |
| pillars-70x42 | 50% | 12 | h4 | 0/10 | 0 | 2 | 8 | — | — |
| pillars-70x42 | 75% | 12 | h4 | 0/10 | 0 | 1 | 9 | — | — |
| pillars-70x42 | 90% | 12 | h4 | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 95% | 12 | h4 | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h4 | 7.5 | — | — | — | 0 / 0 |
| pillars-70x42 | 50% | h4 | 20 | — | — | — | 0 / 0 |
| pillars-70x42 | 75% | h4 | 10 | — | — | — | 0 / 0 |
| pillars-70x42 | 90% | h4 | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 95% | h4 | 0 | — | — | — | 0 / 0 |
