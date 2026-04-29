import tkinter as tk
from tkinter import ttk
from assets.styles import *
from datetime import datetime

class DashboardView:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        header = tk.Frame(self.container, bg=COLORS['light'])
        header.pack(fill='x', pady=(0, 20))

        tk.Label(
            header,
            text="Dashboard",
            font=FONTS['title'],
            bg=COLORS['light'],
            fg=COLORS['primary']
        ).pack(side='left')

        tk.Button(
            header,
            text="Refresh",
            **BUTTON_STYLE,
            command=self.refresh_dashboard
        ).pack(side='right')

        stats_frame = tk.Frame(self.container, bg=COLORS['light'])
        stats_frame.pack(fill='x', pady=(0, 20))

        stats = self.controller.get_dashboard_stats()

        stats_data = [
            ("Total Rooms", stats['total_rooms'], COLORS['primary']),
            ("Occupied", stats['occupied_rooms'], COLORS['success']),
            ("Available", stats['available_rooms'], COLORS['secondary']),
            ("Active Tenants", stats['active_tenants'], COLORS['warning']),
        ]

        for i, (label, value, color) in enumerate(stats_data):
            self.create_stat_card(stats_frame, label, value, color, i)

        financial_frame = tk.LabelFrame(
            self.container,
            text="Financial Summary",
            font=FONTS['heading'],
            bg=COLORS['light'],
            fg=COLORS['primary'],
            padx=15,
            pady=15
        )
        financial_frame.pack(fill='x', pady=(0, 20))

        fin_grid = tk.Frame(financial_frame, bg=COLORS['light'])
        fin_grid.pack(fill='x')

        financial_data = [
            ("Total Income:", f"₱{stats['total_income']:,.2f}", COLORS['success']),
            ("Total Expenses:", f"₱{stats['total_expenses']:,.2f}", COLORS['danger']),
            ("Net Income:", f"₱{stats['net_income']:,.2f}", COLORS['primary']),
            ("Monthly Income:", f"₱{stats['monthly_income']:,.2f}", COLORS['success']),
            ("Monthly Expenses:", f"₱{stats['monthly_expenses']:,.2f}", COLORS['danger']),
            ("Monthly Net:", f"₱{stats['monthly_net']:,.2f}", COLORS['primary']),
        ]

        for i, (label, value, color) in enumerate(financial_data):
            row = i // 3
            col = i % 3

            item_frame = tk.Frame(fin_grid, bg=COLORS['light'])
            item_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')

            tk.Label(
                item_frame,
                text=label,
                font=FONTS['normal'],
                bg=COLORS['light']
            ).pack(side='left')

            tk.Label(
                item_frame,
                text=value,
                font=FONTS['heading'],
                bg=COLORS['light'],
                fg=color
            ).pack(side='left', padx=(10, 0))

        quick_actions_frame = tk.LabelFrame(
            self.container,
            text="Quick Actions",
            font=FONTS['heading'],
            bg=COLORS['light'],
            fg=COLORS['primary'],
            padx=15,
            pady=15
        )
        quick_actions_frame.pack(fill='x', pady=(0, 20))

        actions_container = tk.Frame(quick_actions_frame, bg=COLORS['light'])
        actions_container.pack()

        tk.Button(
            actions_container,
            text="Add Room",
            **BUTTON_SUCCESS,
            command=self.show_add_room_dialog
        ).pack(side='left', padx=5)

        tk.Button(
            actions_container,
            text="Create Lease",
            **BUTTON_STYLE,
            command=self.show_create_lease_dialog
        ).pack(side='left', padx=5)

        tk.Button(
            actions_container,
            text="Record Expense",
            **BUTTON_STYLE,
            command=self.show_add_expense_dialog
        ).pack(side='left', padx=5)

        recent_frame = tk.LabelFrame(
            self.container,
            text="Active Leases",
            font=FONTS['heading'],
            bg=COLORS['light'],
            fg=COLORS['primary'],
            padx=15,
            pady=15
        )
        recent_frame.pack(fill='both', expand=True)

        columns = ('Tenant', 'Room', 'Start Date', 'Monthly Rent', 'Status')
        tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        leases = self.controller.get_active_leases()
        for lease in leases:
            tree.insert('', 'end', values=(
                lease[7],
                lease[8],
                lease[3],
                f"₱{lease[5]:,.2f}",
                lease[6]
            ))

    def create_stat_card(self, parent, label, value, color, index):
        card = tk.Frame(parent, bg=color, relief='flat', bd=0)
        card.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(
            card,
            text=str(value),
            font=('Helvetica', 28, 'bold'),
            bg=color,
            fg=COLORS['white']
        ).pack(pady=(15, 5))

        tk.Label(
            card,
            text=label,
            font=FONTS['normal'],
            bg=color,
            fg=COLORS['white']
        ).pack(pady=(0, 15))

    def show_add_room_dialog(self):
        dialog = tk.Toplevel(self.container)
        dialog.title("Add New Room")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Room Number:", **LABEL_STYLE).pack(pady=(20, 5))
        room_number_entry = tk.Entry(dialog, **ENTRY_STYLE)
        room_number_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Capacity:", **LABEL_STYLE).pack(pady=5)
        capacity_entry = tk.Entry(dialog, **ENTRY_STYLE)
        capacity_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Monthly Rent:", **LABEL_STYLE).pack(pady=5)
        rent_entry = tk.Entry(dialog, **ENTRY_STYLE)
        rent_entry.pack(pady=(0, 20))

        def save_room():
            success, message = self.controller.add_room(
                room_number_entry.get(),
                capacity_entry.get(),
                rent_entry.get()
            )
            if success:
                from tkinter import messagebox
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_dashboard()
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Save", **BUTTON_SUCCESS, command=save_room).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def show_create_lease_dialog(self):
        from tkinter import messagebox
        messagebox.showinfo("Create Lease", "Please use Tenants section to create a lease")

    def show_add_expense_dialog(self):
        dialog = tk.Toplevel(self.container)
        dialog.title("Record Expense")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Description:", **LABEL_STYLE).pack(pady=(20, 5))
        desc_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        desc_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Amount:", **LABEL_STYLE).pack(pady=5)
        amount_entry = tk.Entry(dialog, **ENTRY_STYLE)
        amount_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Category:", **LABEL_STYLE).pack(pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, state='readonly')
        category_combo['values'] = ('Maintenance', 'Utilities', 'Supplies', 'Repairs', 'Other')
        category_combo.pack(pady=(0, 10))

        tk.Label(dialog, text="Date (YYYY-MM-DD):", **LABEL_STYLE).pack(pady=5)
        date_entry = tk.Entry(dialog, **ENTRY_STYLE)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack(pady=(0, 20))

        def save_expense():
            from tkinter import messagebox
            success, message = self.controller.record_expense(
                desc_entry.get(),
                amount_entry.get(),
                date_entry.get(),
                category_var.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Save", **BUTTON_SUCCESS, command=save_expense).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def refresh_dashboard(self):
        self.create_ui()
