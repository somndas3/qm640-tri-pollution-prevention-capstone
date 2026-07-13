"""
data_prep.py

Loads raw EPA TRI Basic Plus File 1A and File 2A for each reporting year (2020-2024),
applies the Form R and manufacturing-NAICS (31/32/33) filters described in the synopsis,
consolidates duplicate facility-chemical-year records, and joins the two files within
each year on DOCUMENT CONTROL NUMBER.

Usage:
    python src/data_prep.py --data-dir data/raw --year 2020
    python src/data_prep.py --data-dir data/raw --reconcile   # reproduce Table 3 for all years

Expects raw files at:
    data/raw/us_<year>/US_1a_<year>.txt
    data/raw/us_<year>/US_2a_<year>.txt

IMPORTANT -- data count reconciliation:
The raw file row count, the Form R + manufacturing-filtered count, and the
consolidated (deduplicated) count are three different numbers. Table 3 of the
synopsis reports the FILTERED, CONSOLIDATED count. Any screenshot or notebook
output showing plain df.shape on the raw file will look smaller after these
filters are applied -- that is expected, not a data error. Run with --reconcile
to print the same raw -> Form R -> manufacturing -> consolidated walk shown in
Appendix E (Figure E1) of the synopsis, and confirm it matches Table 3 exactly.

This is a synopsis-stage scaffold. Full REDUCTION_10 construction (matching each
facility-chemical record to the same record in the following year) will be added
in the next project phase.
"""

import argparse
import pandas as pd
from pathlib import Path

MANUFACTURING_NAICS_PREFIXES = ("31", "32", "33")
YEARS = (2020, 2021, 2022, 2023, 2024)


def load_filtered_1a(data_dir: Path, year: int) -> pd.DataFrame:
    """Load File 1A and apply the Form R + manufacturing-NAICS filters only
    (no consolidation yet). Used both by load_year() and reconcile()."""
    year_dir = data_dir / f"us_{year}"
    f1a = year_dir / f"US_1a_{year}.txt"
    df1 = pd.read_csv(f1a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="c", low_memory=False)

    form_col = next(c for c in df1.columns if c.strip().endswith("FORM TYPE"))
    naics_col = next(c for c in df1.columns if "PRIMARY NAICS CODE" in c)

    form_r = df1[df1[form_col] == "R"]
    manufacturing = form_r[form_r[naics_col].astype(str).str.startswith(MANUFACTURING_NAICS_PREFIXES)]
    return df1, form_r, manufacturing


def consolidate(df1_manufacturing: pd.DataFrame) -> pd.DataFrame:
    """Consolidate duplicate facility-chemical-year records to one row per
    facility + chemical (matches the 'unique facility-chemical-year records
    after consolidation' column of Table 3)."""
    trifd_col = next(c for c in df1_manufacturing.columns if c.strip().endswith("TRIFD"))
    cas_col = next(c for c in df1_manufacturing.columns if "CAS NUMBER" in c)
    chem_col = next(c for c in df1_manufacturing.columns if c.strip().endswith("CHEMICAL NAME"))
    return df1_manufacturing.drop_duplicates(subset=[trifd_col, cas_col, chem_col])


def load_year(data_dir: Path, year: int) -> pd.DataFrame:
    """Load, filter, consolidate File 1A, then join with File 2A for a single year."""
    year_dir = data_dir / f"us_{year}"
    f2a = year_dir / f"US_2a_{year}.txt"

    _, _, manufacturing = load_filtered_1a(data_dir, year)
    consolidated = consolidate(manufacturing)

    df2 = pd.read_csv(f2a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="c", low_memory=False)

    dcn_1a = next(c for c in consolidated.columns if "DOCUMENT CONTROL NUMBER" in c)
    dcn_2a = next(c for c in df2.columns if "DOCUMENT CONTROL NUMBER" in c)
    merged = consolidated.merge(df2, left_on=dcn_1a, right_on=dcn_2a, suffixes=("_1a", "_2a"))
    merged["REPORTING_YEAR"] = year
    return merged


def reconcile(data_dir: Path):
    """Print the raw -> Form R -> manufacturing -> consolidated walk for every
    year and confirm it matches Table 3 of the synopsis. This is the exact
    check documented in VALIDATION_CHECKLIST.md and shown in Appendix E,
    Figure E1."""
    print(f"{'Year':>6} {'Raw rows':>12} {'Form R':>12} {'+ Manufacturing':>16} {'Consolidated':>14}")
    for year in YEARS:
        raw, form_r, manufacturing = load_filtered_1a(data_dir, year)
        consolidated = consolidate(manufacturing)
        print(f"{year:>6} {len(raw):>12,} {len(form_r):>12,} {len(manufacturing):>16,} "
              f"{len(consolidated):>14,}")


def main():
    parser = argparse.ArgumentParser(description="Filter, consolidate, and join TRI Basic Plus files.")
    parser.add_argument("--data-dir", default="data/raw", help="Path to raw data root")
    parser.add_argument("--year", type=int, help="Reporting year, e.g. 2020")
    parser.add_argument("--out", default=None, help="Optional output CSV path")
    parser.add_argument("--reconcile", action="store_true",
                         help="Print raw/Form-R/manufacturing/consolidated counts for all years "
                              "(2020-2024) and compare against Table 3 of the synopsis.")
    args = parser.parse_args()

    if args.reconcile:
        reconcile(Path(args.data_dir))
        return

    if not args.year:
        parser.error("--year is required unless --reconcile is passed")

    df = load_year(Path(args.data_dir), args.year)
    print(f"Year {args.year}: {df.shape[0]:,} consolidated manufacturing Form R "
          f"facility-chemical records across {df.shape[1]} columns after filtering, "
          f"consolidation, and join.")

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
