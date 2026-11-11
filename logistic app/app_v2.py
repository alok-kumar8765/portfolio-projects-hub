import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Generative AI Logistics Suite",
    page_icon="🚛",
    layout="wide"
)

# Initialize SQLite Database & Mock Data
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
            parcels INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            contact_person TEXT,
            email TEXT,
            active_orders INTEGER
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
            ('Julien Morel', 'Truck 12', 'EXP-98564', 'In Delivery', 68, 14.2, 18.0, '25 May 2025', 48),
            ('Sarah Jenkins', 'Truck 08', 'EXP-98565', 'Pending', 20, 9.0, 15.0, '28 May 2025', 30),
            ('David Vance', 'Truck 04', 'EXP-98566', 'Completed', 100, 0.0, 20.0, '20 May 2025', 65)
        ]
        cursor.executemany('''
            INSERT INTO shipments (driver_name, truck_id, shipment_code, status, progress, load_current, load_max, delivery_date, parcels)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_shipments)
        
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        default_clients = [
            ('Logistics Nord SAS', 'Marc Antoine', 'contact@logisticsnord.fr', 4),
            ('Global Freight Corp', 'Elena Rostova', 'elena@globalfreight.com', 2),
            ('Paris Transports SA', 'Lucie Bernard', 'support@paristrans.fr', 7)
        ]
        cursor.executemany('INSERT INTO clients (company_name, contact_person, email, active_orders) VALUES (?, ?, ?, ?)', default_clients)

    cursor.execute('SELECT COUNT(*) FROM history_logs')
    if cursor.fetchone()[0] == 0:
        default_history = [
            ('TRIP-4091', 'David Vance', 'Truck 04', '20 May 2025', 'Delivered Successfully')
        ]
        cursor.executemany('INSERT INTO history_logs (trip_code, driver, truck, completion_date, status) VALUES (?, ?, ?, ?, ?)', default_history)
        
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 👤 Hello, Camille")
st.sidebar.markdown("---")
nav = st.sidebar.radio("NAVIGATION", ["Overview", "Shipments", "Clients", "Analytics", "History", "Settings"])

conn = sqlite3.connect("logistics.db")

# --- VIEW 1: OVERVIEW ---
if nav == "Overview":
    st.title("Suivi logistique - Operations Dashboard")
    
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

    # Status Quick Filters
    scols = st.columns(3)
    with scols[0]:
        if st.button("🔴 Filter: In Delivery", use_container_width=True):
            st.session_state['status_filter'] = 'In Delivery'
    with scols[1]:
        if st.button("🟡 Filter: Pending", use_container_width=True):
            st.session_state['status_filter'] = 'Pending'
    with scols[2]:
        if st.button("🟢 Filter: Completed", use_container_width=True):
            st.session_state['status_filter'] = 'Completed'

    active_status = st.session_state.get('status_filter', None)
    if active_status:
        st.info(f"Active Status Filter: **{active_status}** (Clear filters via dropdown if needed)")

    st.markdown("---")

    # Main Grid Layout (2 Columns)
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Global Progression")
        st.metric(label="Overall Completion Rate", value="72%", delta="540 km covered")
        st.progress(0.72)
        st.caption("⏱ Estimated remaining time: 1h 20 min")

        st.warning("🚨 **Live Alert**: Slowdown expected due to heavy traffic congestion in your active delivery sector.")

        st.subheader("Active Driver & Fleet Assignment")
        
        query = "SELECT * FROM shipments WHERE 1=1"
        params = []
        if truck_filter != "All Trucks":
            query += " AND truck_id = ?"
            params.append(truck_filter)
        if search_query:
            query += " AND (driver_name LIKE ? OR shipment_code LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        if active_status:
            query += " AND status = ?"
            params.append(active_status)

        df_ship = pd.read_sql(query, conn, params=params)
        
        if not df_ship.empty:
            row = df_ship.iloc[0]
            st.success(f"**Driver:** {row['driver_name']} | **Truck:** {row['truck_id']}")
            st.write(f"📦 **Shipment ID:** {row['shipment_code']} ({row['parcels']} parcels)")
            st.write(f"🔄 **Status:** {row['status']} | 📅 **Due:** {row['delivery_date']}")
        else:
            st.info("No matching shipment assignments found for this filter.")

    with right_col:
        st.subheader("Truck Capacity Management")
        st.metric(label="Capacity Utilized", value="78%", delta="14.2 t / 18.0 t max")
        st.progress(0.78)

        st.subheader("Shipment Volume Trends")
        fig, ax = plt.subplots(figsize=(6, 2.8))
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

# --- VIEW 2: SHIPMENTS (DATABASE & STATUS UPDATES) ---
elif nav == "Shipments":
    st.title("Shipment Management & Status Control")
    st.markdown("Edit shipment records directly in the table below. Changing status to **Completed** automatically logs the trip into history and frees up fleet capacity.")

    df = pd.read_sql("SELECT * FROM shipments", conn)
    edited_df = st.data_editor(df, num_rows="dynamic", key="shipment_editor", use_container_width=True)

    if st.button("💾 Save Database Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shipments")
        for _, row in edited_df.iterrows():
            cursor.execute('''
                INSERT INTO shipments (id, driver_name, truck_id, shipment_code, status, progress, load_current, load_max, delivery_date, parcels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['id'], row['driver_name'], row['truck_id'], row['shipment_code'], row['status'], row['progress'], row['load_current'], row['load_max'], row['delivery_date'], row['parcels']))
            
            # Automated Workflow: If completed, log to history
            if row['status'] == 'Completed':
                cursor.execute('''
                    INSERT INTO history_logs (trip_code, driver, truck, completion_date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['shipment_code'], row['driver_name'], row['truck_id'], row['delivery_date'], 'Delivered Successfully'))
        
        conn.commit()
        st.success("Shipment database updated successfully!")
        st.rerun()

# --- VIEW 3: CLIENTS ---
elif nav == "Clients":
    st.title("Client Accounts & Directory")
    st.markdown("Add, modify, or delete client accounts in real time.")

    df_clients = pd.read_sql("SELECT * FROM clients", conn)
    edited_clients = st.data_editor(df_clients, num_rows="dynamic", key="client_editor", use_container_width=True)

    if st.button("💾 Save Client Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients")
        for _, row in edited_clients.iterrows():
            cursor.execute("INSERT INTO clients (id, company_name, contact_person, email, active_orders) VALUES (?, ?, ?, ?, ?)",
                           (row['id'], row['company_name'], row['contact_person'], row['email'], row['active_orders']))
        conn.commit()
        st.success("Client records updated successfully!")
        st.rerun()

# --- VIEW 4: ANALYTICS ---
elif nav == "Analytics":
    st.title("Fleet Analytics & Performance Reports")
    st.metric(label="On-Time Delivery Rate", value="94%", delta="Target: 90% (Exceeding)")
    
    st.subheader("Monthly Delivery Success Rate vs Target")
    fig, ax = plt.subplots(figsize=(8, 3.5))
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

# --- VIEW 5: HISTORY ---
elif nav == "History":
    st.title("Completed Delivery History Log")
    df_history = pd.read_sql("SELECT * FROM history_logs", conn)
    st.dataframe(df_history, use_container_width=True)

# --- VIEW 6: SETTINGS ---
elif nav == "Settings":
    st.title("System Configurations & Dispatch Preferences")
    
    st.checkbox("Enable Real-Time Traffic & Weather Alerts", value=True)
    st.checkbox("Auto-Sync Driver Telemetry with SQLite Database", value=True)
    
    if st.button("Save Preferences"):
        st.success("System configurations saved successfully!")

conn.close()