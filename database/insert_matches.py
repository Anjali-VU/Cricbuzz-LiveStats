import pandas as pd
from db_connection import get_connection


CSV_FILE = "data/live_matches.csv"


def get_or_create_series(cursor, series_id, series_name, match_type):
    """Get existing series or create a new one."""

    cursor.execute(
        """
        SELECT series_id
        FROM series
        WHERE series_id = %s
        """,
        (series_id,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        """
        INSERT INTO series (
            series_id,
            series_name,
            match_type
        )
        VALUES (%s, %s, %s)
        """,
        (
            series_id,
            series_name,
            match_type
        )
    )

    return series_id


def get_or_create_team(cursor, team_name):
    """Get existing team or create a new one."""

    cursor.execute(
        """
        SELECT team_id
        FROM teams
        WHERE team_name = %s
        """,
        (team_name,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        """
        INSERT INTO teams (team_name)
        VALUES (%s)
        """,
        (team_name,)
    )

    return cursor.lastrowid


def get_or_create_venue(cursor, venue_name, city):
    """Get existing venue or create a new one."""

    cursor.execute(
        """
        SELECT venue_id
        FROM venues
        WHERE venue_name = %s
        AND city = %s
        """,
        (venue_name, city)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        """
        INSERT INTO venues (
            venue_name,
            city
        )
        VALUES (%s, %s)
        """,
        (
            venue_name,
            city
        )
    )

    return cursor.lastrowid


def insert_matches():
    """Insert API match data into MySQL."""

    df = pd.read_csv(CSV_FILE)

    connection = get_connection()
    cursor = connection.cursor()

    processed_count = 0

    for _, row in df.iterrows():

        match_id = int(row["match_id"])
        series_id = int(row["series_id"])

        # 1. Create/get series
        get_or_create_series(
            cursor,
            series_id,
            row["series_name"],
            row["match_format"]
        )

        # 2. Create/get teams
        team1_id = get_or_create_team(
            cursor,
            row["team1"]
        )

        team2_id = get_or_create_team(
            cursor,
            row["team2"]
        )

        # 3. Create/get venue
        venue_id = get_or_create_venue(
            cursor,
            row["venue"],
            row["city"]
        )

        # 4. Check if match already exists
        cursor.execute(
            """
            SELECT match_id
            FROM matches
            WHERE match_id = %s
            """,
            (match_id,)
        )

        existing_match = cursor.fetchone()

        if existing_match:

            cursor.execute(
                """
                UPDATE matches
                SET match_description = %s,
                    match_status = %s,
                    match_type = %s,
                    series_id = %s,
                    team1_id = %s,
                    team2_id = %s,
                    venue_id = %s
                WHERE match_id = %s
                """,
                (
                    row["match_description"],
                    row["status"],
                    row["match_format"],
                    series_id,
                    team1_id,
                    team2_id,
                    venue_id,
                    match_id
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO matches (
                    match_id,
                    match_description,
                    match_status,
                    match_type,
                    series_id,
                    team1_id,
                    team2_id,
                    venue_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    match_id,
                    row["match_description"],
                    row["status"],
                    row["match_format"],
                    series_id,
                    team1_id,
                    team2_id,
                    venue_id
                )
            )

        processed_count += 1

    connection.commit()

    print(
        f"{processed_count} matches inserted/updated successfully!"
    )

    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_matches()