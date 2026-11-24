# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 19/40 | 47.5% | 8.631 s | 94 | 21 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | engineering | 10/10 | 100.0% | 5.168 s | 91.5 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | engineering | 9/10 | 90.0% | 10.82 s | 96 | 1 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | engineering | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | engineering | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | engineering | 0/40 | 0 | 19 | 21 | — | — |
| pillars-70x42 | 50% | 12 | engineering | 0/10 | 0 | 10 | 0 | — | — |
| pillars-70x42 | 75% | 12 | engineering | 0/10 | 0 | 9 | 1 | — | — |
| pillars-70x42 | 90% | 12 | engineering | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 95% | 12 | engineering | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | engineering | 47.5 | — | — | — | 0 / 0 |
| pillars-70x42 | 50% | engineering | 100 | — | — | — | 0 / 0 |
| pillars-70x42 | 75% | engineering | 90 | — | — | — | 0 / 0 |
| pillars-70x42 | 90% | engineering | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 95% | engineering | 0 | — | — | — | 0 / 0 |
