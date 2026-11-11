
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Numeric,
    UniqueConstraint,
    CheckConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


# =====================================================
# USER MANAGEMENT
# =====================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(300))
    role: Mapped[str] = mapped_column(String(40), default="operator")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


# =====================================================
# CUSTOMER MANAGEMENT
# =====================================================

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30), default="")
    email: Mapped[str] = mapped_column(String(150), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    gst_number: Mapped[str] = mapped_column(String(20), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


# =====================================================
# VEHICLE MANAGEMENT
# =====================================================

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(80))
    capacity_kg: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(40), default="Available")
    insurance_expiry: Mapped[str] = mapped_column(String(20), default="")


# =====================================================
# DRIVER MANAGEMENT
# =====================================================

class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30))
    licence_number: Mapped[str] = mapped_column(String(60), unique=True)
    licence_expiry: Mapped[str] = mapped_column(String(20), default="")
    status: Mapped[str] = mapped_column(String(40), default="Active")


# =====================================================
# SHIPMENT MANAGEMENT
# =====================================================

class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    origin: Mapped[str] = mapped_column(String(250))
    destination: Mapped[str] = mapped_column(String(250))
    weight_kg: Mapped[float] = mapped_column(Float, default=0)
    freight_amount: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(50), default="Booking Created")
    booking_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expected_delivery: Mapped[str] = mapped_column(String(20), default="")
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id"), nullable=True)
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("drivers.id"), nullable=True)


class ShipmentEvent(Base):
    __tablename__ = "shipment_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipments.id"))
    status: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(250), default="")
    remarks: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


# =====================================================
# AUDIT LOG
# =====================================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80))
    action: Mapped[str] = mapped_column(String(150))
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


# =====================================================
# TRIP MANAGEMENT
# =====================================================

class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    start_location: Mapped[str] = mapped_column(String(250))
    end_location: Mapped[str] = mapped_column(String(250))
    planned_start: Mapped[str] = mapped_column(String(30))
    actual_start: Mapped[str] = mapped_column(String(30), default="")
    actual_end: Mapped[str] = mapped_column(String(30), default="")
    distance_km: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(40), default="Planned")
    remarks: Mapped[str] = mapped_column(Text, default="")


class TripShipment(Base):
    __tablename__ = "trip_shipments"

    __table_args__ = (
        UniqueConstraint("trip_id", "shipment_id", name="uq_trip_shipment"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipments.id"))


class TripExpense(Base):
    __tablename__ = "trip_expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    category: Mapped[str] = mapped_column(String(80))
    amount: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text, default="")
    expense_date: Mapped[str] = mapped_column(String(30))


# =====================================================
# VEHICLE MAINTENANCE
# =====================================================

class VehicleMaintenance(Base):
    __tablename__ = "vehicle_maintenance"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    maintenance_type: Mapped[str] = mapped_column(String(100))
    maintenance_date: Mapped[str] = mapped_column(String(30))
    cost: Mapped[float] = mapped_column(Float, default=0)
    remarks: Mapped[str] = mapped_column(Text, default="")


# =====================================================
# DELIVERY PROOF
# =====================================================

class DeliveryProof(Base):
    __tablename__ = "delivery_proofs"

    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipments.id"))
    receiver_name: Mapped[str] = mapped_column(String(150))
    receiver_phone: Mapped[str] = mapped_column(String(30), default="")
    document_path: Mapped[str] = mapped_column(String(500), default="")
    remarks: Mapped[str] = mapped_column(Text, default="")
    delivered_at: Mapped[str] = mapped_column(String(30))


# =====================================================
# WAREHOUSE MANAGEMENT
# =====================================================

class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    manager_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(30), default="")
    capacity_kg: Mapped[float] = mapped_column(Float, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(30), default="Piece")
    weight_kg: Mapped[float] = mapped_column(Float, default=0)
    description: Mapped[str] = mapped_column(Text, default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint("warehouse_id", "product_id", name="uq_warehouse_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[float] = mapped_column(Float, default=0)
    reorder_level: Mapped[float] = mapped_column(Float, default=0)


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    movement_type: Mapped[str] = mapped_column(String(40))
    quantity: Mapped[float] = mapped_column(Float)
    reference: Mapped[str] = mapped_column(String(100), default="")
    remarks: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class WarehouseTransfer(Base):
    __tablename__ = "warehouse_transfers"

    id: Mapped[int] = mapped_column(primary_key=True)
    transfer_number: Mapped[str] = mapped_column(String(50), unique=True)
    source_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    destination_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(40), default="Completed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


# =====================================================
# FINANCIAL MANAGEMENT
# =====================================================

class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    gstin: Mapped[str] = mapped_column(String(15), default="")
    phone: Mapped[str] = mapped_column(String(30), default="")
    email: Mapped[str] = mapped_column(String(150), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Invoice(Base):
    __tablename__ = "invoices"

    __table_args__ = (
        CheckConstraint(
            "subtotal >= 0 AND cgst >= 0 AND sgst >= 0 "
            "AND igst >= 0 AND total >= 0",
            name="ck_invoice_nonnegative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    shipment_id: Mapped[int | None] = mapped_column(ForeignKey("shipments.id"), nullable=True)
    trip_id: Mapped[int | None] = mapped_column(ForeignKey("trips.id"), nullable=True)

    invoice_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"))
    cgst: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"))
    sgst: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"))
    igst: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"))
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"))

    status: Mapped[str] = mapped_column(String(30), default="Draft")
    notes: Mapped[str] = mapped_column(Text, default="")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    description: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    gst_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"))


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_number: Mapped[str] = mapped_column(String(50), unique=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    payment_method: Mapped[str] = mapped_column(String(40))
    reference_number: Mapped[str] = mapped_column(String(100), default="")
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    notes: Mapped[str] = mapped_column(Text, default="")


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    expense_number: Mapped[str] = mapped_column(String(50), unique=True)
    trip_id: Mapped[int | None] = mapped_column(ForeignKey("trips.id"), nullable=True)
    vendor_id: Mapped[int | None] = mapped_column(ForeignKey("vendors.id"), nullable=True)
    category: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    expense_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    payment_status: Mapped[str] = mapped_column(String(30), default="Unpaid")


class VendorBill(Base):
    __tablename__ = "vendor_bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    bill_number: Mapped[str] = mapped_column(String(50), unique=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))
    bill_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(String(30), default="Unpaid")
    description: Mapped[str] = mapped_column(Text, default="")


class VendorPayment(Base):
    __tablename__ = "vendor_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_number: Mapped[str] = mapped_column(String(50), unique=True)
    bill_id: Mapped[int] = mapped_column(ForeignKey("vendor_bills.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    payment_method: Mapped[str] = mapped_column(String(40))
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    reference_number: Mapped[str] = mapped_column(String(100), default="")
