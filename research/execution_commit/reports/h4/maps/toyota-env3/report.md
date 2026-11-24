# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 34/40 | 85.0% | 4.326 s | 68.5 | 6 / 0 / 0 / 0 |
| all | — | — | phans | 24/40 | 60.0% | 7.384 s | 58 | 16 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | h4 | 10/10 | 100.0% | 1.653 s | 52 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 10/10 | 100.0% | 4.124 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | h4 | 4/10 | 40.0% | 12.77 s | 51.5 | 6 / 0 / 0 / 0 |
| toyota-env3 | 75% | 12 | phans | 1/10 | 10.0% | 5.247 s | 38 | 9 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | h4 | 10/10 | 100.0% | 5.925 s | 79.5 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 6/10 | 60.0% | 13.13 s | 61.5 | 4 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | phans | 7/10 | 70.0% | 10.35 s | 89 | 3 / 0 / 0 / 0 |
| toyota-env3 | 95% | 12 | h4 | 10/10 | 100.0% | 4.326 s | 105.5 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | h4 | 24/40 | 0 | 10 | 6 | 2.224x | 10 |
| toyota-env3 | 50% | 12 | h4 | 10/10 | 0 | 0 | 0 | 1.371x | 4.5 |
| toyota-env3 | 75% | 12 | h4 | 1/10 | 0 | 3 | 6 | 2.188x | 12 |
| toyota-env3 | 90% | 12 | h4 | 6/10 | 0 | 4 | 0 | 2.676x | 8.5 |
| toyota-env3 | 95% | 12 | h4 | 7/10 | 0 | 3 | 0 | 2.377x | 12 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | h4 | 25 | 41.67 | 55.04 | -12.67 | 24 / 24 |
| toyota-env3 | 50% | h4 | 0 | 0 | 27.01 | -10.68 | 10 / 10 |
| toyota-env3 | 75% | h4 | 30 | 300 | 54.29 | -31.58 | 1 / 1 |
| toyota-env3 | 90% | h4 | 40 | 66.67 | 62.63 | -13.45 | 6 / 6 |
| toyota-env3 | 95% | h4 | 30 | 42.86 | 57.93 | -13.98 | 7 / 7 |
