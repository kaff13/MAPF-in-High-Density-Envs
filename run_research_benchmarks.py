"""Run the five PHANS ideas with a shared, resumable 15-second benchmark.

python run_research_benchmarks.py --plan
python run_research_benchmarks.py
python run_research_benchmarks.py --report-only

Default: six maps, densities 50/75/90/95, two seeds (100..101) per cell.
48 scenarios, 336 attempts: at most 84 minutes of planning, reserving
36 minutes of a two-hour budget for setup, validation, and reports.
PHANS is measured once per scenario; execution commitment includes h2 and h4.
Repeat the command to resume. Outputs live in benchmark-results/phans-15s-2h and
research/<idea>/results/15s/<campaign-id>/report.html.
"""
from benchmark.campaign import main


if __name__ == "__main__":
    raise SystemExit(main())
