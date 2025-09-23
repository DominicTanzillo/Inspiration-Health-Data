import os
import pandas as pd
from pathlib import Path

def process_files(input_dir="cleaned_data"):
    # Ensure directory exists
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Directory {input_dir} not found.")
        return

    # Get all CSV files
    csv_files = [f for f in input_path.iterdir() if f.suffix == ".csv"]
    if not csv_files:
        print("No CSV files found in", input_dir)
        return

    for filepath in csv_files:
        filename = filepath.stem  # file name without extension
        print(f"\nProcessing {filepath.name}...")

        # Read CSV
        df = pd.read_csv(filepath)

        # --- Step 1: Split "Sample Name" ---
        if "Sample Name" not in df.columns:
            print(f"❌ Skipping {filepath.name} (no 'Sample Name' column).")
            continue

        split_cols = df["Sample Name"].str.split("_", expand=True)

        # Expected format: C001_serum_L-3 → astronautID=C001, serum (ignored), timepoint=L-3
        if split_cols.shape[1] >= 3:
            df["astronautID"] = split_cols[0]
            df["timepoint"] = split_cols[2]
        else:
            print(f"⚠️ Unexpected 'Sample Name' format in {filepath.name}")
            continue

        # --- Step 2: Check for missing values ---
        missing = df.isnull().sum()
        if missing.any():
            print("🔎 Missing values found:\n", missing[missing > 0])

        # --- Step 3: Check for duplicates ---
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"🔎 Found {duplicates} duplicated rows")

        # --- Step 4: Save combined file ---
        all_astronauts_file = filepath.parent / f"{filename}_all_astronauts.csv"
        df.to_csv(all_astronauts_file, index=False)
        print(f"✅ Saved {all_astronauts_file.name}")

        # --- Step 5: Save per astronaut ---
        for astro_id, sub_df in df.groupby("astronautID"):
            out_file = filepath.parent / f"{filename}_{astro_id}.csv"
            sub_df.to_csv(out_file, index=False)
            print(f"   ↳ Saved {out_file.name}")

if __name__ == "__main__":
    process_files("cleaned_data")
