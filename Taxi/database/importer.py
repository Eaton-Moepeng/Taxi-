"""
importer.py
-----------
Imports CSV data into the Taxi! database.

Expected folder structure:

Taxi/
│
├── data/
│   ├── provinces.csv
│   ├── cities.csv
│   ├── locations.csv
│   ├── hand_signals.csv
│   └── routes.csv
│
└── database/
    ├── importer.py
"""

from pathlib import Path
import csv

from database.database import get_session
from database.models import (
    Province,
    City,
    Location,
    HandSignal,
    Route,
)


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"


# ============================================================
# Helper
# ============================================================

def csv_reader(filename: str):
    """
    Returns rows from a CSV file as dictionaries.
    """

    file = DATA_FOLDER / filename

    if not file.exists():
        print(f"Missing file: {filename}")
        return []

    with open(file, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ============================================================
# Provinces
# ============================================================

def import_provinces():

    session = get_session()

    for row in csv_reader("provinces.csv"):

        exists = (
            session.query(Province)
            .filter_by(name=row["name"])
            .first()
        )

        if exists:
            continue

        session.add(
            Province(
                name=row["name"]
            )
        )

    session.commit()
    session.close()

    print("Imported provinces.")


# ============================================================
# Cities
# ============================================================

def import_cities():

    session = get_session()

    for row in csv_reader("cities.csv"):

        province = (
            session.query(Province)
            .filter_by(name=row["province"])
            .first()
        )

        if province is None:
            continue

        exists = (
            session.query(City)
            .filter_by(
                name=row["name"],
                province=province
            )
            .first()
        )

        if exists:
            continue

        session.add(

            City(
                name=row["name"],
                province=province
            )

        )

    session.commit()
    session.close()

    print("Imported cities.")


# ============================================================
# Locations
# ============================================================

def import_locations():

    session = get_session()

    for row in csv_reader("locations.csv"):

        city = (
            session.query(City)
            .filter_by(name=row["city"])
            .first()
        )

        if city is None:
            continue

        exists = (
            session.query(Location)
            .filter_by(
                name=row["name"]
            )
            .first()
        )

        if exists:
            continue

        latitude = (
            float(row["latitude"])
            if row["latitude"]
            else None
        )

        longitude = (
            float(row["longitude"])
            if row["longitude"]
            else None
        )

        session.add(

            Location(
                city=city,
                name=row["name"],
                location_type=row["location_type"],
                latitude=latitude,
                longitude=longitude,
                description=row["description"],
            )

        )

    session.commit()
    session.close()

    print("Imported locations.")


# ============================================================
# Hand Signals
# ============================================================

def import_hand_signals():

    session = get_session()

    for row in csv_reader("hand_signals.csv"):

        exists = (
            session.query(HandSignal)
            .filter_by(name=row["name"])
            .first()
        )

        if exists:
            continue

        session.add(

            HandSignal(
                name=row["name"],
                description=row["description"],
                image_path=row["image_path"],
                animation_path=row["animation_path"],
            )

        )

    session.commit()
    session.close()

    print("Imported hand signals.")


# ============================================================
# Routes
# ============================================================

def import_routes():

    session = get_session()

    for row in csv_reader("routes.csv"):

        origin = (
            session.query(Location)
            .filter_by(name=row["origin"])
            .first()
        )

        destination = (
            session.query(Location)
            .filter_by(name=row["destination"])
            .first()
        )

        signal = (
            session.query(HandSignal)
            .filter_by(name=row["signal"])
            .first()
        )

        if not origin or not destination or not signal:
            continue

        exists = (
            session.query(Route)
            .filter_by(
                origin=origin,
                destination=destination,
            )
            .first()
        )

        if exists:
            continue

        fare_min = (
            float(row["fare_min"])
            if row["fare_min"]
            else None
        )

        fare_max = (
            float(row["fare_max"])
            if row["fare_max"]
            else None
        )

        distance = (
            float(row["distance_km"])
            if row["distance_km"]
            else None
        )

        minutes = (
            int(row["estimated_minutes"])
            if row["estimated_minutes"]
            else None
        )

        session.add(

            Route(
                origin=origin,
                destination=destination,
                signal=signal,
                fare_min=fare_min,
                fare_max=fare_max,
                estimated_minutes=minutes,
                distance_km=distance,
                notes=row["notes"],
            )

        )

    session.commit()
    session.close()

    print("Imported routes.")


# ============================================================
# Import Everything
# ============================================================

def import_everything():

    print()

    print("=" * 50)
    print("Taxi! Data Import")
    print("=" * 50)

    import_provinces()
    import_cities()
    import_locations()
    import_hand_signals()
    import_routes()

    print("=" * 50)
    print("Import complete.")
    print("=" * 50)


if __name__ == "__main__":
    import_everything()