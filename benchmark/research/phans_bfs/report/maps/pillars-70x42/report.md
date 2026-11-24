# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 37/40 | 92.5% | 105.7 s | 102 | 3 / 0 / 0 / 0 |
| all | — | — | phans_bfs | 34/40 | 85.0% | 99.87 s | 102 | 6 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans | 10/10 | 100.0% | 27.27 s | 93.5 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 50% | 12 | phans_bfs | 10/10 | 100.0% | 33.19 s | 93.5 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans | 10/10 | 100.0% | 75.79 s | 96 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 75% | 12 | phans_bfs | 9/10 | 90.0% | 81.65 s | 101 | 1 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans | 7/10 | 70.0% | 402.8 s | 103 | 3 / 0 / 0 / 0 |
| pillars-70x42 | 90% | 12 | phans_bfs | 5/10 | 50.0% | 431.7 s | 102 | 5 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans | 10/10 | 100.0% | 206.1 s | 138.5 | 0 / 0 / 0 / 0 |
| pillars-70x42 | 95% | 12 | phans_bfs | 10/10 | 100.0% | 258.6 s | 137.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans_bfs | 34/40 | 3 | 0 | 3 | 0.8612x | 0 |
| pillars-70x42 | 50% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8309x | 0 |
| pillars-70x42 | 75% | 12 | phans_bfs | 9/10 | 1 | 0 | 0 | 0.8675x | 0 |
| pillars-70x42 | 90% | 12 | phans_bfs | 5/10 | 2 | 0 | 3 | 0.9547x | -1 |
| pillars-70x42 | 95% | 12 | phans_bfs | 10/10 | 0 | 0 | 0 | 0.8798x | 0.5 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | phans_bfs | -7.5 | -8.108 | -16.12 | 0 | 34 / 34 |
| pillars-70x42 | 50% | phans_bfs | 0 | 0 | -20.37 | 0 | 10 / 10 |
| pillars-70x42 | 75% | phans_bfs | -10 | -10 | -15.27 | 0 | 9 / 9 |
| pillars-70x42 | 90% | phans_bfs | -20 | -28.57 | -4.742 | 1 | 5 / 5 |
| pillars-70x42 | 95% | phans_bfs | 0 | 0 | -13.89 | -0.3968 | 10 / 10 |
