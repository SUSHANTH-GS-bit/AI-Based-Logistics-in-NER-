from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

try:
    from backend.database import Base
except ModuleNotFoundError:
    from database import Base


class Vehicle(Base):
    """
    Vehicles table: Tracks registered transport vehicles carrying essential supplies.
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # 1-to-many relationship: One vehicle can have multiple historic GPS locations
    locations = relationship(
        "VehicleLocation",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )


class VehicleLocation(Base):
    """
    Vehicle Locations table: Stores time-series GPS tracking points for each vehicle.
    """
    __tablename__ = "vehicle_locations"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(50), ForeignKey("vehicles.vehicle_id"), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    # Unique idempotency key from offline client to prevent duplicate sync submissions
    client_record_id = Column(String(100), unique=True, index=True, nullable=True)

    # Back reference to the Vehicle
    vehicle = relationship("Vehicle", back_populates="locations")


class Incident(Base):
    """
    Incidents table: Stores geo-tagged road disruptions, landslides, and accidents.
    """
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(50), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    incident_type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    # Unique idempotency key from offline client to prevent duplicate sync submissions
    client_record_id = Column(String(100), unique=True, index=True, nullable=True)
