
import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import select, func
from database.connection import SessionLocal, initialize_database
from database.models import (
    User, Customer, Vehicle, Shipment, ShipmentEvent, AuditLog
)
from auth.security import hash_password, verify_password
from modules.operations import drivers_page, trip_page
st.set_page_config(
    page_title="LogiTrack ERP",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)
from modules.tracking_warehouse import (
    tracking_page,
    warehouse_page
)
initialize_database()

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem;}
    [data-testid="stMetric"] {
        background: #f0f4f8;
        padding: 16px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


def get_user_count():
    with SessionLocal() as db:
        return db.scalar(select(func.count(User.id))) or 0


def authenticate(username, password):
    with SessionLocal() as db:
        user = db.scalar(
            select(User).where(User.username == username)
        )
        if user and user.active and verify_password(
            password, user.password_hash
        ):
            return {
                "username": user.username,
                "role": user.role
            }
    return None


def login_screen():
    st.title("🚚 LogiTrack")
    st.caption("Logistics ERP & Management System")

    if get_user_count() == 0:
        st.subheader("Initial Administrator Setup")
        st.info("Create your first administrator account.")

        with st.form("setup_form"):
            username = st.text_input("Administrator username")
            password = st.text_input(
                "Password", type="password"
            )
            confirm = st.text_input(
                "Confirm password", type="password"
            )
            submitted = st.form_submit_button(
                "Create Administrator",
                use_container_width=True
            )

            if submitted:
                if not username.strip():
                    st.error("Username is required.")
                elif len(password) < 12:
                    st.error(
                        "Use a password with at least 12 characters."
                    )
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    with SessionLocal() as db:
                        db.add(User(
                            username=username.strip(),
                            password_hash=hash_password(password),
                            role="admin"
                        ))
                        db.commit()
                    st.success(
                        "Administrator created. Please log in."
                    )
                    st.rerun()
        return

    st.subheader("Sign in")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input(
            "Password", type="password"
        )
        submitted = st.form_submit_button(
            "Login", use_container_width=True
        )

        if submitted:
            user = authenticate(username.strip(), password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Invalid username or password.")


def dashboard():
    st.title("Executive Dashboard")
    st.caption("Company-wide logistics performance")

    with SessionLocal() as db:
        shipments = db.scalar(
            select(func.count(Shipment.id)
            )
        ) or 0

        delivered = db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.status == "Delivered"
            )
        ) or 0

        transit = db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.status == "In Transit"
            )
        ) or 0

        customers = db.scalar(
            select(func.count(Customer.id))
        ) or 0

        vehicles = db.scalar(
            select(func.count(Vehicle.id))
        ) or 0

        revenue = db.scalar(
            select(func.coalesce(
                func.sum(Shipment.freight_amount), 0
            )).where(Shipment.status != "Cancelled")
        ) or 0

        shipment_data = db.execute(
            select(Shipment.status, func.count(Shipment.id))
            .group_by(Shipment.status)
        ).all()

        recent = db.scalars(
            select(Shipment).order_by(
                Shipment.id.desc()
            ).limit(10)
        ).all()

    a, b, c = st.columns(3)
    a.metric("Total Shipments", shipments)
    b.metric("Delivered", delivered)
    c.metric("In Transit", transit)

    d, e, f = st.columns(3)
    d.metric("Customers", customers)
    e.metric("Vehicles", vehicles)
    f.metric("Freight Revenue", f"₹{revenue:,.2f}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Shipment Status")
        if shipment_data:
            chart = pd.DataFrame(
                shipment_data,
                columns=["Status", "Count"]
            )
            fig = px.pie(
                chart,
                names="Status",
                values="Count",
                hole=0.5
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No shipment records available yet.")

    with right:
        st.subheader("Delivery Overview")
        st.metric(
            "Delivery Completion",
            f"{delivered / shipments * 100:.1f}%"
            if shipments else "0%"
        )
        st.caption("Based on all recorded shipments.")

    st.subheader("Recent Shipments")

    if recent:
        st.dataframe(
            [{
                "Shipment ID": x.shipment_number,
                "Origin": x.origin,
                "Destination": x.destination,
                "Status": x.status,
                "Freight": x.freight_amount
            } for x in recent],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Create your first shipment to see activity.")


def customers_page():
    st.title("Customer Management")

    with st.form("customer_form"):
        name = st.text_input("Customer name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_area("Address")
        gst = st.text_input("GSTIN")
        submit = st.form_submit_button("Add Customer")

        if submit:
            if not name.strip():
                st.error("Customer name is required.")
            else:
                with SessionLocal() as db:
                    db.add(Customer(
                        name=name.strip(),
                        phone=phone.strip(),
                        email=email.strip(),
                        address=address.strip(),
                        gst_number=gst.strip()
                    ))
                    db.commit()
                st.success("Customer added successfully.")
                st.rerun()

    with SessionLocal() as db:
        records = db.scalars(
            select(Customer).order_by(Customer.id.desc())
        ).all()

    st.subheader("Customer Directory")
    st.dataframe([{
        "ID": x.id,
        "Name": x.name,
        "Phone": x.phone,
        "Email": x.email,
        "GSTIN": x.gst_number
    } for x in records], use_container_width=True)


def fleet_page():
    st.title("Fleet Management")

    with st.form("vehicle_form"):
        reg = st.text_input("Registration number")
        vehicle_type = st.selectbox(
            "Vehicle type",
            ["Truck", "Mini Truck", "Trailer", "Van",
             "Container", "Pickup", "Other"]
        )
        capacity = st.number_input(
            "Capacity (kg)", min_value=0.0, step=100.0
        )
        expiry = st.date_input("Insurance expiry")
        submit = st.form_submit_button("Register Vehicle")

        if submit:
            if not reg.strip():
                st.error("Registration number is required.")
            else:
                with SessionLocal() as db:
                    exists = db.scalar(
                        select(Vehicle).where(
                            Vehicle.registration_number ==
                            reg.strip().upper()
                        )
                    )
                    if exists:
                        st.error("This vehicle already exists.")
                    else:
                        db.add(Vehicle(
                            registration_number=reg.strip().upper(),
                            vehicle_type=vehicle_type,
                            capacity_kg=capacity,
                            insurance_expiry=expiry.isoformat()
                        ))
                        db.commit()
                        st.success("Vehicle registered.")
                        st.rerun()

    with SessionLocal() as db:
        records = db.scalars(
            select(Vehicle).order_by(Vehicle.id.desc())
        ).all()

    st.subheader("Vehicle Register")
    st.dataframe([{
        "ID": x.id,
        "Registration": x.registration_number,
        "Type": x.vehicle_type,
        "Capacity (kg)": x.capacity_kg,
        "Status": x.status,
        "Insurance Expiry": x.insurance_expiry
    } for x in records], use_container_width=True)


def shipments_page():
    st.title("Shipment Management")

    with SessionLocal() as db:
        customers = db.scalars(
            select(Customer).order_by(Customer.name)
        ).all()

    if not customers:
        st.warning("Please register a customer first.")
        return

    customer_options = {
        f"{c.name} (ID: {c.id})": c.id for c in customers
    }

    with st.form("shipment_form"):
        customer_label = st.selectbox(
            "Customer", list(customer_options)
        )
        origin = st.text_input("Pickup location")
        destination = st.text_input("Delivery location")
        weight = st.number_input(
            "Weight (kg)", min_value=0.0, step=1.0
        )
        freight = st.number_input(
            "Freight amount (₹)", min_value=0.0, step=100.0
        )
        expected = st.date_input("Expected delivery date")

        submit = st.form_submit_button("Create Shipment")

        if submit:
            if not origin.strip() or not destination.strip():
                st.error("Origin and destination are required.")
            elif weight <= 0:
                st.error("Weight must be greater than zero.")
            else:
                import uuid
                shipment_no = "LGT-" + uuid.uuid4().hex[:10].upper()

                with SessionLocal() as db:
                    shipment = Shipment(
                        shipment_number=shipment_no,
                        customer_id=customer_options[customer_label],
                        origin=origin.strip(),
                        destination=destination.strip(),
                        weight_kg=weight,
                        freight_amount=freight,
                        expected_delivery=expected.isoformat()
                    )
                    db.add(shipment)
                    db.flush()

                    db.add(ShipmentEvent(
                        shipment_id=shipment.id,
                        status="Booking Created",
                        location=origin.strip(),
                        remarks="Shipment registered"
                    ))

                    db.add(AuditLog(
                        username=st.session_state["user"]["username"],
                        action="Create Shipment",
                        details=shipment_no
                    ))
                    db.commit()

                st.success(f"Shipment {shipment_no} created.")
                st.rerun()

    with SessionLocal() as db:
        records = db.scalars(
            select(Shipment).order_by(Shipment.id.desc())
        ).all()

    st.subheader("Shipment Register")
    st.dataframe([{
        "Shipment ID": x.shipment_number,
        "Origin": x.origin,
        "Destination": x.destination,
        "Weight": x.weight_kg,
        "Freight": x.freight_amount,
        "Status": x.status
    } for x in records], use_container_width=True)


def main():
    if "user" not in st.session_state:
        login_screen()
        return

    user = st.session_state["user"]

    with st.sidebar:
        st.title("🚚 LogiTrack")
        st.caption("Logistics ERP")
        st.write(f"User: **{user['username']}**")
        st.caption(f"Role: {user['role']}")

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Shipments",
                "Customers",
                "Fleet",
                "Tracking",
                "Drivers",
                "Routes & Trips",
                "Warehouse",
                "Billing",
                "Finance",
                "Vendors",
                "Reports",
                "Notifications",
                "User Management",
                "Documents"
            ]
        )

        st.divider()

        if st.button("Logout", use_container_width=True):
            st.session_state.pop("user", None)
            st.rerun()

   
    pages = {
    "Dashboard": dashboard,
    "Shipments": shipments_page,
    "Customers": customers_page,
    "Fleet": fleet_page,
    "Drivers": drivers_page,
    "Routes & Trips": trip_page,
    "Tracking": tracking_page,
    "Warehouse": warehouse_page,
}

    if page in pages:
        pages[page]()
    else:
        st.title(page)
        st.info(
            "This module is included in the architecture "
            "and will be implemented in the next development phase."
        )


if __name__ == "__main__":
    main()
