"""
data_prep.py

Loads raw EPA TRI Basic Plus File 1A and File 2A for each reporting year (2020-2024),
applies the Form R and manufacturing-NAICS (31/32/33) filters described in the synopsis,
and joins the two files within each year on DOCUMENT CONTROL NUMBER.

Usage:
    python src/data_prep.py --data-dir data/raw --year 2020

Expects raw files at:
    data/raw/us_<year>/US_1a_<year>.txt
    data/raw/us_<year>/US_2a_<year>.txt

This is a synopsis-stage scaffold. Full REDUCTION_10 construction (matching each
facility-chemical record to the same record in the following year) will be added
in the next project phase.
"""

import argparse
import pandas as pd
from pathlib import Path

MANUFACTURING_NAICS_PREFIXES = ("31", "32", "33")


def load_year(data_dir: Path, year: int) -> pd.DataFrame:
    """Load and join File 1A + File 2A for a single reporting year."""
    year_dir = data_dir / f"us_{year}"
    f1a = year_dir / f"US_1a_{year}.txt"
    f2a = year_dir / f"US_2a_{year}.txt"

    df1 = pd.read_csv(f1a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="python")
    df2 = pd.read_csv(f2a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="python")

    # Keep Form R records only
    form_col = next(c for c in df1.columns if c.strip().endswith("FORM TYPE"))
    df1 = df1[df1[form_col] == "R"].copy()

    # Restrict to manufacturing NAICS (primary code begins with 31, 32, or 33)
    naics_col = next(c for c in df1.columns if "PRIMARY NAICS CODE" in c)
    df1 = df1[df1[naics_col].astype(str).str.startswith(MANUFACTURING_NAICS_PREFIXES)]

    # Join on DOCUMENT CONTROL NUMBER
    dcn_1a = next(c for c in df1.columns if "DOCUMENT CONTROL NUMBER" in c)
    dcn_2a = next(c for c in df2.columns if "DOCUMENT CONTROL NUMBER" in c)
    merged = df1.merge(df2, left_on=dcn_1a, right_on=dcn_2a, suffixes=("_1a", "_2a"))
    merged["REPORTING_YEAR"] = year
    return merged


def main():
    parser = argparse.ArgumentParser(description="Filter and join TRI Basic Plus files by year.")
    parser.add_argument("--data-dir", default="data/raw", help="Path to raw data root")
    parser.add_argument("--year", type=int, required=True, help="Reporting year, e.g. 2020")
    parser.add_argument("--out", default=None, help="Optional output CSV path")
    args = parser.parse_args()

    df = load_year(Path(args.data_dir), args.year)
    print(f"Year {args.year}: {df.shape[0]:,} manufacturing Form R facility-chemical records "
          f"across {df.shape[1]} columns after filtering and join.")

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
