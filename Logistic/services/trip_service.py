
from datetime import datetime, timezone
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import (
    Trip, TripShipment, Shipment, ShipmentEvent,
    Vehicle, AuditLog
)
from auth.permissions import require_permission


def start_trip(trip_id, username, role):
    require_permission(role, "routes.manage")

    now = datetime.now(timezone.utc).isoformat()

    with SessionLocal.begin() as db:
        trip = db.get(Trip, trip_id)

        if not trip or trip.status != "Planned":
            raise ValueError("Trip cannot be started.")

        trip.status = "In Progress"
        trip.actual_start = now

        assignments = db.scalars(
            select(TripShipment).where(
                TripShipment.trip_id == trip_id
            )
        ).all()

        for assignment in assignments:
            shipment = db.get(Shipment, assignment.shipment_id)

            if shipment.status not in ("Confirmed",):
                raise ValueError(
                    "A shipment is not ready for dispatch."
                )

            shipment.status = "In Transit"

            db.add(ShipmentEvent(
                shipment_id=shipment.id,
                status="In Transit",
                location=trip.start_location,
                remarks=f"Departed on {trip.trip_number}"
            ))

        db.add(AuditLog(
            username=username,
            action="Trip Started",
            details=trip.trip_number
        ))


def complete_trip(trip_id, username, role):
    require_permission(role, "routes.manage")

    now = datetime.now(timezone.utc).isoformat()

    with SessionLocal.begin() as db:
        trip = db.get(Trip, trip_id)

        if not trip or trip.status != "In Progress":
            raise ValueError("Trip is not in progress.")

        trip.status = "Completed"
        trip.actual_end = now

        vehicle = db.get(Vehicle, trip.vehicle_id)
        vehicle.status = "Available"

        db.add(AuditLog(
            username=username,
            action="Trip Completed",
            details=trip.trip_number
        ))

    # Completing a trip does NOT automatically deliver shipments.
    # Delivery confirmation is a separate business operation.
