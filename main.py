import os
import pandas as pd

from scripts.featureEngineering import add_flight_day
from scripts.stats import tidy_from_wide, analyze_r1_vs_L
from scripts.graphMaking import make_figure


def run_pipeline(filename, folder="final_data",
                 analytes=None, astronauts=None,
                 show_error=None):
    """
    Run pipeline: load data, clean, tidy, stats, and show interactive plot.
    `astronauts` can be:
      - None -> all
      - "Male" / "Female" -> filter by sex
      - list of IDs -> filter by astronaut IDs
    """
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    print(f"\nLoading {path} ...")
    df_raw = pd.read_csv(path)

    # 1. Feature engineering
    df_clean = add_flight_day(df_raw)

    # 2. Reshape to tidy format
    tidy_df = tidy_from_wide(df_clean)

    # 3. Run stats
    stats_df = analyze_r1_vs_L(tidy_df)

    # Default analyte if none chosen
    if not analytes:
        analytes = ["sodium"] if "sodium" in tidy_df["analyte"].unique() \
            else [tidy_df["analyte"].unique()[0]]

    print(f"Generating figure for analytes: {analytes}")

    for analyte in analytes:
        print(f"\nPlotting {analyte} ...")
        fig = make_figure(
            tidy_df=tidy_df,
            stats_df=stats_df,
            analytes=[analyte],
            astronaut_filter=astronauts,
            show_error=show_error
        )
        fig.show()


if __name__ == "__main__":
    # List available files
    files = [f for f in os.listdir("final_data") if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No CSV files found in final_data/")

    print("Available datasets:")
    for i, f in enumerate(files):
        print(f"  [{i}] {f}")

    # Choose dataset
    idx = input(f"Select dataset [0-{len(files)-1}] (default=0): ").strip()
    idx = int(idx) if idx.isdigit() and 0 <= int(idx) < len(files) else 0
    filename = files[idx]

    # Choose analytes
    df_preview = pd.read_csv(os.path.join("final_data", filename))
    df_preview = add_flight_day(df_preview)
    tidy_preview = tidy_from_wide(df_preview)
    available_analytes = tidy_preview["analyte"].unique().tolist()

    print("\nAvailable analytes:", ", ".join(available_analytes))
    ana_in = input("Enter analytes (comma-separated, default=sodium): ").strip().lower()
    analytes = [a.strip() for a in ana_in.split(",") if a.strip()] if ana_in else ["sodium"]

    # Choose participants (All / Male / Female / Subset)
    available_astronauts = [a.upper() for a in tidy_preview["astronautID"].unique().tolist()]
    print("\nAvailable astronauts:", ", ".join(available_astronauts))
    print("Options: 'All', 'Male', 'Female', or a comma-separated subset (e.g. C001,C002)")
    choice = input("Select group (default=All): ").strip()

    if not choice or choice.lower() == "all":
        astronauts = None
    elif choice.lower() in ["male", "female"]:
        astronauts = choice.capitalize()
    else:
        astronauts = [c.strip().upper() for c in choice.split(",") if c.strip()]

    # Choose error band type
    err_in = input("Show error band? [none/within/group] (default=none): ").strip().lower()
    show_error = {"none": None, "within": "within", "group": "group"}.get(err_in, None)

    # Run pipeline
    run_pipeline(filename, analytes=analytes,
                 astronauts=astronauts,
                 show_error=show_error)