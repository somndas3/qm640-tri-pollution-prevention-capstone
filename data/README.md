# Data

## Why the full data isn't in this repo

The raw TRI Basic Plus files for 2020–2024 total **535.6 MB** across 10 files (File 1A 61.6–63.6 MB and File 2A 44.0–45.4 MB per year), which is too large to store in a Git repository. Instead, this folder contains a small sample plus exact download instructions. The full raw and processed files are also shared view-only on Google Drive (see the root `README.md`), and the final report (Appendix B, Table B1) lists the size and SHA-256 checksum of every file.

## How to get the full data

1. Go to the EPA TRI Basic Plus Data Files page:
   https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present
2. Download **File 1A** and **File 2A** for reporting years **2020, 2021, 2022, 2023, and 2024** (U.S. national files).
3. Field definitions and code lists are in the TRI Basic Plus Data Files Guides:
   https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides
4. For the final pipeline, point the data path in `notebooks/02_EDA_QM640_Synopsis_TRI_2020_2024.ipynb` at the folder holding the files. The earlier synopsis-stage script `src/data_prep.py` expects this structure:

```
data/raw/
├── us_2020/US_1a_2020.txt, US_2a_2020.txt
├── us_2021/US_1a_2021.txt, US_2a_2021.txt
├── us_2022/US_1a_2022.txt, US_2a_2022.txt
├── us_2023/US_1a_2023.txt, US_2a_2023.txt
└── us_2024/US_1a_2024.txt, US_2a_2024.txt
```

Files are tab-delimited text, encoded as `latin-1`. Each row is one facility-chemical (Form R and Form A) record for that reporting year.

## Sample data (`data/sample/`)

Each file below is the **header row plus the first 200 data rows** of the corresponding raw file, included directly in this repo so reviewers can inspect the real structure without downloading anything:

| File | Rows (incl. header) | Source |
|---|---|---|
| `US_1a_<year>_sample.txt` | 201 | File 1A, reporting year `<year>` (2020–2024) |
| `US_2a_<year>_sample.txt` | 201 | File 2A, reporting year `<year>` (2020–2024) |

## Key fields used in this study

- **File 1A:** `TRIFD` (facility ID), `FACILITY NAME`, `FACILITY STATE`, `PRIMARY NAICS CODE`, `DOCUMENT CONTROL NUMBER`, `CAS NUMBER`, `CHEMICAL NAME`, `UNIT OF MEASURE`, and total on-site release fields.
- **File 2A:** `DOCUMENT CONTROL NUMBER` (join key with File 1A), production/activity ratio, and up to four `SOURCE REDUCTION ACTIVITY CODE` fields (used to derive `REPORTED_ANY_SOURCE_REDUCTION_ACTION`).

Full definitions of the analysis variables, the cleaning log, and the record flow are documented in the final report, `reports/QM640_Final_Report_Somnath_Das.docx` (Appendix E, Tables E1 to E3). The duplicate-filing consolidation rule is in Appendix C, and `data_dictionary.csv` in the Drive `processed/` folder defines every exported column.

**Note:** reporting year 2024 is the held-out test set (2023→2024 transition), used only once for the final RQ4 holdout evaluation and never for model development.

**Note on record counts:** the raw files above contain every TRI Basic Plus record (all industries). The analysis counts are smaller because they apply the Form R filter, the manufacturing NAICS (31/32/33) filter, duplicate consolidation, cross-year matching, and eligibility rules. The final record flow is in the root `README.md` and the final report (Appendix E, Table E3), and it is produced by the EDA notebook. `src/data_prep.py` (`--reconcile` / `--reduction10`) and `notebooks/01_data_exploration.ipynb` reproduce the earlier synopsis-stage walk.
