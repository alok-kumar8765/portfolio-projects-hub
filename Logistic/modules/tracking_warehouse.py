
import streamlit as st
import pandas as pd

from sqlalchemy import select

from database.connection import SessionLocal
from database.models import (
    Shipment, Warehouse, Product, Inventory,
    StockMovement, ShipmentEvent
)

from services.tracking_service import (
    update_tracking, get_tracking_history
)

from services.inventory_service import (
    create_warehouse, create_product,
    receive_stock, dispatch_stock, transfer_stock
)

from auth.permissions import require_permission

def tracking_page():
    user = st.session_state["user"]

    try:
        require_permission(
            user["role"],
            "tracking.view"
        )
    except PermissionError:
        st.error("You do not have permission to access tracking.")
        st.stop()

    st.title("Shipment Tracking")
    st.caption("Shipment status and journey history")

    with SessionLocal() as db:
        shipments = db.scalars(
            select(Shipment).order_by(Shipment.id.desc())
        ).all()

    if not shipments:
        st.info("No shipments available.")
        return

    options = {
        f"{s.shipment_number} | {s.status}": s.id
        for s in shipments
    }

    selected = st.selectbox(
        "Select shipment",
        list(options)
    )

    shipment_id = options[selected]

    try:
        history = get_tracking_history(shipment_id)

        st.subheader("Shipment Details")

        c1, c2, c3 = st.columns(3)
        c1.metric("Shipment", history["shipment"]["number"])
        c2.metric("Current Status", history["shipment"]["status"])
        c3.metric("Destination", history["shipment"]["destination"])

        st.subheader("Journey Timeline")

        if history["events"]:
            for event in reversed(history["events"]):
                st.markdown(
                    f"**{event['status']}** — "
                    f"{event['location']}"
                )
                st.caption(
                    f"{event['date']} | {event['remarks']}"
                )
                if event["latitude"] is not None:
                    st.caption(
                        f"GPS: {event['latitude']}, "
                        f"{event['longitude']}"
                    )
        else:
            st.info("No tracking events recorded.")

    except ValueError as exc:
        st.error(str(exc))

    st.divider()
    st.subheader("Update Shipment Tracking")

    current = next(
        s for s in shipments if s.id == shipment_id
    )

    from services.shipment_service import ALLOWED_TRANSITIONS

    allowed = ALLOWED_TRANSITIONS.get(current.status, [])

    if not allowed:
        st.info("This shipment has no available status transitions.")
        return

    with st.form("tracking_update"):
        status = st.selectbox("New status", allowed)
        location = st.text_input("Current location")
        remarks = st.text_area("Remarks")

        use_gps = st.checkbox("Add GPS coordinates")

        latitude = None
        longitude = None

        if use_gps:
            latitude = st.number_input(
                "Latitude", min_value=-90.0, max_value=90.0,
                value=0.0, format="%.6f"
            )
            longitude = st.number_input(
                "Longitude", min_value=-180.0, max_value=180.0,
                value=0.0, format="%.6f"
            )

        submit = st.form_submit_button("Update Tracking")

        if submit:
            try:
                update_tracking(
                    shipment_id=shipment_id,
                    status=status,
                    location=location,
                    remarks=remarks,
                    username=user["username"],
                    role=user["role"],
                    latitude=latitude,
                    longitude=longitude
                )

                st.success("Shipment tracking updated.")
                st.rerun()

            except (ValueError, PermissionError) as exc:
                st.error(str(exc))


def warehouse_page():
    user = st.session_state["user"]

    st.title("Warehouse Management")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Warehouses",
        "Products",
        "Stock Operations",
        "Inventory Report"
    ])

    with tab1:
        st.subheader("Register Warehouse")

        with st.form("warehouse_form"):
            code = st.text_input("Warehouse code")
            name = st.text_input("Warehouse name")
            address = st.text_area("Address")
            city = st.text_input("City")
            manager = st.text_input("Warehouse manager")
            phone = st.text_input("Contact number")
            capacity = st.number_input(
                "Storage capacity (kg)",
                min_value=0.0
            )

            submit = st.form_submit_button("Add Warehouse")

            if submit:
                try:
                    create_warehouse(
                        code, name, address, city,
                        manager, phone, capacity,
                        user["username"], user["role"]
                    )
                    st.success("Warehouse created.")
                    st.rerun()
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))

        with SessionLocal() as db:
            warehouses = db.scalars(
                select(Warehouse)
            ).all()

        st.dataframe([{
            "Code": w.warehouse_code,
            "Name": w.name,
            "City": w.city,
            "Manager": w.manager_name,
            "Capacity": w.capacity_kg,
            "Active": w.active
        } for w in warehouses], use_container_width=True)

    with tab2:
        st.subheader("Register Product")

        with st.form("product_form"):
            sku = st.text_input("SKU / Product Code")
            name = st.text_input("Product name")
            category = st.text_input("Category")

            unit = st.selectbox(
                "Unit", ["Piece", "Box", "Carton", "Kg", "Pallet"]
            )

            weight = st.number_input(
                "Unit weight (kg)", min_value=0.0
            )

            description = st.text_area("Description")

            submit = st.form_submit_button("Add Product")

            if submit:
                try:
                    create_product(
                        sku, name, category, unit,
                        weight, description,
                        user["username"], user["role"]
                    )
                    st.success("Product registered.")
                    st.rerun()
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))

        with SessionLocal() as db:
            products = db.scalars(
                select(Product)
            ).all()

        st.dataframe([{
            "SKU": p.sku,
            "Name": p.name,
            "Category": p.category,
            "Unit": p.unit,
            "Weight": p.weight_kg
        } for p in products], use_container_width=True)

    with tab3:
        with SessionLocal() as db:
            warehouses = db.scalars(
                select(Warehouse).where(Warehouse.active == True)
            ).all()

            products = db.scalars(
                select(Product).where(Product.active == True)
            ).all()

        if not warehouses or not products:
            st.warning(
                "Create at least one warehouse and one product first."
            )
        else:
            warehouse_map = {
                w.warehouse_code + " - " + w.name: w.id
                for w in warehouses
            }

            product_map = {
                p.sku + " - " + p.name: p.id
                for p in products
            }

            operation = st.radio(
                "Operation",
                ["Receive Stock", "Dispatch Stock", "Transfer Stock"],
                horizontal=True
            )

            with st.form("stock_operation"):
                product_label = st.selectbox(
                    "Product", list(product_map)
                )

                if operation == "Transfer Stock":
                    source_label = st.selectbox(
                        "Source warehouse",
                        list(warehouse_map)
                    )

                    destination_label = st.selectbox(
                        "Destination warehouse",
                        list(warehouse_map)
                    )
                else:
                    warehouse_label = st.selectbox(
                        "Warehouse", list(warehouse_map)
                    )

                quantity = st.number_input(
                    "Quantity",
                    min_value=0.01,
                    step=1.0
                )

                reference = st.text_input("Reference number")
                remarks = st.text_area("Remarks")

                submit = st.form_submit_button("Process Operation")

                if submit:
                    try:
                        product_id = product_map[product_label]

                        if operation == "Receive Stock":
                            receive_stock(
                                warehouse_map[warehouse_label],
                                product_id, quantity, reference,
                                remarks, user["username"], user["role"]
                            )

                        elif operation == "Dispatch Stock":
                            dispatch_stock(
                                warehouse_map[warehouse_label],
                                product_id, quantity, reference,
                                remarks, user["username"], user["role"]
                            )

                        else:
                            transfer_number = transfer_stock(
                                warehouse_map[source_label],
                                warehouse_map[destination_label],
                                product_id, quantity,
                                user["username"], user["role"]
                            )
                            st.success(
                                f"Transfer created: {transfer_number}"
                            )

                        if operation != "Transfer Stock":
                            st.success("Stock operation completed.")

                        st.rerun()

                    except (ValueError, PermissionError) as exc:
                        st.error(str(exc))

    with tab4:
        st.subheader("Current Inventory")

        with SessionLocal() as db:
            rows = db.execute(
                select(
                    Warehouse.warehouse_code,
                    Warehouse.name,
                    Product.sku,
                    Product.name,
                    Inventory.quantity,
                    Inventory.reorder_level
                )
                .join(
                    Inventory,
                    Inventory.warehouse_id == Warehouse.id
                )
                .join(
                    Product,
                    Inventory.product_id == Product.id
                )
            ).all()

        inventory_data = [{
            "Warehouse Code": r[0],
            "Warehouse": r[1],
            "SKU": r[2],
            "Product": r[3],
            "Quantity": r[4],
            "Reorder Level": r[5],
            "Stock Alert": "LOW" if r[4] <= r[5] else "OK"
        } for r in rows]

        if inventory_data:
            df = pd.DataFrame(inventory_data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            low_stock = df[df["Stock Alert"] == "LOW"]
            if not low_stock.empty:
                st.warning(
                    f"{len(low_stock)} inventory records "
                    "are at or below reorder level."
                )

            st.download_button(
                "Download Inventory CSV",
                df.to_csv(index=False).encode("utf-8"),
                "inventory_report.csv",
                "text/csv"
            )
        else:
            st.info("No inventory records found.")
