import streamlit as st
import pandas as pd
from database.db_connection import get_connection

st.set_page_config(
    page_title="Player Statistics",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Player Statistics")
st.markdown(
    "Player information and performance statistics from MySQL."
)

try:
    connection = get_connection()

    # ==========================================
    # PLAYER DATA
    # ==========================================

    player_query = """
        SELECT
            player_id,
            player_name,
            full_name,
            team_id,
            playing_role,
            batting_style,
            bowling_style,
            country
        FROM players
        ORDER BY player_name
    """

    players = pd.read_sql(
        player_query,
        connection
    )

    # ==========================================
    # PLAYER OVERVIEW
    # ==========================================

    st.subheader("📌 Player Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👤 Total Players",
            len(players)
        )

    with col2:
        batsmen = (
            players["playing_role"]
            .fillna("")
            .str.lower()
            .str.contains("batsman")
            .sum()
        )

        st.metric(
            "🏏 Batsmen",
            batsmen
        )

    with col3:
        st.metric(
            "🌍 Countries",
            players["country"].nunique()
        )

    st.divider()

    # ==========================================
    # SEARCH PLAYER
    # ==========================================

    st.subheader("🔎 Search Player")

    search = st.text_input(
        "Search by player name or country",
        placeholder="Example: Virat Kohli or India"
    )

    if search:
        filtered_players = players[
            players.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]
    else:
        filtered_players = players

    # ==========================================
    # PLAYER INFORMATION
    # ==========================================

    st.subheader("📋 Player Information")

    st.dataframe(
        filtered_players,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # BATTING PERFORMANCE
    # ==========================================

    st.subheader("🏏 Batting Performance")

    batting_query = """
        SELECT
            p.player_name AS Player,
            bp.runs AS Runs,
            bp.balls_faced AS `Balls Faced`,
            bp.fours AS Fours,
            bp.sixes AS Sixes,
            bp.strike_rate AS `Strike Rate`,
            CASE
                WHEN bp.is_out = 1 THEN 'Yes'
                ELSE 'No'
            END AS Dismissed
        FROM batting_performance bp
        INNER JOIN players p
            ON bp.player_id = p.player_id
        ORDER BY bp.runs DESC
    """

    batting_data = pd.read_sql(
        batting_query,
        connection
    )

    if batting_data.empty:
        st.info(
            "ℹ️ No batting performance data available."
        )
    else:

        st.dataframe(
            batting_data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📊 Runs by Player")

        runs_chart = batting_data.set_index(
            "Player"
        )[["Runs"]]

        st.bar_chart(runs_chart)

    st.divider()

    # ==========================================
    # BOWLING PERFORMANCE
    # ==========================================

    st.subheader("🎯 Bowling Performance")

    bowling_query = """
        SELECT
            p.player_name AS Player,
            bp.overs AS Overs,
            bp.maidens AS Maidens,
            bp.runs_conceded AS `Runs Conceded`,
            bp.wickets AS Wickets,
            bp.economy_rate AS `Economy Rate`
        FROM bowling_performance bp
        INNER JOIN players p
            ON bp.player_id = p.player_id
        ORDER BY bp.wickets DESC
    """

    bowling_data = pd.read_sql(
        bowling_query,
        connection
    )

    if bowling_data.empty:

        st.info(
            "ℹ️ No bowling performance data available."
        )

    else:

        st.dataframe(
            bowling_data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📊 Wickets by Player")

        wickets_chart = bowling_data.set_index(
            "Player"
        )[["Wickets"]]

        st.bar_chart(wickets_chart)

    st.divider()

    # ==========================================
    # FIELDING PERFORMANCE
    # ==========================================

    st.subheader("🧤 Fielding Performance")

    fielding_query = """
        SELECT
            p.player_name AS Player,
            fp.catches AS Catches,
            fp.stumpings AS Stumpings,
            fp.run_outs AS `Run Outs`
        FROM fielding_performance fp
        INNER JOIN players p
            ON fp.player_id = p.player_id
        ORDER BY fp.catches DESC
    """

    fielding_data = pd.read_sql(
        fielding_query,
        connection
    )

    if fielding_data.empty:

        st.info(
            "ℹ️ No fielding performance data available."
        )

    else:

        st.dataframe(
            fielding_data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📊 Catches by Player")

        catches_chart = fielding_data.set_index(
            "Player"
        )[["Catches"]]

        st.bar_chart(catches_chart)

    connection.close()

except Exception as e:

    st.error(
        f"❌ Database error: {e}"
    )