
import streamlit as st
import pandas as pd

from datetime import date

from sqlalchemy import select
from database.connection import SessionLocal
from database.models import (
    Driver, Vehicle, Shipment, Trip, TripShipment
)

from services.driver_service import register_driver
from services.assignment_service import create_trip
from services.trip_service import start_trip, complete_trip


def current_user():
    return st.session_state["user"]


def drivers_page():
    user = current_user()
    st.title("Driver Management")

    with st.expander("Register New Driver", expanded=True):
        with st.form("driver_registration"):
            name = st.text_input("Driver name")
            phone = st.text_input("Phone number")
            licence = st.text_input("Driving licence number")
            expiry = st.date_input("Licence expiry date")

            submitted = st.form_submit_button(
                "Register Driver"
            )

            if submitted:
                try:
                    driver_id = register_driver(
                        name,
                        phone,
                        licence,
                        expiry.isoformat(),
                        user["username"],
                        user["role"]
                    )
                    st.success(
                        f"Driver registered. ID: {driver_id}"
                    )
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))

    with SessionLocal() as db:
        drivers = db.scalars(
            select(Driver).order_by(Driver.id.desc())
        ).all()

    st.subheader("Driver Directory")

    st.dataframe([{
        "ID": d.id,
        "Name": d.name,
        "Phone": d.phone,
        "Licence": d.licence_number,
        "Expiry": d.licence_expiry,
        "Status": d.status
    } for d in drivers], use_container_width=True)


def trip_page():
    user = current_user()
    st.title("Route & Trip Management")

    with SessionLocal() as db:
        vehicles = db.scalars(
            select(Vehicle).where(
                Vehicle.status == "Available"
            )
        ).all()

        drivers = db.scalars(
            select(Driver).where(
                Driver.status == "Active"
            )
        ).all()

        shipments = db.scalars(
            select(Shipment).where(
                Shipment.status.in_([
                    "Booking Created", "Confirmed"
                ]),
                Shipment.vehicle_id.is_(None),
                Shipment.driver_id.is_(None)
            )
        ).all()

    st.subheader("Create Transport Trip")

    if not vehicles or not drivers or not shipments:
        st.info(
            "You need an available vehicle, active driver "
            "and unassigned shipments to create a trip."
        )
    else:
        vehicle_map = {
            f"{v.registration_number} ({v.capacity_kg} kg)": v.id
            for v in vehicles
        }

        driver_map = {
            f"{d.name} ({d.phone})": d.id
            for d in drivers
        }

        shipment_map = {
            f"{s.shipment_number} | "
            f"{s.origin} → {s.destination} | "
            f"{s.weight_kg} kg": s.id
            for s in shipments
        }

        with st.form("trip_creation"):
            vehicle_label = st.selectbox(
                "Vehicle", list(vehicle_map)
            )

            driver_label = st.selectbox(
                "Driver", list(driver_map)
            )

            selected_shipments = st.multiselect(
                "Select shipments",
                list(shipment_map)
            )

            origin = st.text_input("Trip starting location")
            destination = st.text_input("Trip destination")
            planned_date = st.date_input(
                "Planned departure", value=date.today()
            )

            distance = st.number_input(
                "Estimated distance (km)",
                min_value=0.0,
                step=10.0
            )

            submitted = st.form_submit_button("Create Trip")

            if submitted:
                try:
                    trip_number = create_trip(
                        vehicle_id=vehicle_map[vehicle_label],
                        driver_id=driver_map[driver_label],
                        shipment_ids=[
                            shipment_map[x]
                            for x in selected_shipments
                        ],
                        start_location=origin,
                        end_location=destination,
                        planned_start=planned_date.isoformat(),
                        distance_km=distance,
                        username=user["username"],
                        role=user["role"]
                    )
                    st.success(
                        f"Trip created: {trip_number}"
                    )
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))

    st.divider()
    st.subheader("Trip Register")

    with SessionLocal() as db:
        trips = db.scalars(
            select(Trip).order_by(Trip.id.desc())
        ).all()

        trip_rows = []
        for t in trips:
            vehicle = db.get(Vehicle, t.vehicle_id)
            driver = db.get(Driver, t.driver_id)

            trip_rows.append({
                "ID": t.id,
                "Trip": t.trip_number,
                "Vehicle": vehicle.registration_number if vehicle else "",
                "Driver": driver.name if driver else "",
                "Origin": t.start_location,
                "Destination": t.end_location,
                "Distance": t.distance_km,
                "Status": t.status
            })

    st.dataframe(trip_rows, use_container_width=True)

    if trips:
        st.subheader("Trip Operations")

        trip_options = {
            f"{t.trip_number} ({t.status})": t.id
            for t in trips
        }

        selected = st.selectbox(
            "Select trip",
            list(trip_options)
        )

        trip_id = trip_options[selected]

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "Start Trip",
                use_container_width=True
            ):
                try:
                    start_trip(
                        trip_id,
                        user["username"],
                        user["role"]
                    )
                    st.success("Trip started.")
                    st.rerun()
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))

        with c2:
            if st.button(
                "Complete Trip",
                use_container_width=True
            ):
                try:
                    complete_trip(
                        trip_id,
                        user["username"],
                        user["role"]
                    )
                    st.success("Trip completed.")
                    st.rerun()
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))
