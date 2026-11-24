# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 26/30 | 86.7% | 385.8 s | 105.5 | 4 / 0 / 0 / 0 |
| all | — | — | candidate | 13/30 | 43.3% | 106.1 s | 98 | 17 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 10/10 | 100.0% | 142.3 s | 96 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | candidate | 10/10 | 100.0% | 102 s | 96 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 6/10 | 60.0% | 692.3 s | 101.5 | 4 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | candidate | 3/10 | 30.0% | 723.5 s | 118 | 7 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 10/10 | 100.0% | 432.8 s | 138.5 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | candidate | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 11/30 | 15 | 2 | 2 | 1.149x | -2 |
| pillars-70x42 | 75% | 12 | candidate | 10/10 | 0 | 0 | 0 | 1.221x | -2.5 |
| pillars-70x42 | 90% | 12 | candidate | 1/10 | 5 | 2 | 2 | 1.149x | 16 |
| pillars-70x42 | 95% | 12 | candidate | 0/10 | 10 | 0 | 0 | — | — |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | -43.33 | -50 | 13 | 1.961 | 11 / 11 |
| pillars-70x42 | 75% | candidate | 0 | 0 | 17.11 | 2.451 | 10 / 10 |
| pillars-70x42 | 90% | candidate | -30 | -50 | 13 | -17.39 | 1 / 1 |
| pillars-70x42 | 95% | candidate | -100 | -100 | — | — | 0 / 0 |
