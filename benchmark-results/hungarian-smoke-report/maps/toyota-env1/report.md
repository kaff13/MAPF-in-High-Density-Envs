# MAPF-HD benchmark

| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 45/45 | 100.0% | 0.01145 s | 12 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 45/45 | 100.0% | 0.01101 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env1 | 10% | 2 | phans | 5/5 | 100.0% | 0.007107 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 10% | 2 | candidate | 5/5 | 100.0% | 0.005414 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 20% | 2 | candidate | 5/5 | 100.0% | 0.005943 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 20% | 2 | phans | 5/5 | 100.0% | 0.006808 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env1 | 30% | 2 | phans | 5/5 | 100.0% | 0.00903 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 30% | 2 | candidate | 5/5 | 100.0% | 0.00796 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 40% | 2 | candidate | 5/5 | 100.0% | 0.01019 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 40% | 2 | phans | 5/5 | 100.0% | 0.01145 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | phans | 5/5 | 100.0% | 0.01295 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 50% | 2 | candidate | 5/5 | 100.0% | 0.01402 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 60% | 2 | candidate | 5/5 | 100.0% | 0.01456 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 60% | 2 | phans | 5/5 | 100.0% | 0.01301 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 70% | 2 | phans | 5/5 | 100.0% | 0.014 s | 12 | 0 / 0 / 0 / 0 |
| toyota-env1 | 70% | 2 | candidate | 5/5 | 100.0% | 0.01883 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env1 | 80% | 2 | candidate | 5/5 | 100.0% | 0.03322 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env1 | 80% | 2 | phans | 5/5 | 100.0% | 0.02789 s | 13 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | phans | 5/5 | 100.0% | 0.04178 s | 24 | 0 / 0 / 0 / 0 |
| toyota-env1 | 90% | 2 | candidate | 5/5 | 100.0% | 0.05261 s | 25 | 0 / 0 / 0 / 0 |

## Paired comparison with phans

| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 45/45 | 0 | 0 | 0 | 1.016x | 0 |
| toyota-env1 | 10% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.313x | 0 |
| toyota-env1 | 20% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.138x | 0 |
| toyota-env1 | 30% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.151x | 0 |
| toyota-env1 | 40% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.177x | 0 |
| toyota-env1 | 50% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9558x | 0 |
| toyota-env1 | 60% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9974x | 0 |
| toyota-env1 | 70% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9176x | 1 |
| toyota-env1 | 80% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.7767x | 5 |
| toyota-env1 | 90% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.8564x | 1 |

## Relative metrics

| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | candidate | 0 | 0 | 1.564 | 0 | 45 / 45 |
| toyota-env1 | 10% | candidate | 0 | 0 | 23.81 | 0 | 5 / 5 |
| toyota-env1 | 20% | candidate | 0 | 0 | 12.13 | 0 | 5 / 5 |
| toyota-env1 | 30% | candidate | 0 | 0 | 13.13 | 0 | 5 / 5 |
| toyota-env1 | 40% | candidate | 0 | 0 | 15.05 | 0 | 5 / 5 |
| toyota-env1 | 50% | candidate | 0 | 0 | -4.629 | 0 | 5 / 5 |
| toyota-env1 | 60% | candidate | 0 | 0 | -0.2653 | 0 | 5 / 5 |
| toyota-env1 | 70% | candidate | 0 | 0 | -8.98 | -20 | 5 / 5 |
| toyota-env1 | 80% | candidate | 0 | 0 | -28.76 | -27.78 | 5 / 5 |
| toyota-env1 | 90% | candidate | 0 | 0 | -16.77 | -4.167 | 5 / 5 |
