
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import Shipment, ShipmentEvent, AuditLog
from services.shipment_service import ALLOWED_TRANSITIONS
from auth.permissions import require_permission


def update_tracking(
    shipment_id,
    status,
    location,
    remarks,
    username,
    role,
    latitude=None,
    longitude=None
):
    require_permission(role, "shipments.update")

    if latitude is not None and not -90 <= latitude <= 90:
        raise ValueError("Invalid latitude.")

    if longitude is not None and not -180 <= longitude <= 180:
        raise ValueError("Invalid longitude.")

    if (latitude is None) != (longitude is None):
        raise ValueError("Both GPS coordinates are required.")

    with SessionLocal.begin() as db:
        shipment = db.get(Shipment, shipment_id)

        if not shipment:
            raise ValueError("Shipment not found.")

        allowed = ALLOWED_TRANSITIONS.get(
            shipment.status, []
        )

        if status not in allowed:
            raise ValueError(
                f"Invalid transition: {shipment.status} "
                f"to {status}"
            )

        shipment.status = status

        event = ShipmentEvent(
            shipment_id=shipment.id,
            status=status,
            location=location.strip(),
            remarks=remarks.strip(),
            latitude=latitude,
            longitude=longitude
        )

        db.add(event)

        db.add(AuditLog(
            username=username,
            action="Shipment Tracking Updated",
            details=f"{shipment.shipment_number}: {status}"
        ))

    return True


def get_tracking_history(shipment_id):
    with SessionLocal() as db:
        shipment = db.get(Shipment, shipment_id)

        if not shipment:
            raise ValueError("Shipment not found.")

        events = db.scalars(
            select(ShipmentEvent)
            .where(ShipmentEvent.shipment_id == shipment_id)
            .order_by(ShipmentEvent.id.asc())
        ).all()

        return {
            "shipment": {
                "number": shipment.shipment_number,
                "origin": shipment.origin,
                "destination": shipment.destination,
                "status": shipment.status
            },
            "events": [{
                "status": e.status,
                "location": e.location,
                "remarks": e.remarks,
                "latitude": e.latitude,
                "longitude": e.longitude,
                "date": e.created_at
            } for e in events]
        }
