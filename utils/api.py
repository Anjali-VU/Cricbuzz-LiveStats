import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CRICBUZZ_API_KEY")
API_HOST = os.getenv("CRICBUZZ_API_HOST")

BASE_URL = f"https://{API_HOST}"


def get_live_matches():
    """Fetch live cricket matches from Cricbuzz API."""

    url = f"{BASE_URL}/matches/live"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def extract_live_matches(data):
    """Extract individual live matches from API response."""

    matches = []

    type_matches = data.get("data", {}).get("typeMatches", [])

    for match_type in type_matches:

        series_matches = match_type.get("seriesMatches", [])

        for series_data in series_matches:

            series_wrapper = series_data.get(
                "seriesAdWrapper", {}
            )

            series_name = series_wrapper.get(
                "seriesName"
            )

            series_id = series_wrapper.get(
                "seriesId"
            )

            match_list = series_wrapper.get(
                "matches", []
            )

            for match_data in match_list:

                match_info = match_data.get(
                    "matchInfo", {}
                )

                match_score = match_data.get(
                    "matchScore", {}
                )

                matches.append({
                    "match_id": match_info.get("matchId"),
                    "series_id": series_id,
                    "series_name": series_name,
                    "match_description": match_info.get(
                        "matchDesc"
                    ),
                    "match_format": match_info.get(
                        "matchFormat"
                    ),
                    "state": match_info.get("state"),
                    "status": match_info.get("status"),
                    "team1": match_info.get(
                        "team1", {}
                    ).get("teamName"),
                    "team2": match_info.get(
                        "team2", {}
                    ).get("teamName"),
                    "venue": match_info.get(
                        "venueInfo", {}
                    ).get("ground"),
                    "city": match_info.get(
                        "venueInfo", {}
                    ).get("city"),
                })

    return matches


if __name__ == "__main__":

    data = get_live_matches()

    matches = extract_live_matches(data)

    print(f"Total matches found: {len(matches)}")

    df = pd.DataFrame(matches)

    # Clean text columns
    text_columns = [
        "series_name",
        "match_description",
        "match_format",
        "state",
        "status",
        "team1",
        "team2",
        "venue",
        "city"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # Save cleaned data as CSV backup
    df.to_csv("data/live_matches.csv", index=False)

    print("\nCSV backup created successfully!")

    print("\nLive Match DataFrame:")
    print(df)

    print("\nDataFrame Shape:")
    print(df.shape)

    print("\nDataFrame Columns:")
    print(df.columns.tolist())