from extract_nico_paz import main as extract_nico_paz
from transform_nico_paz_metrics import main as transform_nico_paz_metrics
from transform_nico_paz_shotmap import main as transform_nico_paz_shotmap
from load_nico_paz import main as load_nico_paz


def main():
    print("\n=== NICO PAZ ETL: 2026/27 SERIE A SNAPSHOT ===")

    print("\n[1/4] Extracting FotMob player data...")
    extract_nico_paz()

    print("\n[2/4] Transforming player metrics...")
    transform_nico_paz_metrics()

    print("\n[3/4] Transforming shot-map data...")
    transform_nico_paz_shotmap()

    print("\n[4/4] Loading Nico Paz database...")
    load_nico_paz()

    print("\nNico Paz ETL completed successfully.")


if __name__ == "__main__":
    main()