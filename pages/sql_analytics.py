import streamlit as st
import pandas as pd
from database.db_connection import get_connection

st.set_page_config(
    page_title="SQL Analytics",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Analytics")
st.markdown(
    "Explore cricket data using SQL queries on the MySQL database."
)

try:
    connection = get_connection()

    # ==========================================
    # 1. TOTAL MATCHES
    # ==========================================

    st.subheader("📊 Database Overview")

    query_matches = """
        SELECT COUNT(*) AS total_matches
        FROM matches
    """

    total_matches = pd.read_sql(
        query_matches,
        connection
    ).iloc[0]["total_matches"]

    # ==========================================
    # 2. TOTAL TEAMS
    # ==========================================

    query_teams = """
        SELECT COUNT(*) AS total_teams
        FROM teams
    """

    total_teams = pd.read_sql(
        query_teams,
        connection
    ).iloc[0]["total_teams"]

    # ==========================================
    # 3. TOTAL SERIES
    # ==========================================

    query_series = """
        SELECT COUNT(*) AS total_series
        FROM series
    """

    total_series = pd.read_sql(
        query_series,
        connection
    ).iloc[0]["total_series"]

    # ==========================================
    # 4. TOTAL VENUES
    # ==========================================

    query_venues = """
        SELECT COUNT(*) AS total_venues
        FROM venues
    """

    total_venues = pd.read_sql(
        query_venues,
        connection
    ).iloc[0]["total_venues"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏏 Matches",
            total_matches
        )

    with col2:
        st.metric(
            "👥 Teams",
            total_teams
        )

    with col3:
        st.metric(
            "🏆 Series",
            total_series
        )

    with col4:
        st.metric(
            "🏟️ Venues",
            total_venues
        )

    st.divider()

    # ==========================================
    # MATCHES BY FORMAT
    # ==========================================

    st.subheader("🏏 Matches by Format")

    format_query = """
        SELECT
            match_type AS Match_Type,
            COUNT(*) AS Matches
        FROM matches
        GROUP BY match_type
        ORDER BY Matches DESC
    """

    format_data = pd.read_sql(
        format_query,
        connection
    )

    st.dataframe(
        format_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        format_data.set_index("Match_Type")
    )

    st.divider()

    # ==========================================
    # MATCHES BY SERIES
    # ==========================================

    st.subheader("🏆 Matches by Series")

    series_query = """
        SELECT
            s.series_name AS Series,
            COUNT(m.match_id) AS Matches
        FROM matches m
        INNER JOIN series s
            ON m.series_id = s.series_id
        GROUP BY s.series_id, s.series_name
        ORDER BY Matches DESC
    """

    series_data = pd.read_sql(
        series_query,
        connection
    )

    st.dataframe(
        series_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        series_data.set_index("Series")
    )

    st.divider()

    # ==========================================
    # MATCHES BY VENUE
    # ==========================================

    st.subheader("🏟️ Matches by Venue")

    venue_query = """
        SELECT
            v.venue_name AS Venue,
            v.city AS City,
            COUNT(m.match_id) AS Matches
        FROM matches m
        INNER JOIN venues v
            ON m.venue_id = v.venue_id
        GROUP BY v.venue_id, v.venue_name, v.city
        ORDER BY Matches DESC
    """

    venue_data = pd.read_sql(
        venue_query,
        connection
    )

    st.dataframe(
        venue_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # TEAM MATCH APPEARANCES
    # ==========================================

    st.subheader("👥 Team Match Appearances")

    team_query = """
        SELECT
            t.team_name AS Team,
            COUNT(*) AS Matches
        FROM (
            SELECT team1_id AS team_id
            FROM matches

            UNION ALL

            SELECT team2_id AS team_id
            FROM matches
        ) match_teams

        INNER JOIN teams t
            ON match_teams.team_id = t.team_id

        GROUP BY t.team_id, t.team_name
        ORDER BY Matches DESC
    """

    team_data = pd.read_sql(
        team_query,
        connection
    )

    st.dataframe(
        team_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        team_data.set_index("Team")
    )

    connection.close()

except Exception as e:

    st.error(
        f"❌ Database error: {e}"
    )