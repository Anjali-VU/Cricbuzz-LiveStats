import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Match Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Match Analytics")
st.markdown(
    "Explore cricket matches using interactive analytics."
)

try:
    # Load data
    df = pd.read_csv("data/live_matches.csv")

    # ==============================
    # OVERVIEW
    # ==============================

    st.subheader("📌 Match Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Matches",
            len(df)
        )

    with col2:
        st.metric(
            "Test Matches",
            (df["match_format"].str.upper() == "TEST").sum()
        )

    with col3:
        st.metric(
            "ODI Matches",
            (df["match_format"].str.upper() == "ODI").sum()
        )

    with col4:
        st.metric(
            "T20 Matches",
            (df["match_format"].str.upper() == "T20").sum()
        )

    st.divider()

    # ==============================
    # MATCH FORMAT ANALYSIS
    # ==============================

    st.subheader("🏏 Matches by Format")

    format_counts = (
        df["match_format"]
        .str.upper()
        .value_counts()
    )

    st.bar_chart(format_counts)

    st.divider()

    # ==============================
    # SERIES ANALYSIS
    # ==============================

    st.subheader("🏆 Matches by Series")

    series_counts = (
        df["series_name"]
        .value_counts()
    )

    st.bar_chart(series_counts)

    st.divider()

    # ==============================
    # VENUE ANALYSIS
    # ==============================

    st.subheader("🏟️ Matches by Venue")

    venue_counts = (
        df["venue"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(venue_counts)

    st.divider()

    # ==============================
    # MATCH DETAILS
    # ==============================

    st.subheader("📋 Match Details")

    st.dataframe(
        df[
            [
                "match_id",
                "series_name",
                "match_description",
                "match_format",
                "status",
                "team1",
                "team2",
                "venue",
                "city"
            ]
        ],
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