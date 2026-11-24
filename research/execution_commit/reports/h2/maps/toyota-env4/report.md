# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 22/40 | 55.0% | 7.61 s | 77.5 | 18 / 0 / 0 / 0 |
| all | — | — | phans | 16/40 | 40.0% | 10.91 s | 58 | 24 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | h2 | 8/10 | 80.0% | 4.276 s | 45 | 2 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 8/10 | 80.0% | 6.476 s | 44 | 2 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | h2 | 0/10 | 0.0% | — | — | 10 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 1/10 | 10.0% | 12.52 s | 60 | 9 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | h2 | 5/10 | 50.0% | 11.64 s | 77 | 5 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | h2 | 9/10 | 90.0% | 8.297 s | 104 | 1 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 7/10 | 70.0% | 11.52 s | 97 | 3 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h2 | 16/40 | 0 | 6 | 18 | 1.445x | 4.5 |
| toyota-env4 | 50% | 12 | h2 | 8/10 | 0 | 0 | 2 | 1.482x | 2.5 |
| toyota-env4 | 75% | 12 | h2 | 0/10 | 0 | 0 | 10 | — | — |
| toyota-env4 | 90% | 12 | h2 | 1/10 | 0 | 4 | 5 | 1.578x | 5 |
| toyota-env4 | 95% | 12 | h2 | 7/10 | 0 | 2 | 1 | 1.437x | 6 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h2 | 15 | 37.5 | 30.79 | -6.842 | 16 / 16 |
| toyota-env4 | 50% | h2 | 0 | 0 | 32.21 | -5.78 | 8 / 8 |
| toyota-env4 | 75% | h2 | 0 | — | — | — | 0 / 0 |
| toyota-env4 | 90% | h2 | 40 | 400 | 36.63 | -8.333 | 1 / 1 |
| toyota-env4 | 95% | h2 | 20 | 28.57 | 30.43 | -6.667 | 7 / 7 |
