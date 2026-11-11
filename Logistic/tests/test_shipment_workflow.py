
from services.shipment_service import ALLOWED_TRANSITIONS
from auth.permissions import has_permission


def test_booking_can_be_confirmed():
    assert (
        "Confirmed" in ALLOWED_TRANSITIONS["Booking Created"]
    )


def test_delivered_shipment_is_final():
    assert ALLOWED_TRANSITIONS["Delivered"] == []


def test_cancelled_shipment_is_final():
    assert ALLOWED_TRANSITIONS["Cancelled"] == []


def test_admin_has_all_permissions():
    assert has_permission("admin", "shipments.update")


def test_customer_cannot_manage_fleet():
    assert not has_permission("customer", "fleet.create")


def test_accountant_can_manage_billing():
    assert has_permission("accountant", "billing.manage")
