import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "nico_paz_player_data.json"
OUTPUT_FILE = PROJECT_ROOT / "nico_paz_2026_27_metrics.csv"

SEASON = "2026/2027"
COMPETITION = "Serie A"


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    stats_section = data["firstSeasonStats"]["statsSection"]
    rows = []

    for group in stats_section.get("items", []):
        category = group.get("title", "Uncategorized")

        for item in group.get("items", []):
            rows.append({
                "season": SEASON,
                "competition": COMPETITION,
                "category": category,
                "metric": item.get("title"),
                "value": item.get("statValue"),
                "per90": item.get("per90"),
                "percentile": item.get("percentileRank"),
                "per90_percentile": item.get("percentileRankPer90"),
            })

    metrics_df = pd.DataFrame(rows)

    if metrics_df.empty:
        raise ValueError("No metrics were extracted. Check the JSON structure.")

    metrics_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Metrics extracted: {len(metrics_df)} rows")
    print(f"Saved: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()