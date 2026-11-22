import json
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "nico_paz_player_data.json"

URL = "https://www.fotmob.com/api/data/playerData"
PARAMS = {"id": "1347574"}
HEADERS = {"User-Agent": "Mozilla/5.0"}


def main():
    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print(f"HTTP status: {response.status_code}")
    print(f"Saved raw JSON: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()