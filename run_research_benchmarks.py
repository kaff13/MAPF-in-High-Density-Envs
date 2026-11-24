"""Run the five PHANS ideas with a shared, resumable 15-second benchmark.

python run_research_benchmarks.py --plan
python run_research_benchmarks.py
python run_research_benchmarks.py --report-only

Default: six maps, densities 50/75/90/95, ten seeds (100..109) per cell.
240 scenarios and 1680 attempts run through four parallel workers. The
idealized maximum planning wall time is 105 minutes, plus setup, validation,
and report generation. Use --workers to match the available CPU cores.
PHANS is measured once per scenario; execution commitment includes h2 and h4.
Repeat the command to resume. Outputs live in benchmark-results/phans-15s-10x4 and
research/<idea>/results/15s/<campaign-id>/report.html.
"""
from benchmark.campaign import main


if __name__ == "__main__":
    raise SystemExit(main())
