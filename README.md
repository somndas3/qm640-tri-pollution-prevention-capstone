# Pollution-Prevention Actions and Next-Year Toxic Release Reduction in U.S. Manufacturing

**QM640 Data Analytics Capstone — Walsh College**
Author: Somnath Das · Advisor: Rishab Pandey · Summer 2026 Term

## Problem

U.S. manufacturing facilities report many pollution-prevention actions to the EPA each year, but plant managers and environmental health and safety (EHS) leaders lack a simple, recent-data way to judge whether records with those actions are more likely to see a meaningful reduction in the same chemical's on-site release the following year. This project builds an interpretable screening approach — not a causal claim — using EPA Toxics Release Inventory (TRI) Basic Plus data from 2020–2024.

The primary outcome, `REDUCTION_10`, equals 1 when a facility-chemical's next-year on-site release is no more than 90% of the current-year release. Four linked research questions examine (1) whether reduction rates differ by year/subsector, (2) whether reporting any pollution-prevention action is associated with achieving `REDUCTION_10` after controls, (3) which broad action categories matter most, and (4) whether an interpretable model can predict non-reduction on a held-out future year (2023→2024).

Full problem statement, hypotheses, sample-size planning, and analysis plan (including Appendix E: dataset screenshots and folder structure) are in [`reports/QM640_Synopsis_TRI_2020_2024_V5.docx`](reports/QM640_Synopsis_TRI_2020_2024_V5.docx).

## Dataset source

- **Source:** U.S. EPA Toxics Release Inventory (TRI) Basic Plus Data Files, reporting years 2020–2024.
- **Official pages:** [TRI Basic Plus Data Files (1987–present)](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present) · [TRI Basic Plus Data Files Guides](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides)
- **Files used:** File 1A (facility, chemical, and release fields) and File 2A (production/activity ratio and up to four Source Reduction Activity Codes) for each year, joined within year on `DOCUMENT CONTROL NUMBER`.
- **Scope:** U.S. manufacturing facilities (primary NAICS beginning with 31, 32, or 33), Form R records only.
- **Size:** ~78,000 rows × 185–282 columns per file per year (~630 MB across all 10 raw files) — too large for this repository. See [`data/README.md`](data/README.md) for download instructions and a 200-row sample per year.

This is public-domain U.S. government data; no license restrictions apply to reuse.

## Repository structure

```
qm640-tri-pollution-prevention-capstone/
├── README.md                  # this file
├── requirements.txt           # Python dependencies
├── data/
│   ├── README.md              # EPA download links + instructions to reproduce data/raw/
│   └── sample/                # 200-row sample of File 1A and 2A for each year, 2020-2024
├── notebooks/
│   └── 01_data_exploration.ipynb   # initial EDA: shape, head, dtypes, missing values, action-rate trend
├── src/
│   └── data_prep.py           # loads raw TRI files, applies Form R / manufacturing NAICS filters, joins 1A+2A
├── reports/
│   └── QM640_Synopsis_TRI_2020_2024_V5.docx   # full synopsis: background, RQs, hypotheses, sample size, analysis plan, references
└── images/
    └── 01-06_*.png            # dataset preview, shape, info, describe, missing values, action-rate distribution
```

## Reproducing this work

1. Download the raw TRI Basic Plus files per [`data/README.md`](data/README.md) into `data/raw/<year>/`.
2. `pip install -r requirements.txt`
3. Run `src/data_prep.py` to filter to Form R / manufacturing records and join File 1A + 2A within each year.
4. Open `notebooks/01_data_exploration.ipynb` for the exploratory data analysis shown in `images/`.

## Status

This repository reflects the **synopsis stage** — problem framing, data pipeline scaffolding, and exploratory analysis. Full modeling (RQ2–RQ4: logistic regression, action-category comparison, penalized prediction model on the 2023→2024 holdout) will follow in later phases per the six-week execution plan in Appendix D of the synopsis.

## References

See the synopsis document for the full reference list (12 sources: peer-reviewed papers on TRI disclosure and pollution prevention, methodology papers on sample size and prediction-model evaluation, and EPA program documentation), formatted in APA 7.
