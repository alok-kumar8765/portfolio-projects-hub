
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import Shipment, ShipmentEvent, AuditLog
from auth.permissions import require_permission

ALLOWED_TRANSITIONS = {
    "Booking Created": ["Confirmed", "Cancelled"],
    "Confirmed": ["Picked Up", "Cancelled"],
    "Picked Up": ["In Transit", "Delivery Failed"],
    "In Transit": [
        "At Destination Hub",
        "Delayed",
        "Delivery Failed"
    ],
    "At Destination Hub": ["Out for Delivery"],
    "Out for Delivery": ["Delivered", "Delivery Failed"],
    "Delayed": ["In Transit", "Cancelled"],
    "Delivery Failed": ["In Transit", "Returned"],
    "Returned": [],
    "Delivered": [],
    "Cancelled": []
}


def update_shipment_status(
    shipment_id,
    new_status,
    location,
    remarks,
    username,
    role
):
    require_permission(role, "shipments.update")

    with SessionLocal.begin() as db:
        shipment = db.scalar(
            select(Shipment)
            .where(Shipment.id == shipment_id)
            .with_for_update()
        )

        if shipment is None:
            raise ValueError("Shipment not found.")

        allowed = ALLOWED_TRANSITIONS.get(
            shipment.status, []
        )

        if new_status not in allowed:
            raise ValueError(
                f"Cannot move shipment from "
                f"{shipment.status} to {new_status}."
            )

        shipment.status = new_status

        db.add(ShipmentEvent(
            shipment_id=shipment.id,
            status=new_status,
            location=location,
            remarks=remarks
        ))

        db.add(AuditLog(
            username=username,
            action="Shipment Status Updated",
            details=(
                f"{shipment.shipment_number}: "
                f"{new_status} at {location}"
            )
        ))

    return True
