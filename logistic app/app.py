import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
            ('TRIP-4091', 'David Vance', 'Truck 04', '20 May 2025', 'Delivered Successfully'),
            ('TRIP-4088', 'Marc Leroy', 'Truck 02', '18 May 2025', 'Delivered Successfully')
        ]
        cursor.executemany('INSERT INTO history_logs (trip_code, driver, truck, completion_date, status) VALUES (?, ?, ?, ?, ?)', default_history)
        
    conn.commit()
    conn.close()

class LogisticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Generative AI Logistics - Enterprise Suite")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Theme Palette matching modern dark UI standard
        self.bg_dark = "#0f172a"
        self.bg_sidebar = "#090d16"
        self.card_bg = "#1e293b"
        self.border_color = "#334155"
        self.accent_cyan = "#06b6d4"
        self.accent_emerald = "#10b981"
        self.accent_rose = "#f43f5e"
        self.text_light = "#f8fafc"
        self.text_muted = "#94a3b8"
        
        self.root.configure(bg=self.bg_dark)
        init_db()
        
        self.nav_buttons = {}
        self.selected_truck_filter = None
        self.build_ui()
        
    def build_ui(self):
        sidebar = tk.Frame(self.root, bg=self.bg_sidebar, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        self.build_sidebar(sidebar)
        
        self.main_content = tk.Frame(self.root, bg=self.bg_dark)
        self.main_content.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        self.switch_view("Overview")
        
    def build_sidebar(self, parent):
        profile_frame = tk.Frame(parent, bg=self.bg_sidebar)
        profile_frame.pack(pady=25, padx=15, fill="x")
        
        avatar_lbl = tk.Label(profile_frame, text="👤", font=("Segoe UI", 18), bg=self.card_bg, fg=self.accent_cyan, width=2, height=1)
        avatar_lbl.pack(side="left", padx=(0, 10))
        
        greeting_lbl = tk.Label(profile_frame, text="Hello,\nCamille", font=("Segoe UI", 11, "bold"), bg=self.bg_sidebar, fg=self.text_light, justify="left")
        greeting_lbl.pack(side="left")
        
        sep = tk.Frame(parent, bg=self.border_color, height=1)
        sep.pack(fill="x", padx=15, pady=10)
        
        nav_label = tk.Label(parent, text="NAVIGATION", font=("Segoe UI", 8, "bold"), bg=self.bg_sidebar, fg=self.text_muted)
        nav_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        nav_items = ["Overview", "Shipments", "Clients", "Analytics", "History", "Settings"]
        
        for name in nav_items:
            btn = tk.Button(parent, text=name, font=("Segoe UI", 10), bg=self.bg_sidebar, fg=self.text_light, 
                            activebackground=self.card_bg, activeforeground=self.accent_cyan,
                            bd=0, anchor="w", padx=20, pady=8, cursor="hand2",
                            command=lambda n=name: self.switch_view(n))
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[name] = btn

    def switch_view(self, view_name):
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.config(bg=self.card_bg, fg=self.accent_cyan)
            else:
                btn.config(bg=self.bg_sidebar, fg=self.text_light)
                
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
        if view_name == "Overview":
            self.render_overview_view()
        elif view_name == "Shipments":
            self.render_shipments_view()
        elif view_name == "Clients":
            self.render_clients_view()
        elif view_name == "Analytics":
            self.render_analytics_view()
        elif view_name == "History":
            self.render_history_view()
        elif view_name == "Settings":
            self.render_settings_view()

    def render_overview_view(self):
        header_frame = tk.Frame(self.main_content, bg=self.bg_dark)
        header_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(header_frame, text="Logistics Tracking & Operations", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        controls_frame = tk.Frame(header_frame, bg=self.bg_dark)
        controls_frame.pack(side="right")
        
        # Fully functional truck dropdown mapping
        self.truck_var = tk.StringVar(value="Select a Truck")
        truck_cb = ttk.Combobox(controls_frame, textvariable=self.truck_var, values=["All Trucks", "Truck 12", "Truck 08", "Truck 04"], width=16, state="readonly")
        truck_cb.pack(side="left", padx=5)
        truck_cb.bind("<<ComboboxSelected>>", self.on_truck_dropdown_select)
        
        self.search_ent = tk.Entry(controls_frame, bg=self.card_bg, fg=self.text_light, insertbackground=self.text_light, font=("Segoe UI", 9), width=15, bd=0)
        self.search_ent.insert(0, "Search...")
        self.search_ent.pack(side="left", padx=5, ipady=4)
        self.search_ent.bind("<KeyRelease>", self.filter_overview_data)
        
        # Fully functional notification bell button
        bell_btn = tk.Button(controls_frame, text="🔔", font=("Segoe UI", 11), bg=self.card_bg, fg=self.text_light, bd=0, padx=6, pady=2, cursor="hand2", command=self.show_notifications)
        bell_btn.pack(side="left", padx=5)
        
        status_frame = tk.Frame(self.main_content, bg=self.bg_dark)
        status_frame.pack(fill="x", pady=(0, 12))
        
        for text, color in [("In Delivery", self.accent_rose), ("Pending", "#f59e0b"), ("Completed", self.accent_emerald)]:
            btn = tk.Button(status_frame, text=text, font=("Segoe UI", 9, "bold"), bg=color, fg="#ffffff", bd=0, padx=10, pady=2, cursor="hand2",
                            command=lambda t=text: self.filter_by_status(t))
            btn.pack(side="left", padx=(0, 8))
            
        grid_frame = tk.Frame(self.main_content, bg=self.bg_dark)
        grid_frame.pack(fill="both", expand=True)
        
        left_col = tk.Frame(grid_frame, bg=self.bg_dark)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        right_col = tk.Frame(grid_frame, bg=self.bg_dark)
        right_col.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        prog_card = tk.Frame(left_col, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        prog_card.pack(fill="x", pady=(0, 10), ipady=8, ipadx=10)
        
        tk.Label(prog_card, text="Global Progression", font=("Segoe UI", 10, "bold"), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=10, pady=(5, 2))
        
        prog_info = tk.Frame(prog_card, bg=self.card_bg)
        prog_info.pack(fill="x", padx=10, pady=2)
        tk.Label(prog_info, text="72%", font=("Segoe UI", 20, "bold"), bg=self.card_bg, fg=self.accent_rose).pack(side="left")
        
        stats_sub = tk.Frame(prog_info, bg=self.card_bg)
        stats_sub.pack(side="right")
        tk.Label(stats_sub, text="📍 Distance covered: 540 km", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_muted).pack(anchor="e")
        tk.Label(stats_sub, text="⏱ Remaining time: 1h 20 min", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_light).pack(anchor="e")
        
        canvas_bar = tk.Canvas(prog_card, bg=self.bg_dark, height=6, highlightthickness=0)
        canvas_bar.pack(fill="x", padx=10, pady=6)
        canvas_bar.create_rectangle(0, 0, int(450 * 0.72), 6, fill=self.accent_rose, width=0)
        
        alert_card = tk.Frame(left_col, bg=self.card_bg, highlightbackground=self.accent_rose, highlightthickness=1)
        alert_card.pack(fill="x", pady=(0, 10), ipady=6, ipadx=10)
        tk.Label(alert_card, text="🚨 Live Traffic Alerts", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.accent_rose).pack(anchor="w", padx=10)
        tk.Label(alert_card, text="Slowdown expected: Heavy congestion in primary delivery corridor.", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=10, pady=(2, 4))
        
        self.ship_card_frame = tk.Frame(left_col, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        self.ship_card_frame.pack(fill="x", pady=(0, 10), ipady=8, ipadx=10)
        self.load_active_shipment_details()

        cap_card = tk.Frame(right_col, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        cap_card.pack(fill="x", pady=(0, 10), ipady=8, ipadx=10)
        tk.Label(cap_card, text="Truck Capacity Management", font=("Segoe UI", 10, "bold"), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=10, pady=(5, 2))
        
        cap_sub = tk.Frame(cap_card, bg=self.card_bg)
        cap_sub.pack(fill="x", padx=10, pady=2)
        tk.Label(cap_sub, text="78% used", font=("Segoe UI", 16, "bold"), bg=self.card_bg, fg=self.accent_emerald).pack(side="left")
        tk.Label(cap_sub, text="Load: 14.2 t / 18.0 t max", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_muted).pack(side="right", pady=4)
        
        canvas_cap = tk.Canvas(cap_card, bg=self.bg_dark, height=6, highlightthickness=0)
        canvas_cap.pack(fill="x", padx=10, pady=6)
        canvas_cap.create_rectangle(0, 0, int(420 * 0.78), 6, fill=self.accent_emerald, width=0)

        chart_card = tk.Frame(right_col, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        chart_card.pack(fill="both", expand=True, pady=(0, 10), ipadx=5, ipady=5)
        
        chart_header = tk.Frame(chart_card, bg=self.card_bg)
        chart_header.pack(fill="x", padx=10, pady=4)
        tk.Label(chart_header, text="Shipment Volume Trends", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.text_light).pack(side="left")
        tk.Label(chart_header, text="On-Time Rate: 94%", font=("Segoe UI", 8, "bold"), bg=self.card_bg, fg=self.accent_emerald).pack(side="right")
        
        fig, ax = plt.subplots(figsize=(4.5, 1.5), dpi=100)
        fig.patch.set_facecolor('#1e293b')
        ax.set_facecolor('#1e293b')
        days = ['May 19', 'May 20', 'May 21', 'May 22', 'May 23', 'May 24', 'May 25']
        volumes = [65, 70, 58, 82, 75, 90, 85]
        ax.plot(days, volumes, color='#06b6d4', marker='o', linewidth=2, markersize=3)
        ax.tick_params(colors='#94a3b8', labelsize=7)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.grid(True, color='#334155', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=2)

    def show_notifications(self):
        messagebox.showinfo("System Notifications", "🔔 Active Alerts:\n- Heavy traffic detected in Sector 4.\n- Truck 12 operating at 78% capacity[cite: 1].\n- All telemetry links online.")

    def on_truck_dropdown_select(self, event):
        val = self.truck_var.get()
        if val == "All Trucks":
            self.selected_truck_filter = None
        else:
            self.selected_truck_filter = val
        self.load_active_shipment_details()

    def load_active_shipment_details(self, search_query=None, status_filter=None):
        for widget in self.ship_card_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.ship_card_frame, text="Active Driver & Fleet Assignment", font=("Segoe UI", 10, "bold"), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=10, pady=(5, 2))
        
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        query = "SELECT driver_name, truck_id, shipment_code, status, parcels, delivery_date FROM shipments WHERE 1=1"
        params = []
        
        if self.selected_truck_filter:
            query += " AND truck_id LIKE ?"
            params.append(f"%{self.selected_truck_filter}%")
            
        if search_query and search_query != "Search...":
            query += " AND (driver_name LIKE ? OR shipment_code LIKE ? OR truck_id LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
            
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            tk.Label(self.ship_card_frame, text="No matching assignments found for this filter.", font=("Segoe UI", 9), bg=self.card_bg, fg=self.text_muted).pack(padx=10, pady=10)
            return
            
        row = rows[0]
        driver_row = tk.Frame(self.ship_card_frame, bg=self.card_bg)
        driver_row.pack(fill="x", padx=10, pady=2)
        tk.Label(driver_row, text=f"👨‍✈️ Driver: {row[0]}", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.text_light).pack(side="left")
        tk.Label(driver_row, text=f"🚛 Assigned: {row[1]}", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.accent_cyan).pack(side="right")
        
        ship_stats = tk.Frame(self.ship_card_frame, bg=self.card_bg)
        ship_stats.pack(fill="x", padx=10, pady=6)
        tk.Label(ship_stats, text=f"📦 Code: {row[2]} ({row[4]} parcels)", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_light).pack(side="left")
        tk.Label(ship_stats, text=f"Status: {row[3]} | Due: {row[5]}", font=("Segoe UI", 8), bg=self.card_bg, fg=self.text_muted).pack(side="right")

    def filter_overview_data(self, event):
        self.load_active_shipment_details(search_query=self.search_ent.get())

    def filter_by_status(self, status):
        self.load_active_shipment_details(status_filter=status)

    def render_shipments_view(self):
        header_frame = tk.Frame(self.main_content, bg=self.bg_dark)
        header_frame.pack(fill="x", pady=(0, 15))
        tk.Label(header_frame, text="Shipments Management & Driver Assignments", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        tk.Button(header_frame, text="+ Add New Shipment", font=("Segoe UI", 9, "bold"), bg=self.accent_cyan, fg=self.bg_dark, bd=0, padx=12, pady=6, cursor="hand2", command=self.open_add_shipment_popup).pack(side="right")
        
        table_frame = tk.Frame(self.main_content, bg=self.card_bg)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Driver Name", "Assigned Truck", "Code", "Status", "Parcels", "Delivery Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
            
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.load_shipments_table_data()

    def load_shipments_table_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, driver_name, truck_id, shipment_code, status, parcels, delivery_date FROM shipments")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def open_add_shipment_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Assign Driver & Add Shipment")
        popup.geometry("400x380")
        popup.configure(bg=self.card_bg)
        
        tk.Label(popup, text="New Shipment & Driver Mapping", font=("Segoe UI", 12, "bold"), bg=self.card_bg, fg=self.text_light).pack(pady=10)
        
        fields = [("Driver Name:", "driver_ent"), ("Assigned Truck:", "truck_ent"), ("Shipment Code:", "code_ent"), ("Status (In Delivery/Pending/Completed):", "status_ent"), ("Parcels Count:", "parcels_ent"), ("Delivery Date:", "date_ent")]
        entries = {}
        for label_text, key in fields:
            f = tk.Frame(popup, bg=self.card_bg)
            f.pack(fill="x", padx=20, pady=4)
            tk.Label(f, text=label_text, font=("Segoe UI", 9), bg=self.card_bg, fg=self.text_muted, width=22, anchor="w").pack(side="left")
            ent = tk.Entry(f, bg=self.bg_dark, fg=self.text_light, insertbackground=self.text_light, font=("Segoe UI", 9))
            ent.pack(side="right", fill="x", expand=True)
            entries[key] = ent
            
        def save():
            try:
                conn = sqlite3.connect("logistics.db")
                cursor = conn.cursor()
                cursor.execute('INSERT INTO shipments (driver_name, truck_id, shipment_code, status, progress, load_current, load_max, delivery_date, parcels) VALUES (?, ?, ?, ?, 50, 12.0, 18.0, ?, ?)',
                               (entries["driver_ent"].get(), entries["truck_ent"].get(), entries["code_ent"].get(), entries["status_ent"].get(), entries["date_ent"].get(), int(entries["parcels_ent"].get())))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Shipment & driver mapping added successfully!")
                popup.destroy()
                self.load_shipments_table_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(popup, text="Save Record", font=("Segoe UI", 10, "bold"), bg=self.accent_emerald, fg="#ffffff", bd=0, padx=15, pady=6, command=save).pack(pady=15)

    def render_clients_view(self):
        header = tk.Frame(self.main_content, bg=self.bg_dark)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(header, text="Client Management & Accounts", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        btn_frame = tk.Frame(header, bg=self.bg_dark)
        btn_frame.pack(side="right")
        
        tk.Button(btn_frame, text="+ Add Client", font=("Segoe UI", 9, "bold"), bg=self.accent_cyan, fg=self.bg_dark, bd=0, padx=10, pady=5, cursor="hand2", command=self.open_add_client_popup).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", font=("Segoe UI", 9, "bold"), bg=self.accent_rose, fg="#ffffff", bd=0, padx=10, pady=5, cursor="hand2", command=self.delete_client).pack(side="left", padx=5)
        
        table_frame = tk.Frame(self.main_content, bg=self.card_bg)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Company Name", "Contact Person", "Email Address", "Active Orders")
        self.client_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for col in columns:
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=160, anchor="center")
        self.client_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.load_clients_table_data()

    def load_clients_table_data(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        for row in cursor.fetchall():
            self.client_tree.insert("", "end", values=row)
        conn.close()

    def open_add_client_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Client")
        popup.geometry("380x300")
        popup.configure(bg=self.card_bg)
        
        tk.Label(popup, text="New Client Account", font=("Segoe UI", 12, "bold"), bg=self.card_bg, fg=self.text_light).pack(pady=10)
        
        fields = [("Company Name:", "comp_ent"), ("Contact Person:", "contact_ent"), ("Email Address:", "email_ent"), ("Active Orders:", "orders_ent")]
        entries = {}
        for label_text, key in fields:
            f = tk.Frame(popup, bg=self.card_bg)
            f.pack(fill="x", padx=20, pady=4)
            tk.Label(f, text=label_text, font=("Segoe UI", 9), bg=self.card_bg, fg=self.text_muted, width=16, anchor="w").pack(side="left")
            ent = tk.Entry(f, bg=self.bg_dark, fg=self.text_light, insertbackground=self.text_light, font=("Segoe UI", 9))
            ent.pack(side="right", fill="x", expand=True)
            entries[key] = ent
            
        def save():
            try:
                conn = sqlite3.connect("logistics.db")
                cursor = conn.cursor()
                cursor.execute('INSERT INTO clients (company_name, contact_person, email, active_orders) VALUES (?, ?, ?, ?)',
                               (entries["comp_ent"].get(), entries["contact_ent"].get(), entries["email_ent"].get(), int(entries["orders_ent"].get())))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Client added successfully!")
                popup.destroy()
                self.load_clients_table_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(popup, text="Save Client", font=("Segoe UI", 10, "bold"), bg=self.accent_emerald, fg="#ffffff", bd=0, padx=15, pady=6, command=save).pack(pady=15)

    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a client to delete.")
            return
        item_vals = self.client_tree.item(selected[0], "values")
        client_id = item_vals[0]
        
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Client removed successfully.")
        self.load_clients_table_data()

    def render_analytics_view(self):
        header = tk.Frame(self.main_content, bg=self.bg_dark)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(header, text="Fleet Analytics & Performance Metrics", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        card = tk.Frame(self.main_content, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(card, text="Weekly On-Time Delivery Performance vs Target (90%)", font=("Segoe UI", 11, "bold"), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=20, pady=15)
        
        fig, ax = plt.subplots(figsize=(8, 3.5), dpi=100)
        fig.patch.set_facecolor('#1e293b')
        ax.set_facecolor('#1e293b')
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        performance = [91, 89, 95, 94]
        ax.bar(weeks, performance, color='#06b6d4', width=0.4)
        ax.axhline(y=90, color='#f43f5e', linestyle='--', label='Target (90%)')
        ax.tick_params(colors='#94a3b8', labelsize=9)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#f8fafc')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

    def render_history_view(self):
        header = tk.Frame(self.main_content, bg=self.bg_dark)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(header, text="Historical Completed Deliveries", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        table_frame = tk.Frame(self.main_content, bg=self.card_bg)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Trip Code", "Driver", "Truck", "Completion Date", "Status")
        hist_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for col in columns:
            hist_tree.heading(col, text=col)
            hist_tree.column(col, width=150, anchor="center")
        hist_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history_logs")
        for row in cursor.fetchall():
            hist_tree.insert("", "end", values=row)
        conn.close()

    def render_settings_view(self):
        header = tk.Frame(self.main_content, bg=self.bg_dark)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(header, text="System Configurations & Preferences", font=("Segoe UI", 18, "bold"), bg=self.bg_dark, fg=self.text_light).pack(side="left")
        
        card = tk.Frame(self.main_content, bg=self.card_bg, highlightbackground=self.border_color, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(card, text="Preferences & Dispatch Options", font=("Segoe UI", 12, "bold"), bg=self.card_bg, fg=self.text_light).pack(anchor="w", padx=25, pady=20)
        
        var1 = tk.BooleanVar(value=True)
        var2 = tk.BooleanVar(value=True)
        
        tk.Checkbutton(card, text=" Enable Real-Time Traffic Alerts & Slowdown Warnings", variable=var1, bg=self.card_bg, fg=self.text_light, selectcolor=self.bg_dark, activebackground=self.card_bg, activeforeground=self.text_light).pack(anchor="w", padx=25, pady=8)
        tk.Checkbutton(card, text=" Auto-Sync Driver Telemetry with SQLite Database", variable=var2, bg=self.card_bg, fg=self.text_light, selectcolor=self.bg_dark, activebackground=self.card_bg, activeforeground=self.text_light).pack(anchor="w", padx=25, pady=8)
        
        def save_settings():
            messagebox.showinfo("Settings Saved", "Preferences updated successfully!")
            
        tk.Button(card, text="Save Settings", font=("Segoe UI", 10, "bold"), bg=self.accent_emerald, fg="#ffffff", bd=0, padx=15, pady=6, command=save_settings).pack(anchor="w", padx=25, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticsDashboard(root)
    root.mainloop()