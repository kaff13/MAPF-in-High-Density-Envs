# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 2/40 | 5.0% | 13.98 s | 80.5 | 38 / 0 / 0 / 0 |
| all | — | — | phans | 0/40 | 0.0% | — | — | 40 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | detour | 2/10 | 20.0% | 13.98 s | 80.5 | 8 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | detour | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | detour | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | detour | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | detour | 0/40 | 0 | 2 | 38 | — | — |
| pillars-70x42 | 50% | 12 | detour | 0/10 | 0 | 2 | 8 | — | — |
| pillars-70x42 | 75% | 12 | detour | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 90% | 12 | detour | 0/10 | 0 | 0 | 10 | — | — |
| pillars-70x42 | 95% | 12 | detour | 0/10 | 0 | 0 | 10 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | detour | 5 | — | — | — | 0 / 0 |
| pillars-70x42 | 50% | detour | 20 | — | — | — | 0 / 0 |
| pillars-70x42 | 75% | detour | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 90% | detour | 0 | — | — | — | 0 / 0 |
| pillars-70x42 | 95% | detour | 0 | — | — | — | 0 / 0 |
