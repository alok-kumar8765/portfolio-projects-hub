import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# -----------------------------------------------------------------------------
# PAGE CONFIG & THEMES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Small Business ERP Lite",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme CSS Injector
def inject_theme_css(theme_name):
    if theme_name == "Modern Dark":
        bg_color = "#12121c"
        card_bg = "#1e1e2f"
        text_color = "#ffffff"
        accent_color = "#6c5ce7"
        sidebar_bg = "#161625"
    elif theme_name == "Light Clean":
        bg_color = "#f4f7f6"
        card_bg = "#ffffff"
        text_color = "#2c3e50"
        accent_color = "#3498db"
        sidebar_bg = "#e9ecef"
    else:  # Cyberpunk
        bg_color = "#0b0514"
        card_bg = "#170a2c"
        text_color = "#00ffcc"
        accent_color = "#ff007f"
        sidebar_bg = "#07020d"

    css = f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}
    div[data-testid="stMetric"] {{
        background-color: {card_bg};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    /* Multicolor Footer Style */
    .multicolor-footer {{
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 15px;
        font-weight: bold;
        border-top: 1px solid rgba(255,255,255,0.1);
    }}
    .footer-text-1 {{ color: #ff3366; }}
    .footer-text-2 {{ color: #ff9900; }}
    .footer-text-3 {{ color: #33cc33; }}
    .footer-text-4 {{ color: #3399ff; }}
    .footer-text-5 {{ color: #cc33ff; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE INIT & HELPERS (SQLite for Portable Execution)
# -----------------------------------------------------------------------------
DB_NAME = "erp_lite.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Inventory Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            category TEXT,
            quantity INTEGER,
            min_stock INTEGER,
            price REAL
        )
    """)
    
    # Sales Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            item_name TEXT,
            quantity INTEGER,
            total_price REAL,
            date TEXT
        )
    """)
    
    # Customers Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)
    
    # Insert Sample Data if Empty
    cur.execute("SELECT COUNT(*) FROM inventory")
    if cur.fetchone()[0] == 0:
        sample_items = [
            ("Laptop Pro 15", "Electronics", 12, 5, 1200.00),
            ("Wireless Mouse", "Electronics", 45, 10, 25.00),
            ("Mechanical Keyboard", "Electronics", 4, 8, 85.00),
            ("Office Desk Chair", "Furniture", 8, 3, 150.00),
            ("USB-C Hub", "Electronics", 3, 5, 40.00)
        ]
        cur.executemany("INSERT INTO inventory (item_name, category, quantity, min_stock, price) VALUES (?,?,?,?,?)", sample_events if 'sample_events' in locals() else sample_items)
        
        sample_sales = [
            ("Alice Smith", "Laptop Pro 15", 1, 1200.00, "2026-11-01"),
            ("Bob Jones", "Wireless Mouse", 2, 50.00, "2026-11-02"),
            ("Charlie Brown", "Office Desk Chair", 1, 150.00, "2026-11-03")
        ]
        cur.executemany("INSERT INTO sales (customer_name, item_name, quantity, total_price, date) VALUES (?,?,?,?,?)", sample_sales)
        
        sample_customers = [
            ("Alice Smith", "alice@example.com", "555-0192"),
            ("Bob Jones", "bob@example.com", "555-0143"),
            ("Charlie Brown", "charlie@example.com", "555-0188")
        ]
        cur.executemany("INSERT INTO customers (name, email, phone) VALUES (?,?,?)", sample_customers)
        
        conn.commit()
    conn.close()

init_db()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("💼 ERP Lite")
theme_choice = st.sidebar.selectbox("🎨 Select Theme", ["Modern Dark", "Light Clean", "Cyberpunk"])
inject_theme_css(theme_choice)

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", [
    "📊 Real-Time Analytics", 
    "📦 Inventory Management", 
    "🛍️ Sales & Orders", 
    "👥 Customer Directory", 
    "⚠️ Low Stock Alerts"
])

# -----------------------------------------------------------------------------
# MODULE 1: REAL-TIME ANALYTICS DASHBOARD
# -----------------------------------------------------------------------------
if menu == "📊 Real-Time Analytics":
    st.title("📈 Real-Time Business Analytics")
    
    conn = get_db_connection()
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    inv_df = pd.read_sql_query("SELECT * FROM inventory", conn)
    cust_df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()

    total_revenue = sales_df["total_price"].sum() if not sales_df.empty else 0.0
    total_sales_count = len(sales_df)
    total_items = inv_df["quantity"].sum() if not inv_df.empty else 0
    low_stock_count = len(inv_df[inv_df["quantity"] <= inv_df["min_stock"]]) if not inv_df.empty else 0

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Orders", total_sales_count)
    col3.metric("Stock Units", total_items)
    col4.metric("Low Stock Items", low_stock_count, delta_color="inverse")

    st.markdown("---")

    # Analytics Charts using Pandas & Streamlit native charts
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sales Revenue Trend")
        if not sales_df.empty:
            revenue_by_date = sales_df.groupby("date")["total_price"].sum().reset_index()
            st.line_chart(revenue_by_date.set_index("date"))
        else:
            st.info("No sales data available yet.")

    with col_b:
        st.subheader("Inventory Stock Levels")
        if not inv_df.empty:
            st.bar_chart(inv_df.set_index("item_name")["quantity"])
        else:
            st.info("No inventory data available.")

# -----------------------------------------------------------------------------
# MODULE 2: INVENTORY MANAGEMENT
# -----------------------------------------------------------------------------
elif menu == "📦 Inventory Management":
    st.title("📦 Inventory Management")
    
    conn = get_db_connection()
    inv_df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()

    st.dataframe(inv_df, use_container_width=True)

    st.subheader("➕ Add New Inventory Item")
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        item_name = col1.text_input("Item Name")
        category = col2.selectbox("Category", ["Electronics", "Furniture", "Office Supplies", "Services"])
        
        col3, col4, col5 = st.columns(3)
        quantity = col3.number_input("Quantity", min_value=0, value=10)
        min_stock = col4.number_input("Low Stock Warning Level", min_value=1, value=5)
        price = col5.number_input("Price ($)", min_value=0.0, value=50.0)
        
        submit = st.form_submit_button("Add Item")
        if submit:
            if item_name:
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO inventory (item_name, category, quantity, min_stock, price) VALUES (?,?,?,?,?)",
                                (item_name, category, quantity, min_stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{item_name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding item: {e}")
            else:
                st.warning("Please enter an item name.")

# -----------------------------------------------------------------------------
# MODULE 3: SALES & ORDERS
# -----------------------------------------------------------------------------
elif menu == "🛍️ Sales & Orders":
    st.title("🛍️ Sales & Purchase Tracking")

    conn = get_db_connection()
    inv_df = pd.read_sql_query("SELECT * FROM inventory WHERE quantity > 0", conn)
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()

    st.subheader("🛒 Record New Sale")
    if not inv_df.empty:
        with st.form("sales_form"):
            customer_name = st.text_input("Customer Name")
            item_choice = st.selectbox("Select Item", inv_df["item_name"].tolist())
            
            selected_item_info = inv_df[inv_df["item_name"] == item_choice].iloc[0]
            max_qty = int(selected_item_info["quantity"])
            unit_price = float(selected_item_info["price"])
            
            qty = st.number_input(f"Quantity (Available: {max_qty})", min_value=1, max_value=max_qty, value=1)
            total_cost = qty * unit_price
            st.info(f"Total Amount: **${total_cost:,.2f}**")

            submit_sale = st.form_submit_button("Complete Sale")
            if submit_sale:
                if customer_name:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    # Record Sale
                    cur.execute("INSERT INTO sales (customer_name, item_name, quantity, total_price, date) VALUES (?,?,?,?,?)",
                                (customer_name, item_choice, qty, total_cost, datetime.now().strftime("%Y-%m-%d")))
                    # Update Inventory
                    cur.execute("UPDATE inventory SET quantity = quantity - ? WHERE item_name = ?", (qty, item_choice))
                    conn.commit()
                    conn.close()
                    st.success("Sale completed successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter a customer name.")
    else:
        st.warning("No stock available to sell.")

    st.subheader("📜 Recent Transactions")
    st.dataframe(sales_df, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 4: CUSTOMER DIRECTORY
# -----------------------------------------------------------------------------
elif menu == "👥 Customer Directory":
    st.title("👥 Customer Management")

    conn = get_db_connection()
    cust_df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()

    st.dataframe(cust_df, use_container_width=True)

    with st.form("add_customer_form"):
        st.subheader("➕ Register New Customer")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        
        if st.form_submit_button("Save Customer"):
            if name:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO customers (name, email, phone) VALUES (?,?,?)", (name, email, phone))
                conn.commit()
                conn.close()
                st.success("Customer saved successfully!")
                st.rerun()

# -----------------------------------------------------------------------------
# MODULE 5: LOW STOCK ALERTS
# -----------------------------------------------------------------------------
elif menu == "⚠️ Low Stock Alerts":
    st.title("⚠️ Low Stock Alerts")
    
    conn = get_db_connection()
    inv_df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()

    low_stock_df = inv_df[inv_df["quantity"] <= inv_df["min_stock"]]

    if not low_stock_df.empty:
        st.error(f"⚠️ Warning: {len(low_stock_df)} item(s) are at or below safety threshold!")
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("✅ All inventory items are sufficiently stocked!")

# -----------------------------------------------------------------------------
# MULTICOLOR CENTERED FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="multicolor-footer">
    <span class="footer-text-1">Creator:</span> 
    <span class="footer-text-2">Generative AI</span> 
    <span class="footer-text-3">|</span> 
    <span class="footer-text-4">Copyrights</span> 
    <span class="footer-text-5">2026</span>
</div>
""", unsafe_allow_html=True)