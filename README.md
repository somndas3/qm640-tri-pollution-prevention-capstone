# Pollution-Prevention Actions and Next-Year Toxic Release Reduction in U.S. Manufacturing

**QM640 Data Analytics Capstone — Walsh College**
Author: Somnath Das · Advisor: Rishab Pandey · Summer 2026 Term

## Problem

U.S. manufacturing facilities report many pollution-prevention actions to the EPA each year, but plant managers and environmental health and safety (EHS) leaders lack a simple, recent-data way to judge whether records with those actions are more likely to see a meaningful reduction in the same chemical's on-site release the following year. This project builds an interpretable screening approach — not a causal claim — using EPA Toxics Release Inventory (TRI) Basic Plus data from 2020–2024.

The primary outcome, `REDUCTION_10`, equals 1 when a facility-chemical's next-year on-site release is no more than 90% of the current-year release. Four linked research questions examine (1) whether reduction rates differ by year/subsector, (2) whether reporting any pollution-prevention action is associated with achieving `REDUCTION_10` after controls, (3) which action types matter most, and (4) whether an interpretable model can predict non-reduction on a held-out future year (2023→2024).

Full problem statement, hypotheses, sample-size planning, and analysis plan (including Appendix D: GitHub repository link and folder structure) are in [`reports/QM640_Synopsis_TRI_2020_2024.docx`](reports/QM640_Synopsis_TRI_2020_2024.docx).

## Dataset source

- **Source:** U.S. EPA Toxics Release Inventory (TRI) Basic Plus Data Files, reporting years 2020–2024.
- **Official pages:** [TRI Basic Plus Data Files (1987–present)](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present) · [TRI Basic Plus Data Files Guides](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides)
- **Files used:** File 1A (facility, chemical, and release fields) and File 2A (production/activity ratio and up to four Source Reduction Activity Codes) for each year, joined within year on `DOCUMENT CONTROL NUMBER`.
- **Scope:** U.S. manufacturing facilities (primary NAICS beginning with 31, 32, or 33), Form R records only.
- **Size:** ~78,000 rows × 185–282 columns per file per year (~630 MB across all 10 raw files) — too large for this repository. See [`data/README.md`](data/README.md) for download instructions and a 200-row sample per year.

This is public-domain U.S. government data; no license restrictions apply to reuse.

**Note:** reporting year 2024 is the held-out test set (the 2023→2024 transition). It is used only for the final RQ4 holdout evaluation and is never touched during model development on 2020-2023.

## Repository structure

```
qm640-tri-pollution-prevention-capstone/
├── README.md                  # this file
├── requirements.txt           # Python dependencies
├── data/
│   ├── README.md              # EPA download links + instructions to reproduce data/raw/
│   └── sample/                # 200-row sample of File 1A and 2A for each year, 2020-2024
├── notebooks/
│   └── 01_data_exploration.ipynb   # EDA + Table 3 reconciliation for all years 2020-2024
├── src/
│   └── data_prep.py           # loads raw TRI files, applies Form R / manufacturing NAICS filters + consolidation, joins 1A+2A
└── reports/
    └── QM640_Synopsis_TRI_2020_2024.docx   # full synopsis: background, RQs, hypotheses, sample size, analysis plan, references
```

## Reproducing this work

1. Download the raw TRI Basic Plus files per [`data/README.md`](data/README.md) into `data/raw/<year>/`.
2. `pip install -r requirements.txt`
3. Run `src/data_prep.py` to filter to Form R / manufacturing records and join File 1A + 2A within each year.
4. Open `notebooks/01_data_exploration.ipynb` for the exploratory data analysis and the raw-to-consolidated reconciliation.

## Data validation

`src/data_prep.py --reconcile` and `notebooks/01_data_exploration.ipynb` walk each reporting year from raw rows through the Form R filter, the manufacturing-NAICS filter, and duplicate consolidation, and confirm an exact match with Table 3 of the synopsis for every year, 2020–2024. See [`VALIDATION_CHECKLIST.md`](VALIDATION_CHECKLIST.md) for the full data and APA/template validation process, which is re-run for every new synopsis version.

## Status

This repository reflects the **synopsis stage** — problem framing, data pipeline scaffolding, and exploratory analysis. Full modeling (RQ2–RQ4: logistic regression, action-type comparison, penalized prediction model on the 2023→2024 holdout) will follow in later project phases.

## References

See the synopsis document for the full reference list (12 sources: peer-reviewed papers on TRI disclosure and pollution prevention, methodology papers on sample size and prediction-model evaluation, and EPA program documentation), formatted in APA 7.
