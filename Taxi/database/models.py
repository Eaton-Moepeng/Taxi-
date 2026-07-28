"""
models.py
----------
SQLAlchemy models for the Taxi! application.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    Boolean,
    DateTime,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


# ============================================================
# Province
# ============================================================

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    cities = relationship("City", back_populates="province")

    def __repr__(self):
        return f"<Province {self.name}>"


# ============================================================
# City
# ============================================================

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)

    province_id = Column(Integer, ForeignKey("provinces.id"))

    name = Column(String(100), nullable=False)

    province = relationship("Province", back_populates="cities")

    locations = relationship("Location", back_populates="city")

    def __repr__(self):
        return f"<City {self.name}>"


# ============================================================
# Taxi Association
# ============================================================

class TaxiAssociation(Base):
    __tablename__ = "taxi_associations"

    id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)

    phone = Column(String(30))

    email = Column(String(120))

    notes = Column(Text)

    routes = relationship("Route", back_populates="association")

    def __repr__(self):
        return f"<Association {self.name}>"


# ============================================================
# Location
# ============================================================

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)

    city_id = Column(Integer, ForeignKey("cities.id"))

    name = Column(String(150), nullable=False)

    location_type = Column(
        String(50),
        nullable=False
    )
    # Examples:
    # Taxi Rank
    # Mall
    # Suburb
    # Hospital
    # Campus
    # Township
    # Landmark

    latitude = Column(Float)

    longitude = Column(Float)

    description = Column(Text)

    city = relationship("City", back_populates="locations")

    origin_routes = relationship(
        "Route",
        foreign_keys="Route.origin_location_id",
        back_populates="origin",
    )

    destination_routes = relationship(
        "Route",
        foreign_keys="Route.destination_location_id",
        back_populates="destination",
    )

    def __repr__(self):
        return f"<Location {self.name}>"


# ============================================================
# Hand Signal
# ============================================================

class HandSignal(Base):
    __tablename__ = "hand_signals"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    description = Column(Text)

    image_path = Column(String(255))

    animation_path = Column(String(255))

    routes = relationship("Route", back_populates="signal")

    def __repr__(self):
        return f"<Signal {self.name}>"


# ============================================================
# Route
# ============================================================

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)

    origin_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False,
    )

    destination_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False,
    )

    signal_id = Column(
        Integer,
        ForeignKey("hand_signals.id"),
        nullable=False,
    )

    association_id = Column(
        Integer,
        ForeignKey("taxi_associations.id"),
    )

    fare_min = Column(Float)

    fare_max = Column(Float)

    estimated_minutes = Column(Integer)

    distance_km = Column(Float)

    notes = Column(Text)

    active = Column(Boolean, default=True)

    origin = relationship(
        "Location",
        foreign_keys=[origin_location_id],
        back_populates="origin_routes",
    )

    destination = relationship(
        "Location",
        foreign_keys=[destination_location_id],
        back_populates="destination_routes",
    )

    signal = relationship(
        "HandSignal",
        back_populates="routes",
    )

    association = relationship(
        "TaxiAssociation",
        back_populates="routes",
    )

    def __repr__(self):
        return (
            f"<Route {self.origin_location_id}"
            f" -> {self.destination_location_id}>"
        )


# ============================================================
# Language
# ============================================================

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    code = Column(String(10), nullable=False, unique=True)

    translations = relationship(
        "Translation",
        back_populates="language",
    )

    def __repr__(self):
        return f"<Language {self.name}>"


# ============================================================
# Translation
# ============================================================

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True)

    signal_id = Column(
        Integer,
        ForeignKey("hand_signals.id"),
    )

    language_id = Column(
        Integer,
        ForeignKey("languages.id"),
    )

    translated_text = Column(Text)

    language = relationship(
        "Language",
        back_populates="translations",
    )

    signal = relationship("HandSignal")

    def __repr__(self):
        return f"<Translation {self.id}>"


# ============================================================
# Favourite Route
# ============================================================

class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True)

    nickname = Column(String(100))

    origin_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
    )

    destination_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
    )

    created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# ============================================================
# Community Report (Future)
# ============================================================

class CommunityReport(Base):
    __tablename__ = "community_reports"

    id = Column(Integer, primary_key=True)

    route_id = Column(
        Integer,
        ForeignKey("routes.id"),
    )

    report_type = Column(String(100))
    # Fare Change
    # Wrong Signal
    # Road Closed
    # Route Closed
    # New Route

    description = Column(Text)

    created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    verified = Column(Boolean, default=False)

    route = relationship("Route")