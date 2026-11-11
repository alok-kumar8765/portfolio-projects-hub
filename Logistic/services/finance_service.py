
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from sqlalchemy import select, func

from database.connection import SessionLocal
from database.models import (
    Invoice, InvoiceItem, Payment, AuditLog, Customer
)
from auth.permissions import require_permission


CENT = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def create_invoice(
    customer_id,
    items,
    cgst,
    sgst,
    igst,
    username,
    role,
    shipment_id=None,
    trip_id=None,
    notes=""
):
    require_permission(role, "finance.manage")

    if not items:
        raise ValueError("Invoice requires at least one item.")

    cgst, sgst, igst = money(cgst), money(sgst), money(igst)

    if min(cgst, sgst, igst) < 0:
        raise ValueError("Tax cannot be negative.")

    with SessionLocal.begin() as db:
        customer = db.get(Customer, customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        subtotal = Decimal("0.00")
        prepared_items = []

        for item in items:
            quantity = Decimal(str(item["quantity"]))
            price = money(item["unit_price"])

            if quantity <= 0 or price < 0:
                raise ValueError("Invalid invoice item.")

            amount = money(quantity * price)
            subtotal += amount

            prepared_items.append({
                "description": item["description"],
                "quantity": quantity,
                "unit_price": price,
                "amount": amount,
                "gst_rate": Decimal(str(
                    item.get("gst_rate", 0)
                ))
            })

        subtotal = money(subtotal)
        total = money(subtotal + cgst + sgst + igst)

        invoice_number = (
            "INV-" + uuid4().hex[:12].upper()
        )

        invoice = Invoice(
            invoice_number=invoice_number,
            customer_id=customer_id,
            shipment_id=shipment_id,
            trip_id=trip_id,
            subtotal=subtotal,
            cgst=cgst,
            sgst=sgst,
            igst=igst,
            total=total,
            status="Draft",
            notes=notes
        )

        db.add(invoice)
        db.flush()

        for item in prepared_items:
            db.add(InvoiceItem(
                invoice_id=invoice.id,
                **item
            ))

        db.add(AuditLog(
            username=username,
            action="Invoice Created",
            details=invoice_number
        ))

        return invoice_number


def record_customer_payment(
    invoice_id,
    amount,
    payment_method,
    username,
    role,
    reference_number=""
):
    require_permission(role, "finance.manage")

    amount = money(amount)

    if amount <= 0:
        raise ValueError("Payment must be positive.")

    with SessionLocal.begin() as db:
        invoice = db.get(Invoice, invoice_id)

        if not invoice:
            raise ValueError("Invoice not found.")

        if invoice.status in ("Cancelled", "Draft"):
            raise ValueError(
                "Payment cannot be recorded for this invoice."
            )

        if invoice.status == "Paid":
            raise ValueError("Invoice is already paid.")

        received = db.scalar(
            select(func.coalesce(func.sum(Payment.amount), 0))
            .where(Payment.invoice_id == invoice_id)
        )

        balance = money(
            Decimal(str(invoice.total)) - Decimal(str(received))
        )

        if amount > balance:
            raise ValueError(
                f"Payment exceeds outstanding balance: {balance}"
            )

        receipt = "REC-" + uuid4().hex[:12].upper()

        db.add(Payment(
            receipt_number=receipt,
            invoice_id=invoice_id,
            amount=amount,
            payment_method=payment_method,
            reference_number=reference_number
        ))

        if amount == balance:
            invoice.status = "Paid"
        else:
            invoice.status = "Partially Paid"

        db.add(AuditLog(
            username=username,
            action="Customer Payment",
            details=f"{receipt}: {amount}"
        ))

        return receipt
