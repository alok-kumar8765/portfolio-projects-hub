
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import (
    Vehicle, Driver, Trip, Shipment, TripShipment, AuditLog
)
from auth.permissions import require_permission


def create_trip(
    vehicle_id,
    driver_id,
    shipment_ids,
    start_location,
    end_location,
    planned_start,
    distance_km,
    username,
    role
):
    require_permission(role, "routes.manage")

    if not shipment_ids:
        raise ValueError("Select at least one shipment.")

    if len(set(shipment_ids)) != len(shipment_ids):
        raise ValueError("Duplicate shipment selection.")

    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    with SessionLocal.begin() as db:

        vehicle = db.get(Vehicle, vehicle_id)
        driver = db.get(Driver, driver_id)

        if not vehicle or vehicle.status != "Available":
            raise ValueError("Vehicle is unavailable.")

        if not driver or driver.status != "Active":
            raise ValueError("Driver is unavailable.")

        active_trip_statuses = ["Planned", "In Progress"]

        existing_vehicle_trip = db.scalar(
            select(Trip).where(
                Trip.vehicle_id == vehicle_id,
                Trip.status.in_(active_trip_statuses)
            )
        )

        existing_driver_trip = db.scalar(
            select(Trip).where(
                Trip.driver_id == driver_id,
                Trip.status.in_(active_trip_statuses)
            )
        )

        if existing_vehicle_trip:
            raise ValueError("Vehicle already has an active trip.")

        if existing_driver_trip:
            raise ValueError("Driver already has an active trip.")

        shipments = db.scalars(
            select(Shipment).where(
                Shipment.id.in_(shipment_ids)
            )
        ).all()

        if len(shipments) != len(shipment_ids):
            raise ValueError("One or more shipments do not exist.")

        for shipment in shipments:
            if shipment.status not in (
                "Confirmed", "Booking Created"
            ):
                raise ValueError(
                    f"{shipment.shipment_number} "
                    "is not ready for dispatch."
                )

            if shipment.vehicle_id or shipment.driver_id:
                raise ValueError(
                    f"{shipment.shipment_number} "
                    "already has an assignment."
                )

            if shipment.weight_kg <= 0:
                raise ValueError("Shipment weight must be positive.")

        total_weight = sum(s.weight_kg for s in shipments)

        if total_weight > vehicle.capacity_kg:
            raise ValueError("Vehicle capacity exceeded.")

        trip_number = (
            f"TRP-{__import__('uuid').uuid4().hex[:10].upper()}"
        )

        trip = Trip(
            trip_number=trip_number,
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            start_location=start_location.strip(),
            end_location=end_location.strip(),
            planned_start=planned_start,
            distance_km=distance_km,
            status="Planned"
        )

        db.add(trip)
        db.flush()

        for shipment in shipments:
            db.add(TripShipment(
                trip_id=trip.id,
                shipment_id=shipment.id
            ))

            shipment.vehicle_id = vehicle_id
            shipment.driver_id = driver_id
            shipment.status = "Confirmed"

        vehicle.status = "On Trip"

        db.add(AuditLog(
            username=username,
            action="Trip Created",
            details=trip_number
        ))

    return trip_number
