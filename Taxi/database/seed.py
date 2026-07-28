from database.database import create_database, get_session
from database.models import (
    Province,
    City,
    Location,
    TaxiAssociation,
    HandSignal,
    Language,
)


def seed_database():

    create_database()

    session = get_session()

    # -------------------------------------------------
    # Prevent duplicate seeding
    # -------------------------------------------------

    if session.query(Province).first():
        print("Database already contains data.")
        session.close()
        return

    # -------------------------------------------------
    # Provinces
    # -------------------------------------------------

    gauteng = Province(name="Gauteng")
    kzn = Province(name="KwaZulu-Natal")
    western_cape = Province(name="Western Cape")
    eastern_cape = Province(name="Eastern Cape")
    free_state = Province(name="Free State")
    limpopo = Province(name="Limpopo")
    mpumalanga = Province(name="Mpumalanga")
    north_west = Province(name="North West")
    northern_cape = Province(name="Northern Cape")

    session.add_all([
        gauteng,
        kzn,
        western_cape,
        eastern_cape,
        free_state,
        limpopo,
        mpumalanga,
        north_west,
        northern_cape,
    ])

    session.commit()

    # -------------------------------------------------
    # Cities
    # -------------------------------------------------

    johannesburg = City(
        name="Johannesburg",
        province=gauteng
    )

    pretoria = City(
        name="Pretoria",
        province=gauteng
    )

    midrand = City(
        name="Midrand",
        province=gauteng
    )

    session.add_all([
        johannesburg,
        pretoria,
        midrand,
    ])

    session.commit()

    # -------------------------------------------------
    # Locations
    # -------------------------------------------------

    locations = [

        Location(
            city=johannesburg,
            name="Bree Taxi Rank",
            location_type="Taxi Rank"
        ),

        Location(
            city=johannesburg,
            name="Noord Taxi Rank",
            location_type="Taxi Rank"
        ),

        Location(
            city=johannesburg,
            name="Southgate",
            location_type="Mall"
        ),

        Location(
            city=midrand,
            name="Halfway House",
            location_type="Suburb"
        ),

        Location(
            city=midrand,
            name="Fourways",
            location_type="Suburb"
        ),

    ]

    session.add_all(locations)

    # -------------------------------------------------
    # Taxi Associations
    # -------------------------------------------------

    session.add_all([

        TaxiAssociation(
            name="Johannesburg Taxi Association"
        ),

        TaxiAssociation(
            name="Noord Taxi Association"
        ),

    ])

    # -------------------------------------------------
    # Hand Signals
    # -------------------------------------------------

    session.add_all([

        HandSignal(
            name="One Finger Up",
            description="Johannesburg CBD / Noord / Bree"
        ),

        HandSignal(
            name="Index Finger Down",
            description="Local route"
        ),

        HandSignal(
            name="Three Fingers",
            description="Southgate"
        ),

        HandSignal(
            name="Four Fingers",
            description="Fourways"
        ),

        HandSignal(
            name="Open Hand",
            description="Bree / Noord Taxi Rank"
        ),

        HandSignal(
            name="Two-Hand Cutting Motion",
            description="Halfway House"
        ),

    ])

    # -------------------------------------------------
    # Languages
    # -------------------------------------------------

    session.add_all([

        Language(
            name="English",
            code="en"
        ),

        Language(
            name="isiZulu",
            code="zu"
        ),

        Language(
            name="Afrikaans",
            code="af"
        ),

        Language(
            name="Sesotho",
            code="st"
        ),

        Language(
            name="Xitsonga",
            code="ts"
        ),

        Language(
            name="Setswana",
            code="tn"
        ),

    ])

    session.commit()

    session.close()

    print("=" * 60)
    print("Taxi! database successfully seeded.")
    print("=" * 60)


if __name__ == "__main__":
    seed_database()