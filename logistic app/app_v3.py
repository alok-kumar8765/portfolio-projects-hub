import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# Page Configuration
st.set_page_config(
    page_title="Generative AI Logistics Enterprise Suite",
    page_icon="🚛",
    layout="wide"
)

# Initialize SQLite Database & Relational Tables
def init_db():
    conn = sqlite3.connect("logistics.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT,
            truck_id TEXT,
            shipment_code TEXT,
            status TEXT,
            progress INTEGER,
            load_current REAL,
            load_max REAL,
            delivery_date TEXT,
            parcels INTEGER,
            client_name TEXT,
            payment_status TEXT,
            amount REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            contact_person TEXT,
            email TEXT,
            active_orders INTEGER,
            total_volume_delivered INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT,
            license_no TEXT,
            phone TEXT,
            assigned_truck TEXT,
            rating REAL,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trucks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_code TEXT,
            model TEXT,
            max_capacity_t REAL,
            fuel_efficiency_kmpl REAL,
            maintenance_status TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_code TEXT,
            driver TEXT,
            truck TEXT,
            completion_date TEXT,
            status TEXT
        )
    ''')
    
    # Populate default mock data if empty
    cursor.execute('SELECT COUNT(*) FROM shipments')
    if cursor.fetchone()[0] == 0:
        default_shipments = [
            ('Julien Morel', 'Truck 12', 'EXP-98564', 'In Delivery', 68, 14.2, 18.0, '25 May 2025', 48, 'Logistics Nord SAS', 'Paid', 4500.0),
            ('Sarah Jenkins', 'Truck 08', 'EXP-98565', 'Pending', 20, 9.0, 15.0, '28 May 2025', 30, 'Global Freight Corp', 'Pending', 2800.0),
            ('David Vance', 'Truck 04', 'EXP-98566', 'Completed', 100, 0.0, 20.0, '20 May 2025', 65, 'Paris Transports SA', 'Paid', 6200.0)
        ]
        cursor.executemany('''
            INSERT INTO shipments (driver_name, truck_id, shipment_code, status, progress, load_current, load_max, delivery_date, parcels, client_name, payment_status, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_shipments)
        
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        default_clients = [
            ('Logistics Nord SAS', 'Marc Antoine', 'contact@logisticsnord.fr', 4, 120),
            ('Global Freight Corp', 'Elena Rostova', 'elena@globalfreight.com', 2, 45),
            ('Paris Transports SA', 'Lucie Bernard', 'support@paristrans.fr', 7, 210)
        ]
        cursor.executemany('INSERT INTO clients (company_name, contact_person, email, active_orders, total_volume_delivered) VALUES (?, ?, ?, ?, ?)', default_clients)

    cursor.execute('SELECT COUNT(*) FROM drivers')
    if cursor.fetchone()[0] == 0:
        default_drivers = [
            ('Julien Morel', 'FR-88392-X', '+33 6 12 34 56 78', 'Truck 12', 4.9, 'On Route'),
            ('Sarah Jenkins', 'FR-99210-B', '+33 6 98 76 54 32', 'Truck 08', 4.7, 'Standby'),
            ('David Vance', 'FR-11234-A', '+33 6 55 44 33 22', 'Truck 04', 4.8, 'Available')
        ]
        cursor.executemany('INSERT INTO drivers (driver_name, license_no, phone, assigned_truck, rating, status) VALUES (?, ?, ?, ?, ?, ?)', default_drivers)

    cursor.execute('SELECT COUNT(*) FROM trucks')
    if cursor.fetchone()[0] == 0:
        default_trucks = [
            ('Truck 12', 'Volvo FH16', 18.0, 4.2, 'Optimal'),
            ('Truck 08', 'Renault T-High', 15.0, 4.8, 'Routine Check'),
            ('Truck 04', 'Mercedes Actros', 20.0, 3.9, 'Optimal')
        ]
        cursor.executemany('INSERT INTO trucks (truck_code, model, max_capacity_t, fuel_efficiency_kmpl, maintenance_status) VALUES (?, ?, ?, ?, ?)', default_trucks)
        
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 👤 Hello, Camille")
st.sidebar.markdown("**Role:** CEO & Operations Dispatcher")
st.sidebar.markdown("---")
nav = st.sidebar.radio("NAVIGATION", ["Overview", "Shipments", "Clients", "Drivers", "Trucks", "Analytics", "History", "Settings"])

conn = sqlite3.connect("logistics.db")

# --- VIEW 1: OVERVIEW (WITH LIVE MAP & PAYMENT OVERVIEW) ---
if nav == "Overview":
    st.title("Suivi logistique - Executive Operations Dashboard")
    
    # Top Control Bar
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        truck_filter = st.selectbox("Select Truck Filter", ["All Trucks", "Truck 12", "Truck 08", "Truck 04"])
    with col2:
        search_query = st.text_input("Search Driver or Shipment Code", "")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔔 Check Alerts"):
            st.toast("🚨 Heavy traffic congestion detected in primary delivery zone.")

    # Financial & Operational KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    df_metrics = pd.read_sql("SELECT SUM(amount) as total, SUM(CASE WHEN payment_status='Paid' THEN amount ELSE 0 END) as collected FROM shipments", conn)
    total_rev = df_metrics['total'].iloc[0] or 0
    collected_rev = df_metrics['collected'].iloc[0] or 0
    
    m1.metric("Global Progression", "72%", "540 km covered")
    m2.metric("Fleet Utilization", "78%", "14.2t / 18.0t avg")
    m3.metric("Total Pipeline Revenue", f"€{total_rev:,.2f}")
    m4.metric("Collected Payments", f"€{collected_rev:,.2f}", f"€{total_rev - collected_rev:,.2f} Pending")

    st.markdown("---")

    # Live Fleet Map Integration (Pydeck over France/Paris region)
    st.subheader("🌍 Live Fleet Telemetry & Spatial Awareness Map")
    map_data = pd.DataFrame({
        'lat': [48.8566, 45.7640, 43.2965],
        'lon': [2.3522, 4.8357, 5.3698],
        'truck': ['Truck 12 (Julien)', 'Truck 08 (Sarah)', 'Truck 04 (David)'],
        'status': ['In Delivery', 'Pending', 'Completed']
    })
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=46.6033, longitude=1.8883, zoom=5, pitch=50),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_color='[6, 182, 212, 200]',
                get_radius=40000,
                pickable=True
            ),
        ],
        tooltip={"text": "Truck: {truck}\nStatus: {status}"}
    ))

    st.markdown("---")

    # Main Grid Layout (2 Columns)
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Active Driver & Fleet Assignment")
        
        query = "SELECT * FROM shipments WHERE 1=1"
        params = []
        if truck_filter != "All Trucks":
            query += " AND truck_id = ?"
            params.append(truck_filter)
        if search_query:
            query += " AND (driver_name LIKE ? OR shipment_code LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        df_ship = pd.read_sql(query, conn, params=params)
        
        if not df_ship.empty:
            row = df_ship.iloc[0]
            st.success(f"**Driver:** {row['driver_name']} | **Truck:** {row['truck_id']}")
            st.write(f"📦 **Shipment ID:** {row['shipment_code']} ({row['parcels']} parcels)")
            st.write(f"🏢 **Client:** {row['client_name']} | 💳 **Payment:** {row['payment_status']} (€{row['amount']})")
            st.write(f"🔄 **Status:** {row['status']} | 📅 **Due:** {row['delivery_date']}")
        else:
            st.info("No matching shipment assignments found for this filter.")

    with right_col:
        st.subheader("Shipment Volume Trends")
        fig, ax = plt.subplots(figsize=(6, 2.5))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        
        days = ['May 19', 'May 20', 'May 21', 'May 22', 'May 23', 'May 24', 'May 25']
        volumes = [65, 70, 58, 82, 75, 90, 85]
        
        ax.plot(days, volumes, color='#06b6d4', marker='o', linewidth=2, markersize=4)
        ax.tick_params(colors='white', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#334155')
        ax.grid(True, color='#334155', linestyle='--', alpha=0.3)
        st.pyplot(fig)

# --- VIEW 2: SHIPMENTS & PAYMENT WORKFLOW ---
elif nav == "Shipments":
    st.title("Shipment & Payment Processing Management")
    st.markdown("Manage shipment tracking, update delivery statuses, and process payment invoice states directly.")

    df = pd.read_sql("SELECT * FROM shipments", conn)
    edited_df = st.data_editor(df, num_rows="dynamic", key="shipment_editor", use_container_width=True)

    if st.button("💾 Save Shipment & Payment Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shipments")
        for _, row in edited_df.iterrows():
            cursor.execute('''
                INSERT INTO shipments (id, driver_name, truck_id, shipment_code, status, progress, load_current, load_max, delivery_date, parcels, client_name, payment_status, amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['id'], row['driver_name'], row['truck_id'], row['shipment_code'], row['status'], row['progress'], row['load_current'], row['load_max'], row['delivery_date'], row['parcels'], row['client_name'], row['payment_status'], row['amount']))
            
            if row['status'] == 'Completed':
                cursor.execute('''
                    INSERT INTO history_logs (trip_code, driver, truck, completion_date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['shipment_code'], row['driver_name'], row['truck_id'], row['delivery_date'], 'Delivered Successfully'))
        
        conn.commit()
        st.success("Database synchronized successfully!")
        st.rerun()

# --- VIEW 3: CLIENTS (WITH MOST/LEAST DELIVERED PRODUCT CHARTS) ---
elif nav == "Clients":
    st.title("Client Accounts & Product Volume Analysis")
    st.markdown("Monitor client contracts and analyze delivery distribution to identify high-volume vs. low-volume accounts.")

    df_clients = pd.read_sql("SELECT * FROM clients", conn)
    edited_clients = st.data_editor(df_clients, num_rows="dynamic", key="client_editor", use_container_width=True)

    if st.button("💾 Save Client Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients")
        for _, row in edited_clients.iterrows():
            cursor.execute("INSERT INTO clients (id, company_name, contact_person, email, active_orders, total_volume_delivered) VALUES (?, ?, ?, ?, ?, ?)",
                           (row['id'], row['company_name'], row['contact_person'], row['email'], row['active_orders'], row['total_volume_delivered']))
        conn.commit()
        st.success("Client records updated!")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Client Delivery Volume Distribution (Most vs. Least Delivered)")
    
    if not df_clients.empty:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        
        ax.barh(df_clients['company_name'], df_clients['total_volume_delivered'], color='#10b981')
        ax.set_xlabel("Total Volume Delivered (Units/Parcels)", color='white')
        ax.tick_params(colors='white', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('#334155')
        st.pyplot(fig)

# --- VIEW 4: DRIVERS (DETAILED CRUD) ---
elif nav == "Drivers":
    st.title("Driver Fleet Personnel Management")
    st.markdown("Add, update, or remove driver profiles, track licenses, safety ratings, and active assignments.")

    df_drivers = pd.read_sql("SELECT * FROM drivers", conn)
    edited_drivers = st.data_editor(df_drivers, num_rows="dynamic", key="driver_editor", use_container_width=True)

    if st.button("💾 Save Driver Records", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drivers")
        for _, row in edited_drivers.iterrows():
            cursor.execute("INSERT INTO drivers (id, driver_name, license_no, phone, assigned_truck, rating, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (row['id'], row['driver_name'], row['license_no'], row['phone'], row['assigned_truck'], row['rating'], row['status']))
        conn.commit()
        st.success("Driver roster updated successfully!")
        st.rerun()

# --- VIEW 5: TRUCKS (FLEET & MAINTENANCE) ---
elif nav == "Trucks":
    st.title("Truck Fleet & Asset Management")
    st.markdown("Manage vehicle specifications, maximum ton capacities, fuel efficiencies, and maintenance statuses.")

    df_trucks = pd.read_sql("SELECT * FROM trucks", conn)
    edited_trucks = st.data_editor(df_trucks, num_rows="dynamic", key="truck_editor", use_container_width=True)

    if st.button("💾 Save Truck Fleet Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trucks")
        for _, row in edited_trucks.iterrows():
            cursor.execute("INSERT INTO trucks (id, truck_code, model, max_capacity_t, fuel_efficiency_kmpl, maintenance_status) VALUES (?, ?, ?, ?, ?, ?)",
                           (row['id'], row['truck_code'], row['model'], row['max_capacity_t'], row['fuel_efficiency_kmpl'], row['maintenance_status']))
        conn.commit()
        st.success("Truck asset database updated!")
        st.rerun()

# --- VIEW 6: ANALYTICS ---
elif nav == "Analytics":
    st.title("Enterprise Fleet Analytics & Performance Reports")
    m1, m2 = st.columns(2)
    m1.metric(label="On-Time Delivery Rate", value="94%", delta="Target: 90% (Exceeding)")
    m2.metric(label="Fleet Fuel Efficiency Average", value="4.3 km/L", delta="+0.4 vs last month")
    
    st.subheader("Monthly Delivery Success Rate vs Target")
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    performance = [91, 89, 95, 94]
    
    ax.bar(weeks, performance, color='#06b6d4', width=0.4)
    ax.axhline(y=90, color='#f43f5e', linestyle='--', label='Target (90%)')
    ax.tick_params(colors='white', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#334155')
    ax.legend(facecolor='#0e1117', edgecolor='#334155', labelcolor='white')
    st.pyplot(fig)

# --- VIEW 7: HISTORY ---
elif nav == "History":
    st.title("Completed Delivery Audit Log")
    df_history = pd.read_sql("SELECT * FROM history_logs", conn)
    st.dataframe(df_history, use_container_width=True)

# --- VIEW 8: SETTINGS ---
elif nav == "Settings":
    st.title("System Configurations & Dispatch Preferences")
    st.checkbox("Enable Real-Time GPS Geofencing & Telemetry", value=True)
    st.checkbox("Automated Payment Gateway Sync (Stripe/Bank)", value=True)
    if st.button("Save Preferences"):
        st.success("System configurations saved successfully!")

conn.close()