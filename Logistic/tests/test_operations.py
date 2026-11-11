
from auth.permissions import has_permission
from services.shipment_service import ALLOWED_TRANSITIONS


def test_trip_roles():
    assert has_permission("admin", "routes.manage")
    assert has_permission(
        "operations_manager", "routes.manage"
    )
    assert not has_permission("customer", "routes.manage")


def test_shipment_dispatch_workflow():
    assert (
        "In Transit" in ALLOWED_TRANSITIONS["Picked Up"]
    )


def test_shipment_delivery_workflow():
    assert (
        "Delivered" in ALLOWED_TRANSITIONS["Out for Delivery"]
    )


def test_return_workflow():
    assert (
        "Returned" in ALLOWED_TRANSITIONS["Delivery Failed"]
    )


def test_final_shipment_states():
    assert ALLOWED_TRANSITIONS["Delivered"] == []
    assert ALLOWED_TRANSITIONS["Cancelled"] == []
