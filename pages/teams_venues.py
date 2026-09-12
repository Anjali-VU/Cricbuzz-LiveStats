import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Teams & Venues",
    page_icon="🏟️",
    layout="wide"
)

st.title("🏟️ Teams & Venues")
st.markdown("Explore teams and venues from the Cricbuzz match data.")

try:
    df = pd.read_csv("data/live_matches.csv")

    # ==============================
    # TEAM ANALYSIS
    # ==============================

    st.subheader("🏏 Teams")

    teams = pd.concat(
        [
            df["team1"],
            df["team2"]
        ]
    ).dropna().unique()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Teams",
            len(teams)
        )

    with col2:
        st.metric(
            "Total Matches",
            len(df)
        )

    st.dataframe(
        pd.DataFrame({"Team": sorted(teams)}),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==============================
    # VENUE ANALYSIS
    # ==============================

    st.subheader("🏟️ Venues")

    venue_counts = (
        df.groupby(["venue", "city"])
        .size()
        .reset_index(name="Matches")
        .sort_values("Matches", ascending=False)
    )

    st.metric(
        "Total Venues",
        df["venue"].nunique()
    )

    st.bar_chart(
        venue_counts.set_index("venue")["Matches"]
    )

    st.dataframe(
        venue_counts,
        use_container_width=True,
        hide_index=True
    )

except FileNotFoundError:

    st.error(
        "❌ live_matches.csv was not found."
    )

except Exception as e:

    st.error(
        f"❌ An error occurred: {e}"
    )