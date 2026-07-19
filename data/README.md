# Data

## Why the full data isn't in this repo

The raw TRI Basic Plus files for 2020–2024 total roughly **630 MB** across 10 files (File 1A ≈ 62–64 MB and File 2A ≈ 44–46 MB per year), which is too large to store in a Git repository. Instead, this folder contains a small, fully reproducible sample plus exact download instructions.

## How to get the full data

1. Go to the EPA TRI Basic Plus Data Files page:
   https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-calendar-years-1987-present
2. Download **File 1A** and **File 2A** for reporting years **2020, 2021, 2022, 2023, and 2024** (U.S. national files).
3. Field definitions and code lists are in the TRI Basic Plus Data Files Guides:
   https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-plus-data-files-guides
4. Place the files in this structure so `src/data_prep.py` finds them:

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

Full field-level definitions, transformation rules, and the derivation of `REDUCTION_10` are documented in Appendix A of `reports/QM640_Synopsis_TRI_2020_2024.docx`.

**Note:** reporting year 2024 is the held-out test set (2023→2024 transition) — used only for the final RQ4 holdout evaluation, never for model development.

**Note on record counts:** the raw files above contain every TRI Basic Plus record (all industries). The synopsis's Table 3/Table 4 counts are smaller because they apply the Form R filter, the manufacturing NAICS (31/32/33) filter, and duplicate consolidation — see `src/data_prep.py`, `notebooks/01_data_exploration.ipynb`, Table D1 in Appendix D of the synopsis, and `VALIDATION_CHECKLIST.md` in the repo root for the reconciliation.
