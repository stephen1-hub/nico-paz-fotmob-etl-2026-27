# Nico Paz FotMob ETL — Serie A 2026/27

An ETL pipeline that extracts Nico Paz player data from FotMob, transforms player metrics and shot-map data into CSV files, and loads the results into a SQLite database.

This project captures an **in-season snapshot** of the 2026/27 Serie A season. The outputs reflect the data available from FotMob when the pipeline is run; they are not final season statistics.

## Project objective

Build a repeatable workflow for collecting, transforming, and storing football player data for analysis.

The pipeline focuses on two datasets:

- **Player metrics** — statistical records for Nico Paz.
- **Shot-map data** — individual shot records available from the source.

## Data source

- **Source:** FotMob
- **Player:** Nico Paz
- **Competition:** Serie A
- **Season:** 2026/27
- **Data type:** In-season snapshot

## ETL workflow

The pipeline follows an Extract, Transform, Load process:

1. **Extract** — retrieve Nico Paz's player data from FotMob.
2. **Transform** — process the player metrics and shot-map data into separate CSV datasets.
3. **Load** — store the transformed data in a SQLite database.

## Project outputs

| Output | Description |
|---|---|
| `nico_paz_2026_27_metrics.csv` | Player metrics dataset |
| `nico_paz_2026_27_shotmap.csv` | Shot-map dataset |
| `nico_paz_2026_27.db` | SQLite database containing the pipeline outputs |

The recorded run produced **41 metric records** and **48 shot records**.

## Run the pipeline

From the repository root, run:

```bash
python src/nico_paz_etl.py
```

The pipeline extracts the current available data, processes the datasets, and loads the results into the SQLite database.

## Technologies

- Python
- pandas
- SQLite
- FotMob data

## Scope and limitations

- This is a player-focused ETL project, not a full-league data pipeline.
- The outputs represent the data available when the pipeline runs and may change as the season progresses.
- The project should not be interpreted as a final 2026/27 season report.

## Potential next steps

- Schedule the pipeline to refresh the snapshot regularly.
- Add data-quality checks and logging.
- Track changes between snapshots over time.
- Build an analysis dashboard using the stored data.

## Author

Stephen Yaw Ayamah
