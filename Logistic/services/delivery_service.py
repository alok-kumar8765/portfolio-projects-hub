
from datetime import datetime, timezone
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import (
    Shipment, ShipmentEvent, DeliveryProof, AuditLog
)
from auth.permissions import require_permission


def confirm_delivery(
    shipment_id,
    receiver_name,
    receiver_phone,
    remarks,
    username,
    role
):
    require_permission(role, "shipments.update")

    if not receiver_name.strip():
        raise ValueError("Receiver name is required.")

    now = datetime.now(timezone.utc).isoformat()

    with SessionLocal.begin() as db:
        shipment = db.get(Shipment, shipment_id)

        if not shipment:
            raise ValueError("Shipment not found.")

        if shipment.status != "Out for Delivery":
            raise ValueError(
                "Shipment must be Out for Delivery."
            )

        shipment.status = "Delivered"

        db.add(ShipmentEvent(
            shipment_id=shipment.id,
            status="Delivered",
            location=shipment.destination,
            remarks=remarks
        ))

        db.add(DeliveryProof(
            shipment_id=shipment.id,
            receiver_name=receiver_name.strip(),
            receiver_phone=receiver_phone.strip(),
            remarks=remarks,
            delivered_at=now
        ))

        db.add(AuditLog(
            username=username,
            action="Shipment Delivered",
            details=shipment.shipment_number
        ))

    return True
