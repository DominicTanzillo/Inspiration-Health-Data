import numpy as np
import pandas as pd

def parse_timepoint(timepoint: str) -> int:
    """
    Convert timepoint strings like 'L-3', 'L0', 'R+0', 'R+1' into numeric flight days
    on a stretched scale.
    In particular, we are converting the 3 dats of flight into 30 days so there is a
    difference, the final chart will have fake data in it.
    Convention:
        L-0 ->   0   (launch day = Flight Day 0)
        L-3 ->  -3   (3 days before launch)
        R+0 ->  30   (last day in space, stretched to day 30)
        R+1 ->  31   (first recovery day)
        R+N ->  N+30 (general rule for post-launch days)
    """
    label = str(timepoint).strip().upper()

    if label.startswith("L"):  # Pre-launch
        number = int(label.replace("L", "").replace("+", "").replace("-", "") or "0")
        return -number
    elif label.startswith("R"):  # Return / post-flight
        number = int(label.replace("R", "").replace("+", "").replace("-", "") or "0")
        return number + 30

    return np.nan


def add_flight_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'flight_day' column to a dataframe that already has 'timepoint' and 'astronautID'.
    Drops 'Sample Name' if present, since it's redundant.
    """
    df = df.copy()
    if "timepoint" not in df.columns:
        raise ValueError("DataFrame must contain a 'timepoint' column")

    # create numeric scale
    df["flight_day"] = df["timepoint"].apply(parse_timepoint)

    # drop redundant 'Sample Name' if it exists
    if "Sample Name" in df.columns:
        df = df.drop(columns=["Sample Name"])

    return df

def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived feature: Anion Gap.
    Anion Gap = Sodium − Chloride − Carbon Dioxide
    """
    df = df.copy()

    if all(c in df.columns for c in ["sodium_value", "chloride_value", "carbon_dioxide_value"]):
        df["anion_gap_value"] = (
            df["sodium_value"].astype(float)
            - df["chloride_value"].astype(float)
            - df["carbon_dioxide_value"].astype(float)
        )
        # Placeholders; min/max defined manually in stats.ANALYTE_INFO
        df["anion_gap_range_min"] = np.nan
        df["anion_gap_range_max"] = np.nan
    return df