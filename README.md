# Pollution-Prevention Actions and Next-Year Toxic Release Reduction in U.S. Manufacturing

**QM640 Data Analytics Capstone — Walsh College**
Author: Somnath Das · Advisor: Rishab Pandey · Summer 2026 Term

## Problem

U.S. manufacturing facilities report many pollution-prevention actions to the EPA each year, but plant managers and environmental health and safety (EHS) leaders lack a simple, recent-data way to judge whether records with those actions are more likely to see a meaningful reduction in the same chemical's on-site release the following year. This project builds an interpretable screening approach — not a causal claim — using EPA Toxics Release Inventory (TRI) Basic Plus data from 2020–2024.

The primary outcome, `REDUCTION_10`, equals 1 when a facility-chemical's next-year on-site release is no more than 90% of the current-year release. Four linked research questions examine (1) whether reduction rates differ by year/subsector, (2) whether reporting any pollution-prevention action is associated with achieving `REDUCTION_10` after controls, (3) which action types matter most, and (4) whether an interpretable model can predict non-reduction on a held-out future year (2023→2024).

## Data availability

All raw and processed data are shared **view-only** on Google Drive (anyone with the link can view):

**https://drive.google.com/drive/folders/1oPNHYCAvGwc7uQ1iIP2a_VlZdLnFJuid?usp=sharing**

| Location | Contents |
|---|---|
| `us_2020/` … `us_2024/` | Raw EPA TRI Basic Plus File 1A and File 2A, one folder per reporting year |
| `processed/` | Cleaned analysis datasets and audit tables produced by the EDA notebook |

The ten raw files total **535.6 MB**, which exceeds practical repository limits, so they are distributed through Drive rather than committed here. The interim report lists the size and SHA-256 checksum of every file so that any reader can confirm byte-identical source data.

### Processed files

| File | Description |
|---|---|
| `development.csv` | 123,535 records, action years 2020–2022, features **and** outcome |
| `reserved_2023_2024_features_only.csv` | 39,966 records, 2023→2024 holdout, **features only, no outcome** |
| `data_dictionary.csv` | Definition of every analysis column |
| `preprocessing_parameters.json` | Every preprocessing choice, column roles, and dataset hashes |
| `activity_code_crosswalk.csv` | Legacy W-code to S-code mapping with EPA descriptions |
| `audit_*.csv`, `quality_scorecard.csv` | Field widths, malformed rows, join, consolidation, attrition, quality checks |

## Dataset source

- **Source:** U.S. EPA Toxics Release Inventory (TRI) Basic Plus Data Files, reporting years 2020–2024.
- **Official pages:** [TRI Basic Plus Data Files (1987–present)](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present) · [TRI Basic Plus Data Files Guides](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides)
- **Files used:** File 1A (facility, chemical, and release fields) and File 2A (production/activity ratio and up to four Source Reduction Activity Codes) for each year, joined within year on `DOCUMENT CONTROL NUMBER`.
- **Scope:** U.S. manufacturing facilities (primary NAICS beginning with 31, 32, or 33), Form R records only.
- **Parsing note:** File 1A data lines carry 283 fields against a 282-field header because each data line ends with a trailing delimiter. Fields are read by position against the EPA guide with that offset applied.

This is public-domain U.S. government data; no license restrictions apply to reuse.

**Holdout discipline:** reporting year 2024 supplies outcomes only for the 2023→2024 transition, which is reserved for the final RQ4 evaluation. The reserved export is written under a features-only schema and asserted to contain zero outcome-bearing columns.

## Record counts after cleaning

| Stage | Records | Removed |
|---|---|---|
| Raw File 1A rows, action years 2020–2023 | 315,581 | — |
| Form R only | 280,426 | 35,155 |
| Manufacturing only (NAICS 31–33) | 226,361 | 54,065 |
| After duplicate consolidation | 224,185 | 2,176 |
| Matched to the following year | 205,447 | 18,738 |
| Eligible (positive base release, units agree) | 163,501 | 41,946 |
| → Development (2020-21, 2021-22, 2022-23) | 123,535 | — |
| → Reserved (2023-24) | 39,966 | — |

All synopsis sample-size minimums are met: RQ1 needs 1,068 (116× margin), RQ2 needs 10,756 (11.3×), RQ4 needs 1,269 (97×), and every RQ3 action type exceeds the ~290 required, the smallest being 361.

## Repository structure

```
qm640-tri-pollution-prevention-capstone/
├── README.md
├── requirements.txt
├── data/
│   ├── README.md              # EPA download links; raw data also on Drive (see above)
│   └── sample/                # 200-row sample of File 1A and 2A for each year
├── notebooks/
│   ├── 01_data_exploration.ipynb                    # earlier synopsis-stage EDA
│   └── 02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb    # FINAL EDA: full pipeline, 19 figures
├── src/
│   └── data_prep.py
└── reports/
    ├── QM640_Synopsis_TRI_2020_2024.docx
    └── QM640_Interim_Report_Das.docx                # Week 4 interim report
```

## Reproducing this work

1. Download the raw TRI files from the Drive link above (or from the EPA pages) into `data/raw/<year>/`.
2. `pip install -r requirements.txt`
3. Open `notebooks/02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb` and run all cells top to bottom. It performs parsing, filtering, consolidation, cross-year matching, the full EDA, and the controlled export of both analysis datasets.

## Status

**Week 4 — research design and exploratory data analysis complete.** The data pipeline, cleaning audit, EDA (19 figures), research design, and evaluation metrics are finished and documented in `reports/QM640_Interim_Report_Das.docx`. Model fitting (RQ2 adjusted logistic regression, RQ3 confirmatory comparisons, RQ4 penalised prediction on the reserved holdout) follows in Weeks 5–6.

## References

The interim report contains the full APA 7 reference list (21 sources: peer-reviewed work on TRI disclosure and pollution prevention, methodology papers on sample size, clustered inference, multiple comparisons and prediction-model evaluation, and EPA program documentation).
