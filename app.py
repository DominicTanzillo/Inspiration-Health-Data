import os
import pandas as pd
import streamlit as st

# Import modules
from scripts.featureEngineering import add_flight_day
from scripts.stats import tidy_from_wide, analyze_r1_vs_L
from scripts.graphMaking import make_figure

# Load Data
def list_final_data(folder="final_data"):
    """Return list of CSV files in final_data folder."""
    return [f for f in os.listdir(folder) if f.endswith(".csv")]

def load_final_data(fname, folder="final_data"):
    """Load selected CSV file as pandas DataFrame."""
    path = os.path.join(folder, fname)
    return pd.read_csv(path)

# Main App
def main():
    st.title("Astronaut Biochemistry Dashboard")

    # 1. Sidebar file selection
    st.sidebar.header("Data Selection")
    csv_files = list_final_data()

    if not csv_files:
        st.error("No CSV files found in final_data/")
        return

    selected_file = st.sidebar.selectbox("Choose dataset", csv_files)
    df_raw = load_final_data(selected_file)
    st.write(f"Loaded file: **{selected_file}**")

    # 2. Clean with feature engineering
    df_clean = add_flight_day(df_raw)

    # 3. Transform to tidy format + run stats
    tidy_df = tidy_from_wide(df_clean)
    stats_df = analyze_r1_vs_L(tidy_df)

    # 4. Sidebar user selections
    st.sidebar.header("Plot Controls")

    analyte = st.sidebar.selectbox(
        "Select Analyte",
        options=tidy_df["analyte"].unique().tolist(),
        index=tidy_df["analyte"].unique().tolist().index("sodium")
        if "sodium" in tidy_df["analyte"].unique() else 0
    )

    astronauts = st.sidebar.multiselect(
        "Select Astronauts",
        # Normalize IDs to uppercase for consistency
        options=sorted([a.upper() for a in tidy_df["astronautID"].unique().tolist()]),
        default=[]
    )
    astronauts = [a.upper() for a in astronauts]

    sex_filter = st.sidebar.radio(
        "Sex Filter",
        ["All", "Male", "Female"],
        index=0
    )

    show_error = st.sidebar.radio(
        "Error Band",
        ["None", "within", "group"],
        index=0
    )
    show_error = None if show_error == "None" else show_error

    # Unify filters: Astronauts take priority, else fall back to sex filter
    if astronauts:
        astronaut_filter = astronauts
    elif sex_filter != "All":
        astronaut_filter = sex_filter
    else:
        astronaut_filter = None

    # 5. Generate figure
    if analyte:
        fig = make_figure(
            tidy_df=tidy_df,
            stats_df=stats_df,
            analytes=[analyte],
            astronaut_filter=astronaut_filter,
            show_error=show_error
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one analyte to plot.")

    # 6. Optional: preview data
    with st.expander("Preview Data"):
        st.dataframe(tidy_df.head(20))

if __name__ == "__main__":
    main()