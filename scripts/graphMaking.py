import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def make_figure(
    tidy_df: pd.DataFrame,
    stats_df: pd.DataFrame,
    analytes: list,
    astronaut_filter=None,
    show_error: str = None
):
    """
    Build interactive mission-day plots with stats overlays.
    """

    fig = go.Figure()

    # Highlight stretched space interval (0 to 30 days)
    fig.add_vrect(x0=0, x1=30, fillcolor="LightGray", opacity=0.3,
                  layer="below", line_width=0)
    for day in [10, 20]:
        fig.add_vline(x=day, line=dict(color="white", width=2, dash="dot"),
                      layer="below")

    df = tidy_df.copy()

    # Apply participant filter
    if astronaut_filter is None:
        pass  # show all
    elif isinstance(astronaut_filter, str) and astronaut_filter in ["Male", "Female"]:
        if "sex" in df.columns:
            df = df[df["sex"] == astronaut_filter]
    elif isinstance(astronaut_filter, (list, tuple, set)):
        df = df[df["astronautID"].isin(astronaut_filter)]

    # Loop analytes requested
    for analyte in analytes:
        subdf = df[df["analyte"] == analyte]
        if subdf.empty:
            print(f"[make_figure] Skipping {analyte} – no data")
            continue

        ## Y-axis scaling
        ref_min = subdf["min"].dropna().min()
        ref_max = subdf["max"].dropna().max()
        data_min = subdf["value"].min()
        data_max = subdf["value"].max()

        if "unit" in subdf.columns and not subdf["unit"].dropna().empty:
            unit = subdf["unit"].dropna().iloc[0]
            y_label = f"{analyte.title()} ({unit})"
        else:
            y_label = analyte.title()

        ## Add healthy range lines from min / max
        if pd.notna(ref_min):
            fig.add_hline(
                y=ref_min,
                line=dict(color="green", width=2, dash="dot"),
                annotation_text="Min",
                annotation_position="bottom right"
            )
        if pd.notna(ref_max):
            fig.add_hline(
                y=ref_max,
                line=dict(color="green", width=2, dash="dot"),
                annotation_text="Max",
                annotation_position="top right"
            )

        ## Decide axis limits: must include BOTH healthy range and all data
        low_candidates = [v for v in [ref_min, data_min] if pd.notna(v)]
        high_candidates = [v for v in [ref_max, data_max] if pd.notna(v)]

        if low_candidates and high_candidates:
            low = min(low_candidates)
            high = max(high_candidates)
            span = high - low if high > low else 1
            padding = 0.1 * span
            y_range = [low - padding, high + padding]
        else:
            y_range = None

        ## Apply axis update once
        if y_range:
            fig.update_yaxes(title=y_label, range=y_range)
        else:
            fig.update_yaxes(title=y_label)

        ## Plot each astronaut trace - first colors
        palette = px.colors.qualitative.Set2
        astronaut_colors = {astr: palette[i % len(palette)]
                            for i, astr in enumerate(subdf["astronautID"].unique())}

        ## Plot each astronaut trace
        for astronaut, adf in subdf.groupby("astronautID"):
            if adf.empty:
                continue
            adf = adf.sort_values("flight_day")
            base_color = astronaut_colors[astronaut]

            ### Skip if astronaut not in filter
            if isinstance(astronaut_filter, (list, tuple, set)) and astronaut not in astronaut_filter:
                continue

            # Main Scatter Plot
            fig.add_trace(go.Scatter(
                x=adf["flight_day"],
                y=adf["value"],
                mode="lines+markers",
                name=f"{astronaut} ({analyte})",
                hovertext=adf["timepoint"],
                hovertemplate="Day %{hovertext}<br>Value %{y}<extra></extra>",
                line=dict(color=base_color),
                marker=dict(color=base_color)
            ))

            ### Within-astronaut error band
            if show_error == "within" and not stats_df.empty:
                stat_rows = stats_df[
                    (stats_df["analyte"] == analyte)
                    & (stats_df["test_type"] == "within")
                    ]

                for _, row in stat_rows.iterrows():
                    astronaut = row["astronautID"]
                    if astronaut not in subdf["astronautID"].unique():
                        continue  # skip astronauts not in this analyte subset

                    mean_L = row.get("mean_L", np.nan)
                    se = row.get("se_L", np.nan)
                    R1 = row.get("R1", np.nan)

                    if pd.isna(mean_L) or pd.isna(se):
                        continue

                    base_color = astronaut_colors.get(astronaut, "gray")
                    if base_color.startswith("rgb"):
                        fill_color = base_color.replace("rgb", "rgba").replace(")", ",0.15)")
                    else:
                        fill_color = base_color

                    #### Horizontal band: L +/- SE
                    fig.add_hrect(
                        y0=mean_L - se, y1=mean_L + se,
                        fillcolor=fill_color,
                        opacity=0.2,
                        line_width=0,
                        layer="below"
                    )

                    #### Asterisk if R+1 outside band
                    if pd.notna(R1) and (R1 < mean_L - se or R1 > mean_L + se):
                        fig.add_annotation(
                            x=31,
                            y=R1,
                            text="*",
                            showarrow=False,
                            font=dict(size=20, color="red"),
                            yshift=15
                        )

        ## Group-level error band
        if show_error == "group" and not stats_df.empty:
            stat_rows = stats_df[
                (stats_df["analyte"] == analyte)
                & (stats_df["test_type"] == "group")
                ]

            for _, row in stat_rows.iterrows():
                mean_L = row.get("mean_L", np.nan)
                n = row.get("n_L", 0)

                error = np.nan
                if pd.notna(row.get("effect_size")) and n > 1 and row["effect_size"] != 0:
                    error = abs(row.get("R1", np.nan) - mean_L) / abs(row["effect_size"])
                if pd.isna(error):
                    error = 0

                #### Filter bands only if stats_df has group info
                should_plot = True
                if "group" in row.index and astronaut_filter is not None:
                    group_id = row["group"]

                    if isinstance(astronaut_filter, str) and astronaut_filter in ["Male", "Female"]:
                        should_plot = (group_id == astronaut_filter)
                    elif isinstance(astronaut_filter, (list, tuple, set)):
                        # Only show if group_id matches one of the selected astronauts
                        should_plot = (group_id in astronaut_filter)

                if should_plot and pd.notna(mean_L):
                    fig.add_hrect(
                        y0=mean_L - error, y1=mean_L + error,
                        fillcolor="gray", opacity=0.2,
                        layer="below", line_width=0,
                        annotation_text = "Group Error Band",
                        annotation_position="top left"
                    )

                    if row.get("p_value") is not None and row["p_value"] < 0.05:
                        fig.add_annotation(
                            x=31,  # R+1 = 31
                            y=row.get("R1", mean_L),
                            text="*",
                            showarrow=False,
                            font=dict(size=20, color="red"),
                            yshift=15
                        )

        ## Only update range if ref_min/ref_max are valid
        if pd.notna(ref_min) and pd.notna(ref_max):
            fig.update_yaxes(title=y_label,
                             range=[ref_min * 0.9, ref_max * 1.1])
        else:
            fig.update_yaxes(title=y_label)

    # Layout: Build Dynamic Title
    if astronaut_filter is None:
        group_label = "All Participants"
    elif isinstance(astronaut_filter, str) and astronaut_filter in ["Male", "Female"]:
        group_label = f"{astronaut_filter} Participants"
    elif isinstance(astronaut_filter, (list, tuple, set)):
        group_label = "Subset: " + ", ".join(astronaut_filter)
    else:
        group_label = "Participants"

    # Build analyte label with units if available
    ana_label = ", ".join(analytes)
    unit_label = ""
    subdf = df[df["analyte"] == analytes[0]]
    if "unit" in subdf.columns and not subdf["unit"].dropna().empty:
        unit_label = f" ({subdf['unit'].dropna().iloc[0]})"

    fig.update_layout(
        title=f"{ana_label.title()}{unit_label} Trends ({group_label})",
        xaxis_title="Mission Day",
        legend_title="Participant / Analyte",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=60, r=30, t=60, b=60)
    )

    # Custom ticks
    ticks = [t for t in sorted(df["flight_day"].dropna().unique()) if pd.notna(t)]
    ticktext = []
    for t in ticks:
        if t >= 30:
            lbl = f"R+{int(t-30)}"
        else:
            lbl = f"L{int(t)}"
        ticktext.append(lbl)
    if ticks:
        fig.update_xaxes(tickmode="array", tickvals=ticks, ticktext=ticktext)

    return fig