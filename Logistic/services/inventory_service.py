
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import (
    Warehouse, Product, Inventory, StockMovement, AuditLog
)
from auth.permissions import require_permission


import uuid

from database.models import WarehouseTransfer


def transfer_stock(
    source_id,
    destination_id,
    product_id,
    quantity,
    username,
    role
):
    require_permission(role, "inventory.manage")

    if source_id == destination_id:
        raise ValueError("Select two different warehouses.")

    if quantity <= 0:
        raise ValueError("Quantity must be positive.")

    with SessionLocal.begin() as db:
        source = db.get(Warehouse, source_id)
        destination = db.get(Warehouse, destination_id)

        if not source or not destination:
            raise ValueError("Warehouse not found.")

        if not source.active or not destination.active:
            raise ValueError("Warehouse is inactive.")

        product = db.get(Product, product_id)

        if not product or not product.active:
            raise ValueError("Product is unavailable.")

        source_stock = db.scalar(
            select(Inventory).where(
                Inventory.warehouse_id == source_id,
                Inventory.product_id == product_id
            )
        )

        if not source_stock or source_stock.quantity < quantity:
            raise ValueError("Insufficient source stock.")

        destination_stock = db.scalar(
            select(Inventory).where(
                Inventory.warehouse_id == destination_id,
                Inventory.product_id == product_id
            )
        )

        if destination_stock is None:
            destination_stock = Inventory(
                warehouse_id=destination_id,
                product_id=product_id,
                quantity=0
            )
            db.add(destination_stock)
            db.flush()

        source_stock.quantity -= quantity
        destination_stock.quantity += quantity

        transfer_number = (
            "WHT-" + uuid.uuid4().hex[:10].upper()
        )

        db.add(WarehouseTransfer(
            transfer_number=transfer_number,
            source_warehouse_id=source_id,
            destination_warehouse_id=destination_id,
            product_id=product_id,
            quantity=quantity,
            status="Completed"
        ))

        db.add(StockMovement(
            warehouse_id=source_id,
            product_id=product_id,
            movement_type="TRANSFER_OUT",
            quantity=quantity,
            reference=transfer_number
        ))

        db.add(StockMovement(
            warehouse_id=destination_id,
            product_id=product_id,
            movement_type="TRANSFER_IN",
            quantity=quantity,
            reference=transfer_number
        ))

        db.add(AuditLog(
            username=username,
            action="Warehouse Transfer",
            details=transfer_number
        ))

    return transfer_number

def create_warehouse(
    code, name, address, city, manager, phone, capacity, username, role
):
    require_permission(role, "warehouse.manage")

    if not code.strip() or not name.strip():
        raise ValueError("Warehouse code and name are required.")

    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    with SessionLocal.begin() as db:
        existing = db.scalar(
            select(Warehouse).where(
                Warehouse.warehouse_code == code.strip().upper()
            )
        )

        if existing:
            raise ValueError("Warehouse code already exists.")

        warehouse = Warehouse(
            warehouse_code=code.strip().upper(),
            name=name.strip(),
            address=address.strip(),
            city=city.strip(),
            manager_name=manager.strip(),
            phone=phone.strip(),
            capacity_kg=capacity
        )

        db.add(warehouse)
        db.flush()

        db.add(AuditLog(
            username=username,
            action="Warehouse Created",
            details=warehouse.warehouse_code
        ))

        return warehouse.id


def create_product(
    sku, name, category, unit, weight, description, username, role
):
    require_permission(role, "inventory.manage")

    if not sku.strip() or not name.strip():
        raise ValueError("SKU and product name are required.")

    if weight < 0:
        raise ValueError("Product weight cannot be negative.")

    with SessionLocal.begin() as db:
        existing = db.scalar(
            select(Product).where(
                Product.sku == sku.strip().upper()
            )
        )

        if existing:
            raise ValueError("SKU already exists.")

        product = Product(
            sku=sku.strip().upper(),
            name=name.strip(),
            category=category,
            unit=unit,
            weight_kg=weight,
            description=description
        )

        db.add(product)
        db.flush()

        db.add(AuditLog(
            username=username,
            action="Product Created",
            details=product.sku
        ))

        return product.id


def receive_stock(
    warehouse_id,
    product_id,
    quantity,
    reference,
    remarks,
    username,
    role
):
    require_permission(role, "inventory.manage")

    if quantity <= 0:
        raise ValueError("Quantity must be positive.")

    with SessionLocal.begin() as db:
        warehouse = db.get(Warehouse, warehouse_id)
        product = db.get(Product, product_id)

        if not warehouse or not warehouse.active:
            raise ValueError("Warehouse unavailable.")

        if not product or not product.active:
            raise ValueError("Product unavailable.")

        inventory = db.scalar(
            select(Inventory).where(
                Inventory.warehouse_id == warehouse_id,
                Inventory.product_id == product_id
            )
        )

        if inventory is None:
            inventory = Inventory(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=0
            )
            db.add(inventory)
            db.flush()

        inventory.quantity += quantity

        db.add(StockMovement(
            warehouse_id=warehouse_id,
            product_id=product_id,
            movement_type="IN",
            quantity=quantity,
            reference=reference,
            remarks=remarks
        ))

        db.add(AuditLog(
            username=username,
            action="Stock Received",
            details=f"{product.sku}: {quantity}"
        ))


def dispatch_stock(
    warehouse_id,
    product_id,
    quantity,
    reference,
    remarks,
    username,
    role
):
    require_permission(role, "inventory.manage")

    if quantity <= 0:
        raise ValueError("Quantity must be positive.")

    with SessionLocal.begin() as db:
        inventory = db.scalar(
            select(Inventory).where(
                Inventory.warehouse_id == warehouse_id,
                Inventory.product_id == product_id
            )
        )

        if inventory is None:
            raise ValueError("Inventory record not found.")

        if inventory.quantity < quantity:
            raise ValueError("Insufficient stock.")

        inventory.quantity -= quantity

        db.add(StockMovement(
            warehouse_id=warehouse_id,
            product_id=product_id,
            movement_type="OUT",
            quantity=quantity,
            reference=reference,
            remarks=remarks
        ))

        db.add(AuditLog(
            username=username,
            action="Stock Dispatched",
            details=f"Product ID {product_id}: {quantity}"
        ))
