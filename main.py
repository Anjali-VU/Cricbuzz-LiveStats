import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    df = pd.read_csv("data/live_matches.csv")
except Exception:
    df = pd.DataFrame()


# =========================================================
# CUSTOM STREAMLIT CSS
# Only CSS - NO HTML CARDS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f4f7fb;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b1935;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce4ef;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #53627a;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #102044;
        font-weight: 800;
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Headings */
    h1 {
        color: #102044;
    }

    h2 {
        color: #152750;
    }

    h3 {
        color: #20355e;
    }

    /* Divider */
    hr {
        border-color: #dce4ef;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CALCULATE METRICS
# =========================================================

if not df.empty:

    total_matches = len(df)

    total_teams = pd.concat(
        [
            df["team1"],
            df["team2"]
        ]
    ).dropna().nunique()

    total_series = df["series_name"].dropna().nunique()

    total_venues = df["venue"].dropna().nunique()

else:

    total_matches = 0
    total_teams = 0
    total_series = 0
    total_venues = 0


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:

    st.title("🏏 Cricbuzz LiveStats")

    st.subheader(
        "Real-Time Cricket Insights & SQL-Based Analytics"
    )

    st.write(
        "An interactive cricket analytics dashboard powered by "
        "Python, MySQL, REST API and Streamlit."
    )


with header_col2:

    st.success("🟢 API Connected")

    st.caption(
        "Live cricket data dashboard"
    )


st.divider()


# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

st.header("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        label="🏏 Total Matches",
        value=total_matches,
        delta="Live & Upcoming"
    )


with col2:

    st.metric(
        label="👥 Total Teams",
        value=total_teams,
        delta="Active Teams"
    )


with col3:

    st.metric(
        label="🏆 Total Series",
        value=total_series,
        delta="Available Series"
    )


with col4:

    st.metric(
        label="🏟️ Total Venues",
        value=total_venues,
        delta="Available Venues"
    )


st.divider()


# =========================================================
# ANALYTICS SECTION
# =========================================================

left, right = st.columns([1.5, 1])


# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.header("📡 Live Match Center")

    if not df.empty:

        # Status summary
        status_counts = (
            df["status"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Matches"
        ]

        status_col1, status_col2, status_col3 = st.columns(3)

        live_count = 0
        upcoming_count = 0
        completed_count = 0

        for status, count in zip(
            status_counts["Status"],
            status_counts["Matches"]
        ):

            status_text = str(status).lower()

            if "live" in status_text:
                live_count += count

            elif "upcoming" in status_text or "preview" in status_text:
                upcoming_count += count

            elif "complete" in status_text or "result" in status_text:
                completed_count += count

        with status_col1:
            st.metric(
                "🟢 Live",
                live_count
            )

        with status_col2:
            st.metric(
                "🟡 Upcoming",
                upcoming_count
            )

        with status_col3:
            st.metric(
                "🔵 Completed",
                completed_count
            )


        st.write("")


        # Recent matches
        display_columns = [
            "team1",
            "team2",
            "match_format",
            "status",
            "venue"
        ]

        available_columns = [
            column
            for column in display_columns
            if column in df.columns
        ]

        st.dataframe(
            df[available_columns].head(8),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No live match data is currently available."
        )


# =========================================================
# RIGHT SIDE - FORMAT CHART
# =========================================================

with right:

    st.header("🎯 Match Format")

    if not df.empty:

        format_data = (
            df["match_format"]
            .fillna("Other")
            .astype(str)
            .str.upper()
            .value_counts()
            .reset_index()
        )

        format_data.columns = [
            "Format",
            "Matches"
        ]

        fig = px.pie(
            format_data,
            names="Format",
            values="Matches",
            hole=0.55
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            legend_title="Format"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No format data available."
        )


st.divider()


# =========================================================
# TOP TEAMS
# =========================================================

st.header("🏆 Top Teams by Match Appearances")

if not df.empty:

    team_counts = pd.concat(
        [
            df["team1"],
            df["team2"]
        ]
    ).dropna().value_counts().head(10)

    team_data = team_counts.reset_index()

    team_data.columns = [
        "Team",
        "Matches"
    ]

    fig = px.bar(
        team_data,
        x="Matches",
        y="Team",
        orientation="h",
        text="Matches"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=420,
        margin=dict(
            l=10,
            r=40,
            t=20,
            b=20
        ),
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No team data available."
    )


st.divider()


# =========================================================
# DASHBOARD NAVIGATION
# =========================================================

st.header("🚀 Explore Dashboard")

nav1, nav2, nav3, nav4 = st.columns(4)


with nav1:

    st.subheader("📡 Live Matches")

    st.write(
        "View current cricket matches, teams, "
        "venues and match status."
    )

    st.page_link(
        "pages/live_matches.py",
        label="Open Live Matches →",
        icon="🏏"
    )


with nav2:

    st.subheader("📊 Match Analytics")

    st.write(
        "Analyze match formats, series, venues "
        "and cricket trends."
    )

    st.page_link(
        "pages/match_analytics.py",
        label="Open Match Analytics →",
        icon="📊"
    )


with nav3:

    st.subheader("👤 Player Statistics")

    st.write(
        "Explore batting, bowling and fielding "
        "performance."
    )

    st.page_link(
        "pages/player_statistics.py",
        label="Open Player Statistics →",
        icon="👤"
    )


with nav4:

    st.subheader("🗄️ SQL Analytics")

    st.write(
        "Explore cricket data using MySQL "
        "and SQL queries."
    )

    st.page_link(
        "pages/sql_analytics.py",
        label="Open SQL Analytics →",
        icon="🗄️"
    )


st.divider()


# =========================================================
# TECHNOLOGY STACK
# =========================================================

st.header("🛠️ Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

with tech1:

    st.info(
        """
        🐍 **Python**

        Data processing
        & analytics
        """
    )


with tech2:

    st.info(
        """
        🗄️ **MySQL**

        Database
        management
        """
    )


with tech3:

    st.info(
        """
        📊 **Streamlit**

        Interactive
        dashboard
        """
    )


with tech4:

    st.info(
        """
        🌐 **REST API**

        Live cricket
        data
        """
    )


with tech5:

    st.info(
        """
        📈 **Plotly**

        Interactive
        visualizations
        """
    )


st.divider()


# =========================================================
# PROJECT INFORMATION
# =========================================================

with st.expander("ℹ️ About Cricbuzz LiveStats"):

    st.write(
        """
        **Cricbuzz LiveStats** is a cricket analytics project
        designed to collect cricket data through a REST API,
        process the data using Python, store structured data
        in MySQL and present analytical insights through
        Streamlit.

        ### Main Components

        - 🏏 Real-time cricket match data
        - 🐍 Python data processing
        - 🗄️ MySQL database
        - 📊 SQL analytics
        - 📈 Interactive Plotly charts
        - 🌐 REST API integration
        - 🎨 Streamlit dashboard
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.success(
    "🟢 Cricbuzz LiveStats is ready. "
    "Use the sidebar or dashboard buttons to explore the project."
)