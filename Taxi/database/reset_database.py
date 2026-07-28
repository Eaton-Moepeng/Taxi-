"""
reset_database.py

Deletes the existing Taxi! database and creates
a fresh database with seed data.

Usage:
    python database/reset_database.py
"""

from pathlib import Path

from database.database import DATABASE_FILE
from database.seed import seed_database


def reset_database():

    if DATABASE_FILE.exists():
        DATABASE_FILE.unlink()
        print("Old database removed.")

    seed_database()

    print("New Taxi! database created successfully.")


if __name__ == "__main__":
    reset_database()