import pandas as pd
import numpy as np
from scipy import stats
from .featureEngineering import parse_timepoint

# Map analyte base names to human labels + units + reference ranges
## To get sub and superscripts in Markdown I used ChatGPT: https://chatgpt.com/share/68d9c8f6-2674-8008-8ff7-0731bec9ad49
ANALYTE_INFO = {
    "albumin": {"label": "Albumin", "unit": "g/dL"},
    "alkaline_phosphatase": {"label": "Alkaline Phosphatase", "unit": "U/L"},
    "alt": {"label": "ALT", "unit": "U/L"},
    "ast": {"label": "AST", "unit": "U/L"},
    "total_bilirubin": {"label": "Bilirubin", "unit": "mg/dL"},
    "bun_to_creatinine_ratio": {"label": "BUN/Creatinine Ratio", "unit": ""},
    "calcium": {"label": "Ca²⁺", "unit": "mg/dL"},
    "carbon_dioxide": {"label": "CO₂", "unit": "mmol/L"},
    "chloride": {"label": "Cl⁻", "unit": "mmol/L"},
    "creatinine": {"label": "Creatinine", "unit": "mg/dL"},
    "egfr_african_american": {"label": "eGFR (AA)", "unit": "mL/min/1.73m²"},
    "egfr_non_african_american": {"label": "eGFR (non-AA)", "unit": "mL/min/1.73m²"},
    "globulin": {"label": "Globulin", "unit": "g/dL"},
    "glucose": {"label": "Glucose", "unit": "mg/dL"},
    "potassium": {"label": "K⁺", "unit": "mmol/L"},
    "total_protein": {"label": "Protein", "unit": "g/dL"},
    "sodium": {"label": "Na⁺", "unit": "mmol/L"},
    "urea_nitrogen_bun": {"label": "BUN", "unit": "mg/dL"},


    # Derived feature
    "anion_gap": {
        "label": "Anion Gap",
        "unit": "mmol/L",
        "min": 8,   # manual reference range
        "max": 24
    },
}

# Helpers to find columns by prefix (robust to unit suffixes)
def _first_col_startswith(df: pd.DataFrame, prefixes) -> str | None:
    """
    Return the first column whose lowercase name starts with any prefix in `prefixes`.
    """
    if isinstance(prefixes, str):
        prefixes = [prefixes]
    prefixes = [p.lower() for p in prefixes]
    for col in df.columns:
        cl = col.lower()
        for p in prefixes:
            if cl.startswith(p):
                return col
    return None


def _value_min_max_cols(df: pd.DataFrame, analyte: str):
    """
    For a given base analyte name, return (value_col, min_col, max_col) using flexible prefixes.
    Works with columns like:
      - "<analyte>_value_*"
      - "<analyte>_range_min_*" or "<analyte>_min_*"
      - "<analyte>_range_max_*" or "<analyte>_max_*"
    """
    v = _first_col_startswith(df, f"{analyte}_value")
    mn = _first_col_startswith(df, [f"{analyte}_range_min", f"{analyte}_min"])
    mx = _first_col_startswith(df, [f"{analyte}_range_max", f"{analyte}_max"])
    return v, mn, mx

# Tidy Transformation
def tidy_from_wide(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform astronaut CSV with value/min/max triplets into tidy format.
    Adds derived analytes (like Anion Gap) using flexible column matching.
    Returns: columns [astronautID, timepoint, flight_day, analyte, value, min, max, unit, label, sex]
    """
    tidy_records = []

    ## Standard analytes ##
    for analyte, meta in ANALYTE_INFO.items():
        if analyte == "anion_gap":
            # handled below in derived block
            continue

        value_col, min_col, max_col = _value_min_max_cols(df, analyte)
        if value_col is None:
            continue  # analyte not present in this dataset

        for _, row in df.iterrows():
            astronaut = row["astronautID"]
            rec = {
                "astronautID": astronaut,
                "timepoint": row["timepoint"],
                "flight_day": parse_timepoint(row["timepoint"]),
                "analyte": analyte,
                "value": row[value_col],
                "min": (row[min_col] if (min_col and pd.notna(row.get(min_col))) else meta.get("min")),
                "max": (row[max_col] if (max_col and pd.notna(row.get(max_col))) else meta.get("max")),
                "label": meta["label"],
                "unit": meta["unit"],
                "sex": "Male" if astronaut in ["C001", "C004"] else "Female",
            }
            tidy_records.append(rec)

    # Derived analyte: Anion Gap (Sodium - Chlorine - Carbon Dioxide)
    na_col  = _first_col_startswith(df, "sodium_value")
    cl_col  = _first_col_startswith(df, "chloride_value")
    co2_col = _first_col_startswith(df, "carbon_dioxide_value")
    if all([na_col, cl_col, co2_col]):
        for _, row in df.iterrows():
            astronaut = row["astronautID"]
            try:
                val = float(row[na_col]) - float(row[cl_col]) - float(row[co2_col])
                val = round(val, 1)  # tenths place
            except Exception:
                val = np.nan

            rec = {
                "astronautID": astronaut,
                "timepoint": row["timepoint"],
                "flight_day": parse_timepoint(row["timepoint"]),
                "analyte": "anion_gap",
                "value": val,
                "min": ANALYTE_INFO["anion_gap"]["min"],
                "max": ANALYTE_INFO["anion_gap"]["max"],
                "label": ANALYTE_INFO["anion_gap"]["label"],
                "unit": ANALYTE_INFO["anion_gap"]["unit"],
                "sex": "Male" if astronaut in ["C001", "C004"] else "Female",
            }
            tidy_records.append(rec)

    return pd.DataFrame(tidy_records)

# Statistical Comparison: R+1 vs L-series
def analyze_r1_vs_L(tidy: pd.DataFrame) -> pd.DataFrame:
    """
    Compare R+1 vs L-series for each analyte.
    - Within-astronaut: one-sample t-test (H0: mean(L) == R+1)
      Returns per-astronaut mean, std, SE, t-stat, p-value, and Cohen's d.
    - Across-astronauts (group-level): paired t-test on per-astronaut mean(L) vs R+1
      Returns group mean, std across astronauts, SEM, t-stat, p-value, and Cohen's d.
    """
    results = []
    for analyte, subdf in tidy.groupby("analyte"):

        ## Within-astronaut tests
        for astronaut, adf in subdf.groupby("astronautID"):
            L_mask = adf["timepoint"].astype(str).str.startswith("L")
            R1_mask = adf["timepoint"].astype(str).isin(["R+1", "R1", "R+01"])

            L_vals = adf.loc[L_mask, "value"].dropna().astype(float)
            R1_vals = adf.loc[R1_mask, "value"].dropna().astype(float)

            if len(L_vals) >= 2 and len(R1_vals) == 1:
                R1 = float(R1_vals.iloc[0])
                mean_L = float(L_vals.mean())
                std_L = float(L_vals.std(ddof=1))
                n_L = int(L_vals.shape[0])

                if std_L > 0:
                    se = std_L / np.sqrt(n_L)
                    t_stat = (mean_L - R1) / se
                    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=n_L - 1))
                    cohen_d = (R1 - mean_L) / std_L
                else:
                    se = t_stat = p_val = cohen_d = np.nan

                results.append({
                    "analyte": analyte,
                    "astronautID": astronaut,
                    "test_type": "within",
                    "n_L": n_L,
                    "mean_L": round(mean_L, 2),
                    "R1": round(R1, 2),
                    "std_L": round(std_L, 2),
                    "se_L": round(se, 2) if pd.notna(se) else np.nan,
                    "t_stat": round(t_stat, 3) if pd.notna(t_stat) else np.nan,
                    "p_value": round(p_val, 4) if pd.notna(p_val) else np.nan,
                    "effect_size": round(cohen_d, 3) if pd.notna(cohen_d) else np.nan,
                })

        ## Across-astronauts (paired test)
        astronaut_means, astronaut_R1 = [], []
        for astronaut, adf in subdf.groupby("astronautID"):
            L_mask = adf["timepoint"].astype(str).str.startswith("L")
            R1_mask = adf["timepoint"].astype(str).isin(["R+1", "R1", "R+01"])

            L_vals = adf.loc[L_mask, "value"].dropna().astype(float)
            R1_vals = adf.loc[R1_mask, "value"].dropna().astype(float)

            if len(L_vals) >= 2 and len(R1_vals) == 1:
                astronaut_means.append(float(L_vals.mean()))
                astronaut_R1.append(float(R1_vals.iloc[0]))

        if len(astronaut_means) >= 2:
            diffs = np.array(astronaut_R1) - np.array(astronaut_means)
            t_stat, p_val = stats.ttest_rel(astronaut_R1, astronaut_means)

            # Group-level variability
            std_L = np.std(astronaut_means, ddof=1)
            se_L = std_L / np.sqrt(len(astronaut_means))

            cohen_d = diffs.mean() / diffs.std(ddof=1) if diffs.std(ddof=1) > 0 else np.nan

            results.append({
                "analyte": analyte,
                "astronautID": "ALL",
                "test_type": "group",
                "n_L": len(astronaut_means),
                "mean_L": round(float(np.mean(astronaut_means)), 2),
                "R1": round(float(np.mean(astronaut_R1)), 2),
                "t_stat": round(float(t_stat), 3),
                "p_value": round(float(p_val), 4),
                "effect_size": round(float(cohen_d), 3) if pd.notna(cohen_d) else np.nan,
            })

    return pd.DataFrame(results)
