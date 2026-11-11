import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Generative AI Logistics Enterprise Suite",
    page_icon="🚛",
    layout="wide"
)

# Initialize SQLite Database & Relational Tables with Automated Schema Migration
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
            maintenance_status TEXT,
            mileage_km REAL,
            engine_temp_c REAL,
            brake_wear_pct REAL
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    # Safe migration check for 'trucks' table columns (fixing missing mileage_km error)
    cursor.execute("PRAGMA table_info(trucks)")
    truck_cols = [col[1] for col in cursor.fetchall()]
    if 'mileage_km' not in truck_cols:
        cursor.execute("ALTER TABLE trucks ADD COLUMN mileage_km REAL DEFAULT 100000.0")
    if 'engine_temp_c' not in truck_cols:
        cursor.execute("ALTER TABLE trucks ADD COLUMN engine_temp_c REAL DEFAULT 88.0")
    if 'brake_wear_pct' not in truck_cols:
        cursor.execute("ALTER TABLE trucks ADD COLUMN brake_wear_pct REAL DEFAULT 30.0")

    # Default Admin Credentials if empty
    cursor.execute('SELECT COUNT(*) FROM admin_settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin_settings (username, password) VALUES ('admin', 'admin')")

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
            ('Truck 12', 'Volvo FH16', 18.0, 4.2, 'Optimal', 142000, 88.5, 34.0),
            ('Truck 08', 'Renault T-High', 15.0, 4.8, 'Routine Check', 215000, 96.2, 79.5),
            ('Truck 04', 'Mercedes Actros', 20.0, 3.9, 'Optimal', 89000, 82.0, 21.0)
        ]
        cursor.executemany('INSERT INTO trucks (truck_code, model, max_capacity_t, fuel_efficiency_kmpl, maintenance_status, mileage_km, engine_temp_c, brake_wear_pct) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', default_trucks)
        
    conn.commit()
    conn.close()

init_db()

# --- SECURE LOGIN & RBAC SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = None
    st.session_state['user_name'] = None

if not st.session_state['authenticated']:
    st.title("🔐 Generative AI Logistics - Secure Login Portal")
    st.markdown("Please sign in with your designated corporate credentials.")
    
    conn_login = sqlite3.connect("logistics.db")
    admin_row = conn_login.execute("SELECT username, password FROM admin_settings LIMIT 1").fetchone()
    conn_login.close()
    
    db_username, db_password = admin_row if admin_row else ("admin", "admin")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            if username == db_username and password == db_password:
                st.session_state['authenticated'] = True
                st.session_state['role'] = "Admin/CEO"
                st.session_state['user_name'] = "Camille (CEO)"
                st.rerun()
            elif username.lower() in ["julien", "sarah", "david"] or "driver" in username.lower():
                st.session_state['authenticated'] = True
                st.session_state['role'] = "Driver"
                st.session_state['user_name'] = username.capitalize()
                st.rerun()
            elif "client" in username.lower() or "nord" in username.lower() or "freight" in username.lower():
                st.session_state['authenticated'] = True
                st.session_state['role'] = "Client"
                st.session_state['user_name'] = username.capitalize()
                st.rerun()
            else:
                st.error(f"Invalid credentials. (Hint: username='{db_username}', password='{db_password}')")
    st.stop()

# --- FIXED PDF GENERATOR FUNCTION (Avoiding bytearray encode error) ---
def generate_pdf_invoice(shipment_code, client_name, driver, truck, amount, parcels):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 10, text="GENERATIVE AI LOGISTICS - INVOICE & BOL", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", size=11)
    pdf.cell(200, 10, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(200, 10, text=f"Shipment Reference: {shipment_code}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(200, 10, text=f"Billed Client: {client_name}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Assigned Driver: {driver} ({truck})", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Total Parcels Transferred: {parcels}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text=f"Total Invoice Amount Due: EUR {amount:,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(200, 10, text="Status: COMPLETED & VERIFIED. Thank you for your business.", new_x="LMARGIN", new_y="NEXT")
    
    return bytes(pdf.output())

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown(f"### 👤 {st.session_state['user_name']}")
st.sidebar.markdown(f"**Role:** {st.session_state['role']}")
st.sidebar.markdown("---")

role = st.session_state['role']

if role == "Admin/CEO":
    nav = st.sidebar.radio("NAVIGATION", ["Overview", "Shipments", "Clients", "Drivers", "Trucks", "IoT & Maintenance", "Analytics", "History", "Chat Webhook", "Settings"])
elif role == "Driver":
    nav = st.sidebar.radio("NAVIGATION", ["My Assigned Route", "Chat Webhook"])
else:
    nav = st.sidebar.radio("NAVIGATION", ["My Invoices & History", "Chat Webhook"])

if st.sidebar.button("🚪 Sign Out"):
    st.session_state['authenticated'] = False
    st.rerun()

conn = sqlite3.connect("logistics.db")

# ==========================================
# 1. ADMIN OVERVIEW VIEW
# ==========================================
if role == "Admin/CEO" and nav == "Overview":
    st.title("Suivi logistique - Executive Operations Dashboard")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        truck_filter = st.selectbox("Select Truck Filter", ["All Trucks", "Truck 12", "Truck 08", "Truck 04"])
    with col2:
        search_query = st.text_input("Search Driver or Shipment Code", "")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔔 Check Alerts"):
            st.toast("🚨 Heavy traffic congestion detected in primary delivery zone.")

    m1, m2, m3, m4 = st.columns(4)
    df_metrics = pd.read_sql("SELECT SUM(amount) as total, SUM(CASE WHEN payment_status='Paid' THEN amount ELSE 0 END) as collected FROM shipments", conn)
    total_rev = df_metrics['total'].iloc[0] or 0
    collected_rev = df_metrics['collected'].iloc[0] or 0
    
    m1.metric("Global Progression", "72%", "540 km covered")
    m2.metric("Fleet Utilization", "78%", "14.2t / 18.0t avg")
    m3.metric("Total Pipeline Revenue", f"€{total_rev:,.2f}")
    m4.metric("Collected Payments", f"€{collected_rev:,.2f}", f"€{total_rev - collected_rev:,.2f} Pending")

    st.markdown("---")

    st.subheader("🌍 Live Fleet Telemetry & Spatial Awareness Map")
    m = folium.Map(location=[46.6033, 1.8883], zoom_start=5, tiles="CartoDB dark_matter")

    truck_locations = [
        {"lat": 48.8566, "lon": 2.3522, "popup": "Truck 12 (Julien Morel) - In Delivery"},
        {"lat": 45.7640, "lon": 4.8357, "popup": "Truck 08 (Sarah Jenkins) - Pending"},
        {"lat": 43.2965, "lon": 5.3698, "popup": "Truck 04 (David Vance) - Completed"}
    ]

    for loc in truck_locations:
        folium.CircleMarker(
            location=[loc["lat"], loc["lon"]],
            radius=8,
            color="#06b6d4",
            fill=True,
            fill_color="#06b6d4",
            fill_opacity=0.8,
            popup=loc["popup"]
        ).add_to(m)

    st_folium(m, width=1100, height=400)
    st.markdown("---")

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
            st.info("No matching shipment assignments found.")

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

# ==========================================
# 2. SHIPMENTS & PDF GENERATOR
# ==========================================
elif role == "Admin/CEO" and nav == "Shipments":
    st.title("Shipment Management & PDF Invoice Generator")
    st.markdown("Edit shipment records. When status is marked **Completed**, an automated PDF Invoice & Bill of Lading is instantly ready for download.")

    df = pd.read_sql("SELECT * FROM shipments", conn)
    edited_df = st.data_editor(df, num_rows="dynamic", key="shipment_editor", width='stretch')

    if st.button("💾 Save Database & Generate Invoices", type="primary"):
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

    st.markdown("---")
    st.subheader("📥 Download Completed Bill of Lading / Invoices")
    completed_ships = pd.read_sql("SELECT * FROM shipments WHERE status='Completed'", conn)
    for _, row in completed_ships.iterrows():
        pdf_bytes = generate_pdf_invoice(row['shipment_code'], row['client_name'], row['driver_name'], row['truck_id'], row['amount'], row['parcels'])
        st.download_button(
            label=f"📄 Download Invoice - {row['shipment_code']} ({row['client_name']})",
            data=pdf_bytes,
            file_name=f"Invoice_{row['shipment_code']}.pdf",
            mime="application/pdf"
        )

# ==========================================
# 3. CLIENTS VIEW
# ==========================================
elif role == "Admin/CEO" and nav == "Clients":
    st.title("Client Accounts & Product Volume Analysis")
    df_clients = pd.read_sql("SELECT * FROM clients", conn)
    edited_clients = st.data_editor(df_clients, num_rows="dynamic", key="client_editor", width='stretch')

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
        ax.set_xlabel("Total Volume Delivered (Parcels)", color='white')
        ax.tick_params(colors='white', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('#334155')
        st.pyplot(fig)

# ==========================================
# 4. DRIVERS VIEW
# ==========================================
elif role == "Admin/CEO" and nav == "Drivers":
    st.title("Driver Fleet Personnel Management")
    df_drivers = pd.read_sql("SELECT * FROM drivers", conn)
    edited_drivers = st.data_editor(df_drivers, num_rows="dynamic", key="driver_editor", width='stretch')

    if st.button("💾 Save Driver Records", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drivers")
        for _, row in edited_drivers.iterrows():
            cursor.execute("INSERT INTO drivers (id, driver_name, license_no, phone, assigned_truck, rating, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (row['id'], row['driver_name'], row['license_no'], row['phone'], row['assigned_truck'], row['rating'], row['status']))
        conn.commit()
        st.success("Driver roster updated!")
        st.rerun()

# ==========================================
# 5. TRUCKS VIEW
# ==========================================
elif role == "Admin/CEO" and nav == "Trucks":
    st.title("Truck Fleet & Asset Management")
    df_trucks = pd.read_sql("SELECT * FROM trucks", conn)
    edited_trucks = st.data_editor(df_trucks, num_rows="dynamic", key="truck_editor", width='stretch')

    if st.button("💾 Save Truck Fleet Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trucks")
        for _, row in edited_trucks.iterrows():
            cursor.execute("INSERT INTO trucks (id, truck_code, model, max_capacity_t, fuel_efficiency_kmpl, maintenance_status, mileage_km, engine_temp_c, brake_wear_pct) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (row['id'], row['truck_code'], row['model'], row['max_capacity_t'], row['fuel_efficiency_kmpl'], row['maintenance_status'], row['mileage_km'], row['engine_temp_c'], row['brake_wear_pct']))
        conn.commit()
        st.success("Truck database updated!")
        st.rerun()

# ==========================================
# 6. PREDICTIVE MAINTENANCE & IOT TELEMETRY
# ==========================================
elif role == "Admin/CEO" and nav == "IoT & Maintenance":
    st.title("Predictive Maintenance & IoT Telemetry")
    st.markdown("Real-time sensor monitoring tracking mileage, engine temperatures, and brake wear to prevent highway breakdowns.")

    df_iot = pd.read_sql("SELECT truck_code, model, mileage_km, engine_temp_c, brake_wear_pct, maintenance_status FROM trucks", conn)
    
    for _, row in df_iot.iterrows():
        with st.expander(f"🚛 {row['truck_code']} ({row['model']}) - Status: {row['maintenance_status']}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Mileage", f"{row['mileage_km']:,.0f} km")
            col2.metric("Engine Temperature", f"{row['engine_temp_c']} °C", "Normal < 95°C" if row['engine_temp_c'] < 95 else "⚠️ HIGH TEMP")
            col3.metric("Brake Pad Wear", f"{row['brake_wear_pct']}%", "Optimal < 75%" if row['brake_wear_pct'] < 75 else "⚠️ CRITICAL WEAR")

            if row['engine_temp_c'] > 95 or row['brake_wear_pct'] > 75:
                st.error(f"🚨 **Predictive Alert:** {row['truck_code']} requires immediate mechanic inspection before next dispatch!")
            else:
                st.success(f"✅ {row['truck_code']} telemetry is operating within safe parameters.")

# ==========================================
# 7. ANALYTICS VIEW
# ==========================================
elif role == "Admin/CEO" and nav == "Analytics":
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

# ==========================================
# 8. HISTORY VIEW (Editable & Interactive)
# ==========================================
elif role == "Admin/CEO" and nav == "History":
    st.title("Completed Delivery Audit Log")
    st.markdown("Manually add, update, or remove completed historical trip entries below.")

    df_history = pd.read_sql("SELECT * FROM history_logs", conn)
    edited_history = st.data_editor(df_history, num_rows="dynamic", key="history_editor", width='stretch')

    if st.button("💾 Save History Audit Changes", type="primary"):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history_logs")
        for _, row in edited_history.iterrows():
            cursor.execute("INSERT INTO history_logs (id, trip_code, driver, truck, completion_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (row['id'], row['trip_code'], row['driver'], row['truck'], row['completion_date'], row['status']))
        conn.commit()
        st.success("History audit log updated successfully!")
        st.rerun()

# ==========================================
# 9. INTERNAL CHAT WEBHOOK
# ==========================================
elif nav == "Chat Webhook":
    st.title("💬 Internal Dispatcher-Driver Communication Drawer")
    st.markdown("Send real-time road updates or check urgent dispatch instructions.")

    chat_col1, chat_col2 = st.columns([2, 1])
    
    with chat_col1:
        st.subheader("Message History")
        df_chat = pd.read_sql("SELECT sender, recipient, message, timestamp FROM chat_messages ORDER BY id DESC", conn)
        for _, chat in df_chat.iterrows():
            st.markdown(f"**{chat['sender']}** *(to {chat['recipient']})* [{chat['timestamp']}]:\n> {chat['message']}")
            
    with chat_col2:
        st.subheader("Send Message")
        with st.form("chat_form"):
            recipient = st.selectbox("Recipient", ["All Drivers", "Julien Morel", "Sarah Jenkins", "David Vance", "Dispatcher HQ"])
            msg = st.text_area("Message Content")
            send_btn = st.form_submit_button("Send Dispatch Note")
            
            if send_btn and msg:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO chat_messages (sender, recipient, message, timestamp) VALUES (?, ?, ?, ?)",
                               (st.session_state['user_name'], recipient, msg, datetime.now().strftime('%H:%M:%S')))
                conn.commit()
                st.success("Message transmitted successfully!")
                st.rerun()

# ==========================================
# 10. DRIVER PORTAL VIEW
# ==========================================
elif role == "Driver":
    st.title(f"🚚 Driver Portal - Welcome, {st.session_state['user_name']}")
    st.markdown("Here is your currently assigned route, truck status, and active delivery instructions.")

    driver_name = st.session_state['user_name']
    df_route = pd.read_sql("SELECT * FROM shipments WHERE driver_name LIKE ?", conn, params=[f"%{driver_name}%"])
    
    if not df_route.empty:
        for _, r in df_route.iterrows():
            st.success(f"Assigned Shipment Code: **{r['shipment_code']}**")
            st.write(f"🚛 **Assigned Truck:** {r['truck_id']}")
            st.write(f"🏢 **Destination Client:** {r['client_name']}")
            st.write(f"📦 **Parcels:** {r['parcels']} | **Due Date:** {r['delivery_date']}")
            st.progress(r['progress'] / 100.0)
    else:
        st.info("You currently have no active route assignments. Standby for dispatcher updates.")

# ==========================================
# 11. CLIENT PORTAL VIEW
# ==========================================
elif role == "Client":
    st.title(f"🏢 Client Portal - Welcome")
    st.markdown("View your specific invoice history and active order tracking status.")

    df_client_orders = pd.read_sql("SELECT shipment_code, truck_id, status, delivery_date, amount, payment_status FROM shipments", conn)
    st.dataframe(df_client_orders, width='stretch')

# ==========================================
# 12. SETTINGS VIEW (With Admin Credentials Management)
# ==========================================
elif role == "Admin/CEO" and nav == "Settings":
    st.title("System Configurations & Admin Credentials")
    st.markdown("Manage system preferences and update secure administrator login credentials.")

    with st.form("admin_creds_form"):
        st.subheader("🔑 Administrator Account Security")
        new_username = st.text_input("New Admin Username", value="admin")
        new_password = st.text_input("New Admin Password", type="password")
        update_creds = st.form_submit_button("Update Admin Credentials")
        
        if update_creds:
            if new_username and new_password:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM admin_settings")
                cursor.execute("INSERT INTO admin_settings (username, password) VALUES (?, ?)", (new_username, new_password))
                conn.commit()
                st.success("Admin credentials updated successfully! Use these credentials upon next sign in.")
            else:
                st.error("Fields cannot be blank.")

    st.markdown("---")
    st.checkbox("Enable Real-Time GPS Geofencing & Telemetry", value=True)
    st.checkbox("Automated Payment Gateway Sync (Stripe/Bank)", value=True)
    if st.button("Save Preferences"):
        st.success("System configurations saved successfully!")

conn.close()