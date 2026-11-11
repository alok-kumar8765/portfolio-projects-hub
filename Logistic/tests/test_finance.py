
from decimal import Decimal
import pytest

from services.finance_service import money
from services.gst_service import calculate_gst


def test_money_rounding():
    assert money("100.456") == Decimal("100.46")


def test_intra_state_gst():
    result = calculate_gst(
        "1000", "18", "INTRA_STATE"
    )

    assert result["cgst"] == Decimal("90.00")
    assert result["sgst"] == Decimal("90.00")
    assert result["igst"] == Decimal("0.00")
    assert result["grand_total"] == Decimal("1180.00")


def test_inter_state_gst():
    result = calculate_gst(
        "1000", "18", "INTER_STATE"
    )

    assert result["igst"] == Decimal("180.00")
    assert result["cgst"] == Decimal("0.00")
    assert result["sgst"] == Decimal("0.00")


def test_invalid_gst_rate():
    with pytest.raises(ValueError):
        calculate_gst("1000", "150", "INTRA_STATE")


def test_invalid_supply_type():
    with pytest.raises(ValueError):
        calculate_gst("1000", "18", "UNKNOWN")


def test_negative_taxable_amount():
    with pytest.raises(ValueError):
        calculate_gst("-100", "18", "INTRA_STATE")
