This research implementation explores Modification B of PHANS for multi-agent pathfinding in high-density environments (MAPF-HD). The baseline PHANS algorithm selects evacuation cells for obstructing agents sequentially using a greedy strategy. PHANS-Hungarian replaces that selection step with a global assignment computed using the Hungarian algorithm.

The goal is to investigate whether jointly assigning available free cells can reduce competition between obstructing agents and improve performance in dense environments.

> The Hungarian assignment optimizes destinations, but does not by itself guarantee conflict-free routes, deadlock avoidance, or a lower makespan.


## Repository Structure
research/

└── phans\_hungarian/

&#x20;   ├── solver.py                    # Benchmark entry point

&#x20;   ├── team\_solver.py               # Solver adapter and orchestration

&#x20;   ├── a\_star.py                    # A\* pathfinding utilities

&#x20;   ├── phans\_hungarian.py           # Hungarian-based assignment logic

&#x20;   └── README.md                    # Method description and benchmark report



The benchmark framework and shared project components remain in their original locations and are not duplicated in this research directory.


## Method
Let $B = \\{b\_1, \\dots, b\_k\\}$ be the obstructing agents considered for evacuation, and let $N = \\{n\_1, \\dots, n\_p\\}$ be the available free cells. The solver builds a cost matrix $C$, where $c\_{ij}$ is the cost of assigning free cell $n\_j$ to obstructing agent $b\_i$. The Hungarian algorithm selects an assignment that minimizes the total cost, subject to each agent receiving at most one cell and each cell being assigned to at most one agent.

Cost metric used: \[Specify the metric implemented in this version, e.g. Manhattan distance or BFS path distance.]

If the implementation uses Manhattan distance, it does not account for static walls or columns. Therefore, a geometrically close cell may be difficult or impossible to reach in the actual map.

Implementation

The benchmark entry point is solver.py. The remaining Python modules contain the solver adapter, pathfinding utilities, assignment logic, and null-agent swapping components.

To run the implementation, use the module path and entry point supported by the benchmark:

research.phans\_hungarian.solver:solve


## Results
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


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
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


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
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 45/45 | 100.0% | 0.008869 s | 14 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 45/45 | 100.0% | 0.01049 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 10% | 2 | phans | 5/5 | 100.0% | 0.005381 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 10% | 2 | candidate | 5/5 | 100.0% | 0.004167 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 20% | 2 | candidate | 5/5 | 100.0% | 0.004543 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 20% | 2 | phans | 5/5 | 100.0% | 0.005179 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 30% | 2 | phans | 5/5 | 100.0% | 0.006095 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 30% | 2 | candidate | 5/5 | 100.0% | 0.005863 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 40% | 2 | candidate | 5/5 | 100.0% | 0.00708 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 40% | 2 | phans | 5/5 | 100.0% | 0.006716 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | phans | 5/5 | 100.0% | 0.007621 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 100.0% | 0.008 s | 11 | 0 / 0 / 0 / 0 |
| toyota-env2 | 60% | 2 | candidate | 5/5 | 100.0% | 0.01371 s | 16 | 0 / 0 / 0 / 0 |
| toyota-env2 | 60% | 2 | phans | 5/5 | 100.0% | 0.01002 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 70% | 2 | phans | 5/5 | 100.0% | 0.0153 s | 15 | 0 / 0 / 0 / 0 |
| toyota-env2 | 70% | 2 | candidate | 5/5 | 100.0% | 0.0166 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env2 | 80% | 2 | candidate | 5/5 | 100.0% | 0.03725 s | 21 | 0 / 0 / 0 / 0 |
| toyota-env2 | 80% | 2 | phans | 5/5 | 100.0% | 0.03571 s | 18 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | phans | 5/5 | 100.0% | 0.04581 s | 25 | 0 / 0 / 0 / 0 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 100.0% | 0.05129 s | 26 | 0 / 0 / 0 / 0 |
## Paired comparison with phans
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 45/45 | 0 | 0 | 0 | 1.002x | 0 |
| toyota-env2 | 10% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.175x | 0 |
| toyota-env2 | 20% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.141x | 0 |
| toyota-env2 | 30% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.8887x | 0 |
| toyota-env2 | 40% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9486x | 0 |
| toyota-env2 | 50% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9748x | 0 |
| toyota-env2 | 60% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.7842x | 0 |
| toyota-env2 | 70% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9216x | 2 |
| toyota-env2 | 80% | 2 | candidate | 5/5 | 0 | 0 | 0 | 0.9587x | 5 |
| toyota-env2 | 90% | 2 | candidate | 5/5 | 0 | 0 | 0 | 1.018x | 0 |
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 45/45 | 100.0% | 3.278 s | 49 | 0 / 0 / 0 / 0 |
| all | — | — | candidate | 45/45 | 100.0% | 1.706 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 10% | 12 | phans | 5/5 | 100.0% | 0.6379 s | 47 | 0 / 0 / 0 / 0 |
| toyota-env3 | 10% | 12 | candidate | 5/5 | 100.0% | 0.4401 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env3 | 20% | 12 | candidate | 5/5 | 100.0% | 0.8155 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 20% | 12 | phans | 5/5 | 100.0% | 1.294 s | 47 | 0 / 0 / 0 / 0 |
| toyota-env3 | 30% | 12 | phans | 5/5 | 100.0% | 1.025 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 30% | 12 | candidate | 5/5 | 100.0% | 1.126 s | 46 | 0 / 0 / 0 / 0 |
| toyota-env3 | 40% | 12 | candidate | 5/5 | 100.0% | 1.489 s | 47 | 0 / 0 / 0 / 0 |
| toyota-env3 | 40% | 12 | phans | 5/5 | 100.0% | 1.731 s | 49 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | phans | 5/5 | 100.0% | 3.135 s | 50 | 0 / 0 / 0 / 0 |
| toyota-env3 | 50% | 12 | candidate | 5/5 | 100.0% | 2.128 s | 48 | 0 / 0 / 0 / 0 |
| toyota-env3 | 60% | 12 | candidate | 5/5 | 100.0% | 3.331 s | 51 | 0 / 0 / 0 / 0 |
| toyota-env3 | 60% | 12 | phans | 5/5 | 100.0% | 4.834 s | 53 | 0 / 0 / 0 / 0 |
| toyota-env3 | 70% | 12 | phans | 5/5 | 100.0% | 10.28 s | 55 | 0 / 0 / 0 / 0 |
| toyota-env3 | 70% | 12 | candidate | 5/5 | 100.0% | 7.947 s | 54 | 0 / 0 / 0 / 0 |
| toyota-env3 | 80% | 12 | candidate | 5/5 | 100.0% | 22.6 s | 58 | 0 / 0 / 0 / 0 |
| toyota-env3 | 80% | 12 | phans | 5/5 | 100.0% | 12.99 s | 55 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | phans | 5/5 | 100.0% | 14.17 s | 75 | 0 / 0 / 0 / 0 |
| toyota-env3 | 90% | 12 | candidate | 5/5 | 100.0% | 49.36 s | 80 | 0 / 0 / 0 / 0 |
## Paired comparison with phans
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 45/45 | 0 | 0 | 0 | 1.192x | 0 |
| toyota-env3 | 10% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.128x | 0 |
| toyota-env3 | 20% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.192x | 0 |
| toyota-env3 | 30% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.079x | -1 |
| toyota-env3 | 40% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.645x | -1 |
| toyota-env3 | 50% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.42x | -2 |
| toyota-env3 | 60% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.695x | -1 |
| toyota-env3 | 70% | 12 | candidate | 5/5 | 0 | 0 | 0 | 2.251x | -1 |
| toyota-env3 | 80% | 12 | candidate | 5/5 | 0 | 0 | 0 | 1.188x | 3 |
| toyota-env3 | 90% | 12 | candidate | 5/5 | 0 | 0 | 0 | 0.2827x | 6 |
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | — | — | phans | 39/40 | 97.5% | 9.037 s | 60 | 1 / 0 / 0 / 0 |
| all | — | — | candidate | 40/40 | 100.0% | 28.12 s | 64 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | phans | 10/10 | 100.0% | 2.92 s | 45 | 0 / 0 / 0 / 0 |
| toyota-env4 | 50% | 12 | candidate | 10/10 | 100.0% | 1.967 s | 44.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | phans | 9/10 | 90.0% | 24.65 s | 50 | 1 / 0 / 0 / 0 |
| toyota-env4 | 75% | 12 | candidate | 10/10 | 100.0% | 24.18 s | 52 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | phans | 10/10 | 100.0% | 13.24 s | 69.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 90% | 12 | candidate | 10/10 | 100.0% | 39.75 s | 70 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | phans | 10/10 | 100.0% | 6.324 s | 103.5 | 0 / 0 / 0 / 0 |
| toyota-env4 | 95% | 12 | candidate | 10/10 | 100.0% | 55.86 s | 103.5 | 0 / 0 / 0 / 0 |
## Paired comparison with phans
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 39/40 | 0 | 1 | 0 | 0.4407x | 2 |
| toyota-env4 | 50% | 12 | candidate | 10/10 | 0 | 0 | 0 | 1.434x | 0.5 |
| toyota-env4 | 75% | 12 | candidate | 9/10 | 0 | 1 | 0 | 1.62x | 2 |
| toyota-env4 | 90% | 12 | candidate | 10/10 | 0 | 0 | 0 | 0.3342x | 4.5 |
| toyota-env4 | 95% | 12 | candidate | 10/10 | 0 | 0 | 0 | 0.1446x | 0 |
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


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
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 11/30 | 15 | 2 | 2 | 1.149x | -2 |
| pillars-70x42 | 75% | 12 | candidate | 10/10 | 0 | 0 | 0 | 1.221x | -2.5 |
| pillars-70x42 | 90% | 12 | candidate | 1/10 | 5 | 2 | 2 | 1.149x | 16 |
| pillars-70x42 | 95% | 12 | candidate | 0/10 | 10 | 0 | 0 | — | — |
Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.


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
Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.


| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all | — | — | candidate | 2/40 | 0 | 4 | 34 | 1.258x | -4 |
| aisles-100x60 | 50% | 12 | candidate | 2/10 | 0 | 4 | 4 | 1.258x | -4 |
| aisles-100x60 | 75% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 90% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |
| aisles-100x60 | 95% | 12 | candidate | 0/10 | 0 | 0 | 10 | — | — |
