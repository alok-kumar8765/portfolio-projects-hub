import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# -----------------------------------------------------------------------------
# DATABASE SETUP & UTILS (SQLite)
# -----------------------------------------------------------------------------
DB_NAME = "event_db.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            event_name TEXT,
            event_date TEXT,
            location TEXT,
            price REAL,
            seats INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT,
            customer_name TEXT,
            quantity INTEGER,
            booking_date TEXT,
            status TEXT DEFAULT 'Confirmed'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)
    
    # Insert sample data if events table is empty
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:
        sample_events = [
            ("EVT001", "Music Concert", "2026-11-15", "New York, USA", 50.00, 120),
            ("EVT002", "Tech Festival", "2026-11-20", "San Francisco, USA", 75.00, 95),
            ("EVT003", "Food Carnival", "2026-11-25", "Chicago, USA", 30.00, 160),
            ("EVT004", "Business Expo", "2026-12-05", "Los Angeles, USA", 100.00, 80),
            ("EVT005", "AI & Data Seminar", "2026-12-10", "Seattle, USA", 40.00, 140)
        ]
        cur.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", sample_events)
        
        sample_customers = [
            ("Alice Smith", "alice@example.com", "555-0101"),
            ("Bob Jones", "bob@example.com", "555-0192"),
            ("Charlie Brown", "charlie@example.com", "555-0143")
        ]
        cur.executemany("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", sample_customers)

        sample_bookings = [
            ("EVT001", "Alice Smith", 2, "2026-11-01 10:30:00", "Confirmed"),
            ("EVT002", "Bob Jones", 1, "2026-11-02 14:15:00", "Confirmed"),
            ("EVT003", "Charlie Brown", 4, "2026-11-03 09:00:00", "Pending")
        ]
        cur.executemany("INSERT INTO bookings (event_id, customer_name, quantity, booking_date, status) VALUES (?, ?, ?, ?, ?)", sample_bookings)
        con.commit()
    con.close()

# -----------------------------------------------------------------------------
# THEMES CONFIGURATION
# -----------------------------------------------------------------------------
THEMES = {
    "Modern Dark": {
        "bg": "#1e1e2f",
        "fg": "#ffffff",
        "card_bg": "#2b2b40",
        "sidebar_bg": "#151522",
        "accent": "#6c5ce7",
        "hover": "#8075e8",
        "text_secondary": "#a4b0be",
        "table_bg": "#2b2b40",
        "table_fg": "#ffffff"
    },
    "Light Clean": {
        "bg": "#f4f7f6",
        "fg": "#2c3e50",
        "card_bg": "#ffffff",
        "sidebar_bg": "#2c3e50",
        "accent": "#3498db",
        "hover": "#2980b9",
        "text_secondary": "#7f8c8d",
        "table_bg": "#ffffff",
        "table_fg": "#2c3e50"
    },
    "Cyberpunk": {
        "bg": "#0f051d",
        "fg": "#00ffcc",
        "card_bg": "#1b0a33",
        "sidebar_bg": "#080211",
        "accent": "#ff007f",
        "hover": "#ff3399",
        "text_secondary": "#b366ff",
        "table_bg": "#1b0a33",
        "table_fg": "#00ffcc"
    }
}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Event & Ticket Booking System")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        frame = tk.Frame(self.root, bg="#1e1e2f", padx=30, pady=30)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="🎫 EventHub Login", bg="#1e1e2f", fg="#ffffff", font=("Arial", 16, "bold")).pack(pady=15)

        tk.Label(frame, text="Username:", bg="#1e1e2f", fg="#a4b0be", font=("Arial", 10)).pack(anchor="w")
        self.user_entry = tk.Entry(frame, font=("Arial", 11), width=30)
        self.user_entry.pack(pady=5, ipady=3)
        self.user_entry.insert(0, "admin")

        tk.Label(frame, text="Password:", bg="#1e1e2f", fg="#a4b0be", font=("Arial", 10)).pack(anchor="w")
        self.pass_entry = tk.Entry(frame, font=("Arial", 11), width=30, show="*")
        self.pass_entry.pack(pady=5, ipady=3)
        self.pass_entry.insert(0, "admin")

        tk.Button(frame, text="Login", bg="#6c5ce7", fg="#ffffff", font=("Arial", 11, "bold"), relief=tk.FLAT, width=25, command=self.authenticate).pack(pady=20)

    def authenticate(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if u == "admin" and p == "admin":
            self.root.destroy()
            main_root = tk.Tk()
            EventBookingApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password! (Use admin/admin)")


class EventBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event & Ticket Booking System")
        self.root.geometry("1280x720")
        self.current_theme = "Modern Dark"
        
        init_db()
        self.create_widgets()

    def apply_theme(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        t = THEMES[self.current_theme]
        self.root.configure(bg=t["bg"])
        
        # Main Container
        self.main_container = tk.Frame(self.root, bg=t["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # ---------------- SIDEBAR ----------------
        self.sidebar = tk.Frame(self.main_container, bg=t["sidebar_bg"], width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        logo_lbl = tk.Label(self.sidebar, text="🎫 EventHub", bg=t["sidebar_bg"], fg="#ffffff", font=("Arial", 16, "bold"))
        logo_lbl.pack(pady=20)

        nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("📅 Events", self.show_events),
            ("🎫 Book Ticket", self.show_book_ticket),
            ("📋 My Bookings", self.show_bookings),
            ("👥 Customers", self.show_customers),
            ("📈 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings),
        ]

        for text, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=text, bg=t["sidebar_bg"], fg="#ffffff", activebackground=t["accent"],
                            activeforeground="#ffffff", relief=tk.FLAT, anchor="w", padx=20, font=("Arial", 11), command=cmd)
            btn.pack(fill=tk.X, pady=4)

        # Logout Button
        logout_btn = tk.Button(self.sidebar, text="🚪 Logout", bg=t["sidebar_bg"], fg="#ff5252", activebackground="#ff5252",
                               activeforeground="#ffffff", relief=tk.FLAT, anchor="w", padx=20, font=("Arial", 11), command=self.logout)
        logout_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Theme selector in sidebar
        theme_frame = tk.Frame(self.sidebar, bg=t["sidebar_bg"])
        theme_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X, padx=10)
        tk.Label(theme_frame, text="Theme:", bg=t["sidebar_bg"], fg=t["text_secondary"], font=("Arial", 9)).pack(anchor="w")
        
        self.theme_combo = ttk.Combobox(theme_frame, values=list(THEMES.keys()), state="readonly")
        self.theme_combo.set(self.current_theme)
        self.theme_combo.pack(fill=tk.X, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # ---------------- CONTENT AREA ----------------
        self.content_area = tk.Frame(self.main_container, bg=t["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header banner
        header_frame = tk.Frame(self.content_area, bg=t["card_bg"], height=65)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Event & Ticket Booking System", bg=t["card_bg"], fg=t["fg"], font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        # Footer (Generative AI & Copyright)
        footer_frame = tk.Frame(self.content_area, bg=t["bg"], height=30)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(footer_frame, text="Creator: Generative AI | Copyrights 2026", bg=t["bg"], fg=t["text_secondary"], font=("Arial", 9)).pack(side=tk.RIGHT, padx=15)

        # Load Dashboard by default
        self.show_dashboard()

    def change_theme(self, event):
        self.current_theme = self.theme_combo.get()
        self.apply_theme()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()

    def clear_content(self):
        for w in self.content_area.winfo_children():
            if w.winfo_y() > 60 and w.winfo_y() < 660:
                w.destroy()

    def get_stats_data(self):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM events")
        ev_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM bookings")
        bk_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM customers")
        cust_count = cur.fetchone()[0]
        cur.execute("SELECT SUM(b.quantity * e.price) FROM bookings b JOIN events e ON b.event_id = e.event_id WHERE b.status='Confirmed'")
        rev = cur.fetchone()[0]
        con.close()
        return str(ev_count), str(bk_count), str(cust_count), f"${rev:,.2f}" if rev else "$0.00"

    def show_dashboard(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        
        dash_frame = tk.Frame(self.content_area, bg=t["bg"])
        dash_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        ev_c, bk_c, cust_c, rev_val = self.get_stats_data()

        # Stat Cards
        cards_frame = tk.Frame(dash_frame, bg=t["bg"])
        cards_frame.pack(fill=tk.X, pady=5)

        stats = [
            ("Total Events", ev_c, "#3498db"),
            ("Total Bookings", bk_c, "#2ecc71"),
            ("Total Customers", cust_c, "#e67e22"),
            ("Total Revenue", rev_val, "#9b59b6")
        ]

        for title, val, color in stats:
            card = tk.Frame(cards_frame, bg=color, width=220, height=80)
            card.pack(side=tk.LEFT, padx=8, expand=True, fill=tk.X)
            card.pack_propagate(False)
            tk.Label(card, text=title, bg=color, fg="#ffffff", font=("Arial", 10)).pack(anchor="w", padx=12, pady=6)
            tk.Label(card, text=val, bg=color, fg="#ffffff", font=("Arial", 16, "bold")).pack(anchor="w", padx=12)

        # Charts Section (Canvas mockups matching reference design)
        charts_frame = tk.Frame(dash_frame, bg=t["bg"])
        charts_frame.pack(fill=tk.X, pady=10)

        # Left Chart: Bookings by Event Bar Chart
        bar_card = tk.Frame(charts_frame, bg=t["card_bg"], height=160)
        bar_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        bar_card.pack_propagate(False)
        tk.Label(bar_card, text="Bookings by Event", bg=t["card_bg"], fg=t["fg"], font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        canvas_bar = tk.Canvas(bar_card, bg=t["card_bg"], highlightthickness=0, height=110)
        canvas_bar.pack(fill=tk.BOTH, expand=True, padx=10)
        # Draw bars
        bars = [("Concert", 112, "#9b59b6"), ("Tech Fest", 98, "#3498db"), ("Food Fest", 76, "#e67e22"), ("Expo", 54, "#2ecc71"), ("Seminar", 46, "#e74c3c")]
        x_start = 30
        for name, val, col in bars:
            canvas_bar.create_rectangle(x_start, 100 - val*0.7, x_start + 30, 100, fill=col)
            canvas_bar.create_text(x_start + 15, 108, text=name, fill=t["text_secondary"], font=("Arial", 8))
            canvas_bar.create_text(x_start + 15, 90 - val*0.7, text=str(val), fill=t["fg"], font=("Arial", 8, "bold"))
            x_start += 75

        # Right Chart: Booking Status Donut Chart / Legend
        pie_card = tk.Frame(charts_frame, bg=t["card_bg"], height=160, width=320)
        pie_card.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        pie_card.pack_propagate(False)
        tk.Label(pie_card, text="Booking Status", bg=t["card_bg"], fg=t["fg"], font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        canvas_pie = tk.Canvas(pie_card, bg=t["card_bg"], highlightthickness=0, width=120, height=110)
        canvas_pie.pack(side=tk.LEFT, padx=10)
        # Draw Donut slices roughly
        canvas_pie.create_arc(10, 10, 110, 110, start=0, extent=295, fill="#2ecc71", outline="")
        canvas_pie.create_arc(10, 10, 110, 110, start=295, extent=41, fill="#f1c40f", outline="")
        canvas_pie.create_arc(10, 10, 110, 110, start=336, extent=24, fill="#e74c3c", outline="")
        canvas_pie.create_oval(35, 35, 85, 85, fill=t["card_bg"], outline="")
        canvas_pie.create_text(60, 60, text="486\nTotal", fill=t["fg"], font=("Arial", 8, "bold"), justify="center")

        legend_frame = tk.Frame(pie_card, bg=t["card_bg"])
        legend_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(legend_frame, text="🟢 Confirmed (82.1%)", bg=t["card_bg"], fg=t["fg"], font=("Arial", 9)).pack(anchor="w", pady=4)
        tk.Label(legend_frame, text="🟡 Pending (11.5%)", bg=t["card_bg"], fg=t["fg"], font=("Arial", 9)).pack(anchor="w", pady=4)
        tk.Label(legend_frame, text="🔴 Cancelled (6.4%)", bg=t["card_bg"], fg=t["fg"], font=("Arial", 9)).pack(anchor="w", pady=4)

        # Upcoming Events Table
        table_frame = tk.Frame(dash_frame, bg=t["card_bg"])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(table_frame, text="Upcoming Events", bg=t["card_bg"], fg=t["fg"], font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=5)

        columns = ("Event ID", "Event Name", "Date", "Location", "Price", "Seats")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT event_id, event_name, event_date, location, price, seats FROM events")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], f"${row[4]:.2f}", row[5]))
        con.close()

        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    def show_events(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(f, text="Event Management Module", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        # Form to add event
        form_f = tk.Frame(f, bg=t["card_bg"], padx=15, pady=15)
        form_f.pack(fill=tk.X, pady=5)
        
        tk.Label(form_f, text="ID:", bg=t["card_bg"], fg=t["fg"]).grid(row=0, column=0, sticky="w")
        e_id = tk.Entry(form_f, width=10)
        e_id.grid(row=0, column=1, padx=5)
        e_id.insert(0, "EVT006")

        tk.Label(form_f, text="Name:", bg=t["card_bg"], fg=t["fg"]).grid(row=0, column=2, sticky="w")
        e_name = tk.Entry(form_f, width=18)
        e_name.grid(row=0, column=3, padx=5)

        tk.Label(form_f, text="Date:", bg=t["card_bg"], fg=t["fg"]).grid(row=0, column=4, sticky="w")
        e_date = tk.Entry(form_f, width=12)
        e_date.grid(row=0, column=5, padx=5)
        e_date.insert(0, "2026-12-15")

        tk.Label(form_f, text="Price:", bg=t["card_bg"], fg=t["fg"]).grid(row=0, column=6, sticky="w")
        e_price = tk.Entry(form_f, width=8)
        e_price.grid(row=0, column=7, padx=5)

        def save_event():
            try:
                con = get_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", 
                            (e_id.get(), e_name.get(), e_date.get(), "New York, USA", float(e_price.get() or 50), 100))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Event Added Successfully!")
                self.show_events()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        tk.Button(form_f, text="Add Event", bg=t["accent"], fg="#ffffff", relief=tk.FLAT, padx=10, command=save_event).grid(row=0, column=8, padx=10)

        # Table of events
        columns = ("Event ID", "Event Name", "Date", "Location", "Price", "Seats")
        tree = ttk.Treeview(f, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM events")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        con.close()
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def show_book_ticket(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(f, text="Online Ticket Booking", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        form = tk.Frame(f, bg=t["card_bg"], padx=30, pady=30)
        form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT event_id, event_name FROM events")
        events_list = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
        con.close()

        tk.Label(form, text="Select Event:", bg=t["card_bg"], fg=t["fg"], font=("Arial", 11)).pack(anchor="w", pady=5)
        ev_combo = ttk.Combobox(form, values=events_list, width=40, state="readonly")
        if events_list: ev_combo.set(events_list[0])
        ev_combo.pack(anchor="w", pady=5)

        tk.Label(form, text="Customer Name:", bg=t["card_bg"], fg=t["fg"], font=("Arial", 11)).pack(anchor="w", pady=5)
        cust_entry = tk.Entry(form, width=43, font=("Arial", 11))
        cust_entry.pack(anchor="w", pady=5)

        tk.Label(form, text="Ticket Quantity:", bg=t["card_bg"], fg=t["fg"], font=("Arial", 11)).pack(anchor="w", pady=5)
        qty_spin = ttk.Spinbox(form, from_=1, to=10, width=41)
        qty_spin.pack(anchor="w", pady=5)
        qty_spin.set(1)

        def book_action():
            try:
                ev_id = ev_combo.get().split(" - ")[0]
                c_name = cust_entry.get().strip()
                qty = int(qty_spin.get())
                if not c_name:
                    messagebox.showerror("Error", "Please enter customer name!")
                    return
                con = get_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO bookings (event_id, customer_name, quantity, booking_date, status) VALUES (?, ?, ?, ?, ?)",
                            (ev_id, c_name, qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Confirmed"))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Ticket Booked Successfully!")
                self.show_bookings()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        tk.Button(form, text="Confirm & Book Ticket", bg=t["accent"], fg="#ffffff", font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=8, command=book_action).pack(anchor="w", pady=20)

    def show_bookings(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        top_bar = tk.Frame(f, bg=t["bg"])
        top_bar.pack(fill=tk.X, pady=5)
        tk.Label(top_bar, text="Booking Status & Tracking", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        def confirm_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select", "Please select a booking to update!")
                return
            b_id = tree.item(selected[0])['values'][0]
            con = get_connection()
            cur = con.cursor()
            cur.execute("UPDATE bookings SET status='Confirmed' WHERE booking_id=?", (b_id,))
            con.commit()
            con.close()
            messagebox.showinfo("Success", f"Booking #{b_id} Confirmed!")
            self.show_bookings()

        tk.Button(top_bar, text="Mark Confirmed", bg="#2ecc71", fg="#ffffff", relief=tk.FLAT, command=confirm_selected).pack(side=tk.RIGHT)

        columns = ("Booking ID", "Event ID", "Customer Name", "Quantity", "Booking Date", "Status")
        tree = ttk.Treeview(f, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookings")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        con.close()
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def show_customers(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(f, text="Customer Directory", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        columns = ("Customer ID", "Full Name", "Email", "Phone")
        tree = ttk.Treeview(f, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor="center")
        
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM customers")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)
        con.close()
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def show_reports(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(f, text="Revenue Analytics & Financial Reports", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        card = tk.Frame(f, bg=t["card_bg"], padx=25, pady=25)
        card.pack(fill=tk.BOTH, expand=True, pady=10)

        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT SUM(b.quantity * e.price) FROM bookings b JOIN events e ON b.event_id = e.event_id WHERE b.status='Confirmed'")
        tot_rev = cur.fetchone()[0] or 0.0
        cur.execute("SELECT COUNT(*) FROM bookings")
        tot_bk = cur.fetchone()[0]
        con.close()

        tk.Label(card, text=f"Total Gross Revenue: ${tot_rev:,.2f}", bg=t["card_bg"], fg="#2ecc71", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)
        tk.Label(card, text=f"Total Processed Bookings: {tot_bk}", bg=t["card_bg"], fg=t["fg"], font=("Arial", 12)).pack(anchor="w", pady=5)
        tk.Label(card, text="Report generated successfully via SQLite database engine.", bg=t["card_bg"], fg=t["text_secondary"], font=("Arial", 10)).pack(anchor="w", pady=15)

    def show_settings(self):
        self.clear_content()
        t = THEMES[self.current_theme]
        f = tk.Frame(self.content_area, bg=t["bg"])
        f.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(f, text="System Settings", bg=t["bg"], fg=t["fg"], font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        card = tk.Frame(f, bg=t["card_bg"], padx=20, pady=20)
        card.pack(fill=tk.X, pady=10)
        
        tk.Label(card, text="Database Engine: SQLite (Local File: event_db.sqlite)", bg=t["card_bg"], fg="#2ecc71", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)
        tk.Label(card, text="App Version: v2.6.0 Enterprise", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w", pady=5)
        tk.Label(card, text="Theme Engine: Active Multi-Theme Support", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w", pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()