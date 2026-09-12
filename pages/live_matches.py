import streamlit as st
import pandas as pd
import subprocess
import sys
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Live Matches",
    page_icon="🏏",
    layout="wide"
)

# ==============================
# PAGE TITLE
# ==============================

st.title("🏏 Live Cricket Matches")

st.markdown(
    "Current match information collected from the Cricbuzz API."
)

# ==============================
# REFRESH LIVE DATA
# ==============================

col_refresh, col_time = st.columns([1, 3])

with col_refresh:

    if st.button(
        "🔄 Refresh Live Data",
        use_container_width=True
    ):

        with st.spinner("Fetching latest cricket data..."):

            try:

                # Fetch latest API data
                api_result = subprocess.run(
                    [sys.executable, "utils/api.py"],
                    capture_output=True,
                    text=True
                )

                if api_result.returncode == 0:

                    # Update MySQL database
                    db_result = subprocess.run(
                        [sys.executable, "database/insert_matches.py"],
                        capture_output=True,
                        text=True
                    )

                    if db_result.returncode == 0:

                        st.success(
                            "✅ API data and MySQL database updated successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ API updated, but MySQL update failed."
                        )

                        st.code(db_result.stderr)

                else:

                    st.error(
                        "❌ Failed to fetch latest API data."
                    )

                    st.code(api_result.stderr)

            except Exception as e:

                st.error(
                    f"❌ Refresh error: {e}"
                )


with col_time:

    if os.path.exists("data/live_matches.csv"):

        modified_time = os.path.getmtime(
            "data/live_matches.csv"
        )

        last_updated = datetime.fromtimestamp(
            modified_time
        ).strftime("%d %b %Y, %I:%M:%S %p")

        st.info(
            f"🕒 Last data update: {last_updated}"
        )


# ==============================
# LOAD MATCH DATA
# ==============================

try:

    df = pd.read_csv(
        "data/live_matches.csv"
    )

    st.success(
        f"{len(df)} matches loaded successfully!"
    )

    # ==============================
    # SUMMARY METRICS
    # ==============================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🏏 Total Matches",
            len(df)
        )

    with col2:

        st.metric(
            "🏆 Series",
            df["series_name"].nunique()
        )

    with col3:

        st.metric(
            "🏟️ Venues",
            df["venue"].nunique()
        )

    st.divider()

    # ==============================
    # MATCH STATUS CLASSIFICATION
    # ==============================

    def classify_status(status):

        status = str(status).lower()

        if (
            "won by" in status
            or "match abandoned" in status
        ):

            return "Completed"

        elif "innings break" in status:

            return "Live"

        elif "stumps" in status:

            return "Ongoing"

        else:

            return "Live"


    df["status_category"] = df["status"].apply(
        classify_status
    )

    # ==============================
    # MATCH STATUS SUMMARY
    # ==============================

    st.subheader(
        "📊 Match Status Summary"
    )

    status_counts = df[
        "status_category"
    ].value_counts()

    st.bar_chart(
        status_counts
    )

    st.divider()

    # ==============================
    # STATUS FILTER
    # ==============================

    st.subheader(
        "🎯 Filter by Match Status"
    )

    status_filter = st.selectbox(
        "Select status",
        [
            "All Matches",
            "Live",
            "Ongoing",
            "Completed"
        ]
    )

    # ==============================
    # SEARCH
    # ==============================

    st.subheader(
        "🔎 Search Matches"
    )

    search = st.text_input(
        "Search by team, series, venue, or match",
        placeholder="Example: India, England, County..."
    )

    # ==============================
    # APPLY FILTER
    # ==============================

    if status_filter == "All Matches":

        filtered_df = df.copy()

    else:

        filtered_df = df[
            df["status_category"] == status_filter
        ].copy()


    # ==============================
    # APPLY SEARCH
    # ==============================

    if search:

        mask = (
            filtered_df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )

        filtered_df = filtered_df[mask]

    # ==============================
    # MATCH TABLE
    # ==============================

    st.subheader(
        "📋 Match List"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing {len(filtered_df)} "
        f"of {len(df)} matches"
    )


except FileNotFoundError:

    st.error(
        "❌ live_matches.csv was not found."
    )


except Exception as e:

    st.error(
        f"❌ An error occurred: {e}"
    )