
from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Driver, AuditLog
from auth.permissions import require_permission


def register_driver(
    name,
    phone,
    license_number,
    license_expiry,
    username,
    role
):
    require_permission(role, "drivers.manage")

    if not name.strip():
        raise ValueError("Driver name is required.")

    if not phone.strip():
        raise ValueError("Driver phone is required.")

    if not license_number.strip():
        raise ValueError("License number is required.")

    with SessionLocal.begin() as db:

        existing = db.scalar(
            select(Driver).where(
                Driver.license_number == license_number.strip()
            )
        )

        if existing:
            raise ValueError("License number already registered.")

        driver = Driver(
            name=name.strip(),
            phone=phone.strip(),
            license_number=license_number.strip(),
            license_expiry=license_expiry
        )

        db.add(driver)
        db.flush()

        db.add(AuditLog(
            username=username,
            action="Driver Registered",
            details=f"Driver: {driver.name}"
        ))

        return driver.id
