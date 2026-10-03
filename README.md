# Savanna retail data review

**KABOOKI MICHEAL · 2024-08-27300**

MySQL 8.4 coursework with an independently generated January–June 2026 retail dataset. Only the assignment PDF was supplied; every customer, transaction, employee and operational event in the practical analysis is fictitious.

[Portfolio PDF](output/pdf/kabooki-micheal-portfolio.pdf) · [Editable report](docs/portfolio.md)

## Evidence and navigation

| Assignment | Review location |
|---|---|
| A1–A2 diagnosis and governance | Report A1–A2; RACI and compliance CSVs in `docs/` |
| B1 architecture and modelling | Report B1; nine editable `.drawio` diagrams; `sql/01_core.sql` |
| B2 cleansing and quality | `scripts/generate_simulation.py`, `analyse_simulation.py`, `src/savanna/quality.py` |
| B3 registry MDM | Report B3; `diagrams/mdm-flows.drawio` |
| B4 ETL and history | `src/savanna/etl.py`, SQL 02, 03 and 07; simulation evidence |
| C1 metadata | `docs/data-dictionary.csv`; lineage diagram |
| C2 access and privacy | SQL 04; `evidence/mysql-tests.txt`; report DPIA and incident plan |
| C3 analytics | `dashboard/` (native `.twbx`, extract CSV, screenshots, published URL); report questions, findings and Appendix F |
| D1–D2 delivery and reflection | Report D1–D2; `docs/decision-log.csv` |

## Reproduce the analysis

Python 3.11+ handles the transformation code without third-party packages. Run from the repository root:

```sh
python3 scripts/generate_simulation.py
python3 scripts/analyse_simulation.py
python3 scripts/diagnose_simulated_etl.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
sh scripts/run_simulation_mysql.sh
sh scripts/test_mysql.sh
```

MySQL tests use Docker's official `mysql:8.4` image in disposable containers with no network or published ports. The scripts need `rg`. Test accounts are demonstration-only. Install SQL 01–04 into a fresh instance; dimension procedures own their transactions and run before fact loading. Late history corrections require a reviewed rebuild.

Seed **27300** creates 5,000 customer rows (4,100 identities), 1,200 product rows (1,140 SKUs) and 60,000 sales. Full-load replay preserves 60,000 facts. Python and MySQL reconcile UGX **1,502,003,100**, KES **609,850** and RWF **5,975,822** separately. See `evidence/simulation/results.json`, `before_after.csv`, `mysql_execution.txt` and `mysql_totals.tsv` for denominators and executed evidence. `data/synthetic/` contains small reusable software test cases, separate from the individual analysis dataset.

## PDF and figures

Install `requirements-docs.txt`, run `python3 scripts/build_diagrams.py`, then `python3 scripts/build_portfolio.py`. The PDF renderer uses the supplied cover PDF, Times New Roman from macOS supplemental fonts and Calibri from the installed Word font directory. Body text is 12pt with 20.7pt leading and one-inch margins, matching the assignment reference. The original cloud Word file is unchanged.

The report proposes central reporting, registry MDM, a two-store pilot and a UGX 444M programme. Proposed controls are distinguished from executed fixture checks. The dashboard contains only synthetic data. Published view: https://public.tableau.com/app/profile/joshua.mutesasira/viz/MichealUGXSalesDashboard/Dashboard1

AI assistance: OpenAI Codex assisted with drafting, code, diagrams and testing. Shared validation/MySQL utilities were reused from the companion portfolio and are acknowledged in the report; this dataset, written analysis and diagrams are separately developed.
