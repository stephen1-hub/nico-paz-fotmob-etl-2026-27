import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

st.set_page_config(
    page_title="Nico Paz | Player Analytics",
    page_icon="⚽",
    layout="wide",
)

METRICS_FILE = "nico_paz_2026_27_metrics.csv"
SHOTMAP_FILE = "nico_paz_2026_27_shotmap.csv"

st.title("⚽ Nico Paz | Player Analytics")
st.caption("2026/27 season • Player metrics and shot map")

@st.cache_data
def load_data():
    metrics = pd.read_csv(METRICS_FILE)
    shots = pd.read_csv(SHOTMAP_FILE)
    return metrics, shots

try:
    metrics, shots = load_data()
except Exception as e:
    st.error(f"Could not load the CSV files: {e}")
    st.stop()

# Clean numeric fields
for col in ["value", "per90", "percentile", "per90_percentile"]:
    if col in metrics.columns:
        metrics[col] = pd.to_numeric(metrics[col], errors="coerce")

for col in ["x", "y", "expectedGoals", "min", "expectedGoalsOnTarget"]:
    if col in shots.columns:
        shots[col] = pd.to_numeric(shots[col], errors="coerce")

# Sidebar filters
st.sidebar.header("Filters")

if "category" in metrics.columns:
    categories = sorted(metrics["category"].dropna().unique())
    selected_category = st.sidebar.selectbox("Metric category", ["All"] + categories)
    if selected_category != "All":
        metrics_view = metrics[metrics["category"] == selected_category]
    else:
        metrics_view = metrics.copy()
else:
    metrics_view = metrics.copy()

if "situation" in shots.columns:
    situations = sorted(shots["situation"].dropna().unique())
    selected_situation = st.sidebar.selectbox("Shot situation", ["All"] + situations)
    if selected_situation != "All":
        shots_view = shots[shots["situation"] == selected_situation]
    else:
        shots_view = shots.copy()
else:
    shots_view = shots.copy()

# Match filter
if "matchId" in shots.columns:
    match_cols = [
        col for col in
        ["matchId", "matchDate", "homeTeamName", "awayTeamName",
         "homeScore", "awayScore"]
        if col in shots.columns
    ]

    matches = shots[match_cols].drop_duplicates("matchId").copy()

    def match_label(row):
        date = str(row.get("matchDate", ""))
        home = str(row.get("homeTeamName", "Home"))
        away = str(row.get("awayTeamName", "Away"))
        score = ""

        if pd.notna(row.get("homeScore")) and pd.notna(row.get("awayScore")):
            score = f" ({int(row['homeScore'])}-{int(row['awayScore'])})"

        return f"{date} | {home} vs {away}{score}"

    match_labels = {
        row["matchId"]: match_label(row)
        for _, row in matches.iterrows()
    }

    match_ids = matches["matchId"].tolist()
    selected_match = st.sidebar.selectbox(
        "Match",
        options=["All matches"] + match_ids,
        format_func=lambda value: (
            "All matches" if value == "All matches"
            else match_labels.get(value, str(value))
        ),
    )

    if selected_match != "All matches":
        shots_view = shots_view[shots_view["matchId"] == selected_match]

# Overview metrics
c1, c2, c3 = st.columns(3)
c1.metric("Metrics tracked", len(metrics))
c2.metric("Shots in dataset", len(shots))
c3.metric(
    "Goals",
    int(shots["eventType"].astype(str).str.contains("goal", case=False, na=False).sum())
    if "eventType" in shots.columns else "—"
)

st.divider()

# Player metrics
st.subheader("Player Metrics")

if not metrics_view.empty:
    display_cols = [
        col for col in
        ["metric", "value", "per90", "percentile", "per90_percentile"]
        if col in metrics_view.columns
    ]

    st.dataframe(
        metrics_view[display_cols].sort_values(
            "value", ascending=False, na_position="last"
        ),
        use_container_width=True,
        hide_index=True,
    )

    if "metric" in metrics_view.columns and "value" in metrics_view.columns:
        chart_data = metrics_view.dropna(subset=["value"]).sort_values("value")
        if not chart_data.empty:
            fig = px.bar(
                chart_data,
                x="value",
                y="metric",
                orientation="h",
                title="Metric Values",
                labels={"value": "Value", "metric": ""},
                hover_data=[
                    c for c in ["per90", "percentile", "per90_percentile"]
                    if c in chart_data.columns
                ],
            )
            fig.update_layout(height=max(400, len(chart_data) * 28))
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No metrics match the selected category.")

st.divider()

# Shot map — vertical Opta-style pitch
st.subheader("Shot Map")

if {"x", "y"}.issubset(shots_view.columns):
    shot_data = shots_view.dropna(subset=["x", "y"]).copy()

    if not shot_data.empty:
        # Match-specific summary
        total_shots = len(shot_data)

        total_xg = (
            pd.to_numeric(shot_data["expectedGoals"], errors="coerce").sum()
            if "expectedGoals" in shot_data.columns else 0
        )

        goals = (
            shot_data["eventType"].astype(str)
            .str.contains("goal", case=False, na=False).sum()
            if "eventType" in shot_data.columns else 0
        )

        k1, k2, k3 = st.columns(3)
        k1.metric("Shots", total_shots)
        k2.metric("Goals", int(goals))
        k3.metric("Total xG", f"{total_xg:.2f}")

        # Create vertical pitch
        pitch = VerticalPitch(
            pitch_type="opta",
            half=False,
            pitch_color="#0b1220",
            line_color="#d7dee8",
            linewidth=1.2,
            goal_type="box",
        )

        fig, ax = pitch.draw(figsize=(5, 7))
        fig.patch.set_facecolor("#0b1220")
        ax.set_facecolor("#0b1220")

        event_colors = {
            "Goal": "#22c55e",
            "AttemptSaved": "#38bdf8",
            "Miss": "#f59e0b",
            "Post": "#f43f5e",
        }

        shot_data["plot_color"] = (
            shot_data["eventType"]
            .map(event_colors)
            .fillna("#c084fc")
        )

        if "expectedGoals" in shot_data.columns:
            xg = pd.to_numeric(
                shot_data["expectedGoals"], errors="coerce"
            ).fillna(0).clip(lower=0)

            marker_sizes = 35 + xg * 350
        else:
            marker_sizes = 65

        pitch.scatter(
            shot_data["x"],
            shot_data["y"],
            ax=ax,
            s=marker_sizes,
            c=shot_data["plot_color"],
            edgecolors="white",
            linewidths=0.6,
            alpha=0.9,
            zorder=3,
        )

        legend_items = [
            plt.Line2D(
                [0], [0],
                marker="o",
                color="none",
                markerfacecolor=color,
                markeredgecolor="white",
                markersize=8,
                label=label,
            )
            for label, color in event_colors.items()
        ]

        ax.legend(
            handles=legend_items,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.04),
            ncol=4,
            frameon=False,
            labelcolor="white",
        )

        st.pyplot(fig, use_container_width=False)
        plt.close(fig)

    else:
        st.info("No shot locations available for the selected filter.")

else:
    st.warning("The shot-map CSV does not contain x and y coordinates.")