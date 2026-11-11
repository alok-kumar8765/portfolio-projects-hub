
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def calculate_gst(
    taxable_amount,
    gst_rate,
    supply_type
):
    taxable = Decimal(str(taxable_amount))
    rate = Decimal(str(gst_rate))

    if taxable < 0 or rate < 0 or rate > 100:
        raise ValueError("Invalid taxable amount or GST rate.")

    tax = (taxable * rate / Decimal("100")).quantize(
        CENT, rounding=ROUND_HALF_UP
    )

    if supply_type == "INTRA_STATE":
        cgst = (tax / 2).quantize(
            CENT, rounding=ROUND_HALF_UP
        )
        sgst = tax - cgst
        igst = Decimal("0.00")

    elif supply_type == "INTER_STATE":
        cgst = Decimal("0.00")
        sgst = Decimal("0.00")
        igst = tax

    else:
        raise ValueError("Invalid supply type.")

    return {
        "taxable_amount": taxable.quantize(CENT),
        "gst_rate": rate,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "total_tax": tax,
        "grand_total": taxable + tax
    }
