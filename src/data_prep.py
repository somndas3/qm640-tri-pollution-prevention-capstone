"""
data_prep.py

Loads raw EPA TRI Basic Plus File 1A and File 2A for each reporting year (2020-2024),
applies the Form R and manufacturing-NAICS (31/32/33) filters described in the synopsis,
consolidates duplicate facility-chemical-year records using a deterministic tie-break
rule, joins the two files within each year on DOCUMENT CONTROL NUMBER, and matches
consolidated records across consecutive reporting years to construct REDUCTION_10.

Usage:
    python src/data_prep.py --data-dir data/raw --year 2020
    python src/data_prep.py --data-dir data/raw --reconcile      # reproduce Table 3 / Table D1 for all years
    python src/data_prep.py --data-dir data/raw --reduction10    # reproduce Table 4 for all consecutive-year transitions

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
Appendix D (Table D1) of the synopsis, and confirm it matches Table 3 exactly.

IMPORTANT -- duplicate consolidation tie-break rule:
A single facility-chemical-year is sometimes reported across more than one Form R
filing (e.g., amended or resubmitted forms). Consolidation groups by
TRIFD + CAS NUMBER + CHEMICAL NAME within a reporting year and resolves duplicates
deterministically:
  - REPORTED_ANY_SOURCE_REDUCTION_ACTION = 1 if ANY duplicate filing reports a valid
    Source Reduction Activity Code (logical OR across duplicates).
  - The authoritative TOTAL ON-SITE RELEASES and UNIT OF MEASURE are taken from the
    filing with the highest DOCUMENT CONTROL NUMBER among the duplicates (treated as
    the most recent / final filing).
This rule is documented in Appendix A, Table A1 of the synopsis and is the exact
rule used to produce Table 3, Table 4, and Table D1.
"""

import argparse
import pandas as pd
from pathlib import Path

MANUFACTURING_NAICS_PREFIXES = ("31", "32", "33")
YEARS = (2020, 2021, 2022, 2023, 2024)


def _find_col(columns, suffix):
    """Match a real EPA column header (which may carry a leading 'N. ' numeric
    prefix and/or a stray non-breaking space) by its normalized suffix."""
    def norm(s):
        return " ".join(str(s).replace("\xa0", " ").split())
    suffix_n = norm(suffix)
    for c in columns:
        if norm(c).endswith(suffix_n):
            return c
    raise KeyError(suffix)


def load_filtered_1a(data_dir: Path, year: int) -> pd.DataFrame:
    """Load File 1A and apply the Form R + manufacturing-NAICS filters only
    (no consolidation yet). Used both by load_year() and reconcile()."""
    year_dir = data_dir / f"us_{year}"
    f1a = year_dir / f"US_1a_{year}.txt"
    df1 = pd.read_csv(f1a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="c", low_memory=False)

    form_col = _find_col(df1.columns, "FORM TYPE")
    naics_col = _find_col(df1.columns, "PRIMARY NAICS CODE")

    form_r = df1[df1[form_col] == "R"]
    manufacturing = form_r[form_r[naics_col].astype(str).str.startswith(MANUFACTURING_NAICS_PREFIXES)].copy()
    return df1, form_r, manufacturing


def load_2a_action(data_dir: Path, year: int) -> pd.Series:
    """Load File 2A and reduce it to one boolean ANY_ACTION flag per
    DOCUMENT CONTROL NUMBER: True if any of the four Source Reduction Activity
    Code fields is populated for that filing."""
    year_dir = data_dir / f"us_{year}"
    f2a = year_dir / f"US_2a_{year}.txt"
    df2 = pd.read_csv(f2a, sep="\t", index_col=False, encoding="latin1",
                       on_bad_lines="skip", engine="c", low_memory=False)

    dcn_col = _find_col(df2.columns, "DOCUMENT CONTROL NUMBER")
    code_cols = [
        _find_col(df2.columns, "FIRST SOURCE REDUCTION ACTIVITY CODE"),
        _find_col(df2.columns, "SECOND SOURCE REDUCTION ACTIVITY CODE"),
        _find_col(df2.columns, "THIRD SOURCE REDUCTION ACTIVITY CODE"),
        _find_col(df2.columns, "FOURTH SOURCE REDUCTION ACTIVITY CODE"),
    ]
    for c in code_cols:
        df2[c] = df2[c].astype(str).str.strip().replace({"nan": ""})
    df2["ANY_ACTION"] = (df2[code_cols] != "").any(axis=1)
    return df2.groupby(dcn_col)["ANY_ACTION"].any()


def consolidate(df1_manufacturing: pd.DataFrame, action_by_dcn: pd.Series) -> pd.DataFrame:
    """Consolidate duplicate facility-chemical-year records to one row per
    TRIFD + CAS NUMBER + CHEMICAL NAME (matches the 'unique facility-chemical-year
    records after consolidation' column of Table 3), applying the deterministic
    tie-break rule documented in Appendix A, Table A1:
      - REPORTED_ANY_SOURCE_REDUCTION_ACTION = OR across all duplicate filings.
      - Authoritative release/unit = the filing with the highest
        DOCUMENT CONTROL NUMBER among the duplicates.
    """
    trifd_col = _find_col(df1_manufacturing.columns, "TRIFD")
    cas_col = _find_col(df1_manufacturing.columns, "CAS NUMBER")
    chem_col = _find_col(df1_manufacturing.columns, "CHEMICAL NAME")
    dcn_col = _find_col(df1_manufacturing.columns, "DOCUMENT CONTROL NUMBER")

    grp_key = [trifd_col, cas_col, chem_col]

    df = df1_manufacturing.copy()
    df["REPORTED_ANY_SOURCE_REDUCTION_ACTION"] = df[dcn_col].map(action_by_dcn).fillna(False)

    # OR across duplicates within each facility-chemical group
    action_any = df.groupby(grp_key)["REPORTED_ANY_SOURCE_REDUCTION_ACTION"].transform("any")
    df["REPORTED_ANY_SOURCE_REDUCTION_ACTION"] = action_any

    # authoritative row per group = highest DOCUMENT CONTROL NUMBER
    df_sorted = df.sort_values(dcn_col)
    consolidated = df_sorted.drop_duplicates(subset=grp_key, keep="last").copy()

    release_col = _find_col(consolidated.columns, "TOTAL ON-SITE RELEASES")
    consolidated[release_col] = pd.to_numeric(consolidated[release_col], errors="coerce")
    return consolidated


def load_year(data_dir: Path, year: int) -> pd.DataFrame:
    """Load, filter, and consolidate File 1A (with the deterministic tie-break
    rule applied against File 2A action data) for a single year."""
    _, _, manufacturing = load_filtered_1a(data_dir, year)
    action_by_dcn = load_2a_action(data_dir, year)
    consolidated = consolidate(manufacturing, action_by_dcn)
    consolidated["REPORTING_YEAR"] = year
    return consolidated


def reconcile(data_dir: Path):
    """Print the raw -> Form R -> manufacturing -> consolidated walk for every
    year and confirm it matches Table 3 of the synopsis. This is the exact
    check documented in VALIDATION_CHECKLIST.md and shown in Appendix D,
    Table D1."""
    print(f"{'Year':>6} {'Raw rows':>12} {'Form R':>12} {'+ Manufacturing':>16} "
          f"{'Consolidated':>14} {'Action %':>10}")
    for year in YEARS:
        raw, form_r, manufacturing = load_filtered_1a(data_dir, year)
        action_by_dcn = load_2a_action(data_dir, year)
        consolidated = consolidate(manufacturing, action_by_dcn)
        pct = consolidated["REPORTED_ANY_SOURCE_REDUCTION_ACTION"].mean() * 100
        print(f"{year:>6} {len(raw):>12,} {len(form_r):>12,} {len(manufacturing):>16,} "
              f"{len(consolidated):>14,} {pct:>9.2f}%")


def match_consecutive_years(consol_t: pd.DataFrame, consol_t1: pd.DataFrame) -> pd.DataFrame:
    """Match consolidated action-year records (consol_t) to the same TRIFD +
    TRI_CHEM_ID in the following year (consol_t1), and construct REDUCTION_10.
    REDUCTION_10 = 1 when next-year TOTAL ON-SITE RELEASES <= 0.90 x current-year
    release, provided current-year release > 0 (Appendix A, Table A4)."""
    trifd_col = _find_col(consol_t.columns, "TRIFD")
    chem_id_col = _find_col(consol_t.columns, "TRI_CHEM_ID")
    unit_col = _find_col(consol_t.columns, "UNIT OF MEASURE")
    release_col = _find_col(consol_t.columns, "TOTAL ON-SITE RELEASES")
    action_col = "REPORTED_ANY_SOURCE_REDUCTION_ACTION"

    a = consol_t[[trifd_col, chem_id_col, unit_col, release_col, action_col]].rename(
        columns={release_col: "REL_T", unit_col: "UNIT_T"})
    b = consol_t1[[trifd_col, chem_id_col, unit_col, release_col]].rename(
        columns={release_col: "REL_T1", unit_col: "UNIT_T1"})

    matched = a.merge(b, on=[trifd_col, chem_id_col], how="inner")
    zero_mask = matched["REL_T"] == 0
    eligible = matched[~zero_mask].copy()
    eligible["REDUCTION_10"] = eligible["REL_T1"] <= 0.90 * eligible["REL_T"]

    matched["ELIGIBLE"] = ~zero_mask
    matched["REDUCTION_10"] = eligible["REDUCTION_10"].reindex(matched.index, fill_value=False)
    return matched


def reduction10_table(data_dir: Path):
    """Print the consecutive-year matching walk (Table 4) for every transition
    2020-2021 through 2023-2024, using the same consolidated frames produced by
    load_year()."""
    consolidated_by_year = {year: load_year(data_dir, year) for year in YEARS}

    print(f"{'Transition':>14} {'Matched':>10} {'Zero-release':>13} {'Eligible':>10} {'Reduction %':>12}")
    for t in (2020, 2021, 2022, 2023):
        m = match_consecutive_years(consolidated_by_year[t], consolidated_by_year[t + 1])
        n_matched = len(m)
        n_zero = int((~m["ELIGIBLE"]).sum())
        eligible = m[m["ELIGIBLE"]]
        n_eligible = len(eligible)
        rate = eligible["REDUCTION_10"].mean() * 100
        print(f"{t}-{t+1:>9} {n_matched:>10,} {n_zero:>13,} {n_eligible:>10,} {rate:>11.2f}%")


def main():
    parser = argparse.ArgumentParser(description="Filter, consolidate, join, and match TRI Basic Plus files.")
    parser.add_argument("--data-dir", default="data/raw", help="Path to raw data root")
    parser.add_argument("--year", type=int, help="Reporting year, e.g. 2020")
    parser.add_argument("--out", default=None, help="Optional output CSV path")
    parser.add_argument("--reconcile", action="store_true",
                         help="Print raw/Form-R/manufacturing/consolidated counts for all years "
                              "(2020-2024) and compare against Table 3 of the synopsis.")
    parser.add_argument("--reduction10", action="store_true",
                         help="Print the consecutive-year matching walk (matched/zero/eligible/rate) "
                              "for every transition and compare against Table 4 of the synopsis.")
    args = parser.parse_args()

    if args.reconcile:
        reconcile(Path(args.data_dir))
        return

    if args.reduction10:
        reduction10_table(Path(args.data_dir))
        return

    if not args.year:
        parser.error("--year is required unless --reconcile or --reduction10 is passed")

    df = load_year(Path(args.data_dir), args.year)
    print(f"Year {args.year}: {df.shape[0]:,} consolidated manufacturing Form R "
          f"facility-chemical records across {df.shape[1]} columns after filtering, "
          f"consolidation (with tie-break), and File 2A action join.")

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
