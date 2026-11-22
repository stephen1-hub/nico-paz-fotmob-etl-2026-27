## Nico Paz FotMob ETL — Serie A 2026/27 In-Season Snapshot

An ETL pipeline that extracts Nico Paz player data from FotMob, transforms player metrics and shot-map data into CSV files, and loads them into a SQLite database.

This is an **in-season snapshot**, not final 2026/27 season statistics. The data reflects the source at the time the pipeline is run.

### Data source

FotMob player data for Nico Paz.

### Outputs

- `nico_paz_2026_27_metrics.csv` — player metrics
- `nico_paz_2026_27_shotmap.csv` — shot-map data
- `nico_paz_2026_27.db` — SQLite database

The pipeline loaded 41 metric records and 48 shot records.

### Run the pipeline

```bash
python src/nico_paz_etl.py
