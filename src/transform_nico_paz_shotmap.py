import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "nico_paz_player_data.json"
OUTPUT_FILE = PROJECT_ROOT / "nico_paz_2026_27_shotmap.csv"

SEASON = "2026/2027"
COMPETITION = "Serie A"


def flatten_dict(data, parent_key="", separator="_"):
    flattened = {}

    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            flattened.update(flatten_dict(value, new_key, separator))
        else:
            flattened[new_key] = value

    return flattened


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    shotmap = data["firstSeasonStats"].get("shotmap", [])

    rows = []

    for shot in shotmap:
        row = flatten_dict(shot)
        row["season"] = SEASON
        row["competition"] = COMPETITION
        rows.append(row)

    shots_df = pd.DataFrame(rows)

    if shots_df.empty:
        raise ValueError("No shots were extracted. Check the JSON structure.")

    shots_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Shots extracted: {len(shots_df)} rows")
    print(f"Saved: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()