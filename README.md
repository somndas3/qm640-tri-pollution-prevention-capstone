# Pollution-Prevention Actions and Next-Year Toxic Release Reduction in U.S. Manufacturing

**QM640 Data Analytics Capstone, Walsh College**
Author: Somnath Das · Mentor: Professor Rishab Pandey · Summer 2026 Term · Final report submitted September 15, 2026

## Project deliverables

| Deliverable | File |
|---|---|
| **Final report** (APA 7, submission version) | [`reports/QM640_Final_Report_Somnath_Das.docx`](reports/QM640_Final_Report_Somnath_Das.docx) |
| Final report, PDF for reading in the browser | [`reports/QM640_Final_Report_Somnath_Das.pdf`](reports/QM640_Final_Report_Somnath_Das.pdf) |
| **Final presentation** | [`presentation/QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pptx`](presentation/QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pptx) |
| Final presentation, PDF for reading in the browser | [`presentation/QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pdf`](presentation/QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pdf) |
| **Final analysis notebook** (RQ1 to RQ4 results) | [`notebooks/02_QM640_TRI_2020_2024_final.ipynb`](notebooks/02_QM640_TRI_2020_2024_final.ipynb) |
| Exploratory data analysis and data preparation notebook | [`notebooks/02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb`](notebooks/02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb) |
| Synopsis | [`reports/QM640_Synopsis_TRI_2020_2024.docx`](reports/QM640_Synopsis_TRI_2020_2024.docx) |

The final report is the authoritative record of methods and results. Every number in it was checked against the executed final notebook.

## Problem

U.S. manufacturing facilities report pollution-prevention actions to the EPA each year, but plant managers and environmental health and safety (EHS) leaders lack a simple, recent-data way to judge whether records with those actions are more likely to see a meaningful reduction in the same chemical's on-site release the following year, or which records deserve review first. This project builds an interpretable screening approach, not a causal claim, using EPA Toxics Release Inventory (TRI) Basic Plus data from 2020 to 2024.

The primary outcome, `REDUCTION_10`, equals 1 when a facility-chemical's next-year on-site release is no more than 90% of the current-year release. Four linked research questions examine (1) whether reduction rates differ by year and subsector, (2) whether reporting any pollution-prevention action is associated with achieving `REDUCTION_10` after controls, (3) which action types show the clearest differences, and (4) whether an interpretable model can predict non-reduction on a sealed future year (2023 to 2024).

## Key results

| Research question | Method | Result |
|---|---|---|
| RQ1: Do reduction rates differ by year and subsector? | Chi-square tests, Cramér's V | Yes, but small effects. Rates rose from 27.54% to 35.86% across transitions (V = .073) and ranged from 25.89% to 41.26% across subsectors (V = .048). |
| RQ2: Is reporting any action associated with reduction after adjustment? | Facility-clustered logistic regression | Adjusted odds ratio = 1.14, 95% CI [1.06, 1.23], p < .001. About 14% higher **odds** (not probability). An association, not proof of cause. |
| RQ3: Which action types differ from no action? | Five comparisons with Holm correction | Material modification (38.95%, +7.64 points) and operating practice or training (35.53%, +4.23 points). The other three types were not statistically demonstrated, which does not mean they are ineffective. |
| RQ4: Can a model predict non-reduction on the sealed 2023 to 2024 holdout? | Elastic-net logistic regression, 13 predictors, leave-one-transition-out cross-validation | Holdout AUC = .523, 95% CI [.515, .532], versus .502 for the baseline. A reliable but modest gain, suitable for triage, not automation. |

**Screening lift.** Among the top 5% of 39,500 ranked holdout records (1,975 records), 73.87% did not reduce, against a base rate of 67.95%. That is about 117 more non-reducers than an unranked review of the same size.

**Four user benefits** (final report, Implementation and User Benefit):

1. **Triage with the model:** work a fixed review capacity from the top of the ranked list.
2. **Prioritize further evaluation of the strongest action types:** material modification and operating practice or training.
3. **Weight by pounds at risk:** order reviews by predicted risk multiplied by release volume.
4. **Benchmark against peers and trend:** compare each facility with its subsector and recent trend.

Human experts stay in control. The model tells a team where to look first, not what to conclude.

### Differences between the slides and the final report

The presentation is kept exactly as delivered. Where it differs from the final report, the report is correct:

- Slides 5, 8, and 9 describe the RQ4 elastic net as using 15 subsector predictors. The locked model used **13 predictors** (release, production, action, and chemical hazard features) and **no subsector indicators**.
- Slide 9 says diagnostics "confirm the model is sound," and slide 10 describes the Brier score (0.218) as "reasonably well-calibrated." The report states that diagnostics did not indicate serious multicollinearity, and that the calibration plot showed no large departures within a narrow range of predicted probabilities, without a formal calibration slope.
- Slides 2 and 12 use causal-sounding wording ("actually lead to," "Focus Prevention Where It Works"). The report treats all results as associations and frames benefit 2 as prioritizing further evaluation.
- Slide 14 cites a different Gamper-Rabindran (2006) article. The correct source is: Gamper-Rabindran, S. (2006). Did the EPA's voluntary industrial toxics program reduce emissions? A GIS analysis of distributional impacts and by-media analysis of substitution. *Journal of Environmental Economics and Management, 52*(1), 391–410.

## Data availability

All raw and processed data are shared **view-only** on Google Drive (anyone with the link can view):

**https://drive.google.com/drive/folders/1oPNHYCAvGwc7uQ1iIP2a_VlZdLnFJuid?usp=sharing**

| Location | Contents |
|---|---|
| `us_2020/` … `us_2024/` | Raw EPA TRI Basic Plus File 1A and File 2A, one folder per reporting year |
| `processed/` | Cleaned analysis datasets and audit tables produced by the EDA notebook |

The ten raw files total **535.6 MB**, which exceeds practical repository limits, so they are distributed through Drive rather than committed here. The final report (Appendix B, Table B1) lists the size and SHA-256 checksum of every file so that any reader can confirm byte-identical source data.

### Processed files

| File | Description |
|---|---|
| `development.csv` | 123,535 records, action years 2020 to 2022, features **and** outcome |
| `reserved_2023_2024_features_only.csv` | 39,966 records, 2023 to 2024 holdout, **features only, no outcome** |
| `data_dictionary.csv` | Definition of every analysis column |
| `preprocessing_parameters.json` | Every preprocessing choice, column roles, and dataset hashes |
| `activity_code_crosswalk.csv` | Legacy W-code to S-code mapping with EPA descriptions |
| `audit_*.csv`, `quality_scorecard.csv` | Field widths, malformed rows, join, consolidation, attrition, quality checks |

## Dataset source

- **Source:** U.S. EPA Toxics Release Inventory (TRI) Basic Plus Data Files, reporting years 2020 to 2024.
- **Official pages:** [TRI Basic Plus Data Files (1987 to present)](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present) · [TRI Basic Plus Data Files Guides](https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides)
- **Files used:** File 1A (facility, chemical, and release fields) and File 2A (production or activity ratio and up to four Source Reduction Activity Codes) for each year, joined within year on `DOCUMENT CONTROL NUMBER`.
- **Scope:** U.S. manufacturing facilities (primary NAICS beginning with 31, 32, or 33), Form R records only.
- **Parsing note:** File 1A data lines carry 283 fields against a 282-field header because each data line ends with a trailing delimiter. Fields are read by position against the EPA guide with that offset applied.
- **Duplicate filings:** consolidated with the conditional rule in the final report, Appendix C. When a revision-coded filing exists, the revision with the highest document control number supplies the release; otherwise the release quantities of the original filings are summed.

This is public-domain U.S. government data; no license restrictions apply to reuse.

**Holdout discipline:** reporting year 2024 supplies outcomes only for the 2023 to 2024 transition, which was reserved for the final RQ4 evaluation and scored once after the model was locked. The reserved export is written under a features-only schema and asserted to contain zero outcome-bearing columns.

## Record counts after cleaning

| Stage | Records | Removed |
|---|---|---|
| Raw File 1A rows, action years 2020 to 2023 | 315,581 | |
| Form R only | 280,426 | 35,155 |
| Manufacturing only (NAICS 31 to 33) | 226,361 | 54,065 |
| After duplicate consolidation | 224,185 | 2,176 |
| Matched to the following year | 205,447 | 18,738 |
| Eligible (positive base release, units agree) | 163,501 | 41,946 |
| Development (2020-21, 2021-22, 2022-23) | 123,535 | |
| Reserved holdout (2023-24) | 39,966 | |

The development set includes 122,017 pound-reported records (used for RQ2 and RQ4) and 1,518 gram-reported dioxin records analyzed separately. Of the 39,966 holdout records, 39,500 pound-reported records formed the RQ4 modeling holdout.

All sample-size minimums are met: RQ1 needs 1,068 records, RQ2 needs 10,756, RQ4 needs 1,269, and every RQ3 action type exceeds the roughly 290 required, the smallest being 361 (final report, Appendix E, Table E4).

## Repository structure

```
qm640-tri-pollution-prevention-capstone/
├── README.md
├── requirements.txt
├── VALIDATION_CHECKLIST.md
├── data/
│   ├── README.md              # EPA download links; raw data also on Drive (see above)
│   └── sample/                # header plus 200 rows of File 1A and 2A for each year
├── notebooks/
│   ├── 01_data_exploration.ipynb                    # early synopsis-stage exploration
│   ├── 02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb    # EDA and data preparation: parsing, consolidation, matching, export, 19 figures
│   └── 02_QM640_TRI_2020_2024_final.ipynb           # FINAL analysis: RQ1 to RQ4, holdout evaluation, screening lift
├── src/
│   └── data_prep.py           # synopsis-stage preparation script (superseded by the EDA notebook)
├── reports/
│   ├── QM640_Synopsis_TRI_2020_2024.docx
│   ├── QM640_Final_Report_Somnath_Das.docx          # FINAL report
│   └── QM640_Final_Report_Somnath_Das.pdf
└── presentation/
    ├── QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pptx
    └── QM640_Walsh_Capstone_Final_Presentation_Somnath_Das.pdf
```

## Reproducing this work

Both notebooks were run top to bottom in Google Colab with the data on Google Drive. The final notebook fixes random elements with seed 42.

1. Copy the Drive folder above into your own Google Drive, or download the raw files from the EPA pages.
2. Update the data path near the top of each notebook (the notebooks use `/content/drive/MyDrive/Walsh_DBA/Year2/Projects/Capstone_QM640_TRI_2020_2024/Data`).
3. Run `notebooks/02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb` from top to bottom. It performs parsing, filtering, consolidation, cross-year matching, the full EDA, and the controlled export of both analysis datasets to `processed/`.
4. Run `notebooks/02_QM640_TRI_2020_2024_final.ipynb` from top to bottom. It fits the RQ1 to RQ3 models, tunes and locks the RQ4 elastic net, and scores the sealed holdout once.
5. To run outside Colab, `pip install -r requirements.txt` and replace the Google Drive mount cell with a local path.

`src/data_prep.py` is kept for transparency. It reproduces the synopsis-stage record walk but uses the earlier "highest document control number" duplicate rule, which the final pipeline replaced (final report, Appendix C). Use the EDA notebook to reproduce final results.

## Status

**Complete.** The data pipeline, EDA, statistical tests (RQ1 to RQ3), predictive model and sealed holdout evaluation (RQ4), final report, and final presentation are finished.

## References

The final report contains the full APA 7 reference list (24 sources: peer-reviewed work on TRI disclosure and pollution prevention, methodology papers on interval estimation, clustered inference, multiple comparisons, sample size, regularization, and prediction-model evaluation, and EPA program documentation).
