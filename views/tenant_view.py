import tkinter as tk
from tkinter import ttk, messagebox
from assets.styles import *
from datetime import datetime

class TenantView:
    def __init__(self, container, controller, dashboard_controller):
        self.container = container
        self.controller = controller
        self.dashboard_controller = dashboard_controller
        self.create_ui()

    def create_ui(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        header = tk.Frame(self.container, bg=COLORS['light'])
        header.pack(fill='x', pady=(0, 20))

        tk.Label(
            header,
            text="Tenant Management",
            font=FONTS['title'],
            bg=COLORS['light'],
            fg=COLORS['primary']
        ).pack(side='left')

        btn_frame = tk.Frame(header, bg=COLORS['light'])
        btn_frame.pack(side='right')

        tk.Button(
            btn_frame,
            text="Add Tenant",
            **BUTTON_SUCCESS,
            command=self.show_add_tenant_dialog
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            **BUTTON_STYLE,
            command=self.refresh_list
        ).pack(side='left')

        search_frame = tk.Frame(self.container, bg=COLORS['light'])
        search_frame.pack(fill='x', pady=(0, 10))

        tk.Label(search_frame, text="Search:", **LABEL_STYLE).pack(side='left', padx=(0, 10))
        self.search_entry = tk.Entry(search_frame, **ENTRY_STYLE, width=30)
        self.search_entry.pack(side='left', padx=(0, 10))
        tk.Button(
            search_frame,
            text="Search",
            **BUTTON_STYLE,
            command=self.search_tenants
        ).pack(side='left')

        columns = ('ID', 'Name', 'Contact', 'Email', 'ID Number', 'Status')
        self.tree = ttk.Treeview(self.container, columns=columns, show='headings', height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=50)
            else:
                self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(self.container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        action_frame = tk.Frame(self.container, bg=COLORS['light'])
        action_frame.pack(fill='x', pady=(10, 0))

        tk.Button(
            action_frame,
            text="View Details",
            **BUTTON_STYLE,
            command=self.view_tenant_details
        ).pack(side='left', padx=5)

        tk.Button(
            action_frame,
            text="Edit",
            **BUTTON_STYLE,
            command=self.edit_tenant
        ).pack(side='left', padx=5)

        tk.Button(
            action_frame,
            text="Create Lease",
            **BUTTON_SUCCESS,
            command=self.create_lease
        ).pack(side='left', padx=5)

        tk.Button(
            action_frame,
            text="Delete",
            **BUTTON_DANGER,
            command=self.delete_tenant
        ).pack(side='left', padx=5)

        self.load_tenants()

    def load_tenants(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tenants = self.controller.get_all_tenants()
        for tenant in tenants:
            self.tree.insert('', 'end', values=tenant)

    def search_tenants(self):
        search_term = self.search_entry.get()
        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_term:
            tenants = self.controller.search_tenants(search_term)
        else:
            tenants = self.controller.get_all_tenants()

        for tenant in tenants:
            self.tree.insert('', 'end', values=tenant)

    def show_add_tenant_dialog(self):
        dialog = tk.Toplevel(self.container)
        dialog.title("Add New Tenant")
        dialog.geometry("450x400")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Name:", **LABEL_STYLE).pack(pady=(20, 5))
        name_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        name_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Contact:", **LABEL_STYLE).pack(pady=5)
        contact_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        contact_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Email:", **LABEL_STYLE).pack(pady=5)
        email_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        email_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="ID Number:", **LABEL_STYLE).pack(pady=5)
        id_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        id_entry.pack(pady=(0, 20))

        def save_tenant():
            success, message = self.controller.add_tenant(
                name_entry.get(),
                contact_entry.get(),
                email_entry.get(),
                id_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Save", **BUTTON_SUCCESS, command=save_tenant).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def edit_tenant(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to edit")
            return

        tenant_data = self.tree.item(selected[0])['values']
        tenant_id = tenant_data[0]

        dialog = tk.Toplevel(self.container)
        dialog.title("Edit Tenant")
        dialog.geometry("450x400")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Name:", **LABEL_STYLE).pack(pady=(20, 5))
        name_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        name_entry.insert(0, tenant_data[1])
        name_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Contact:", **LABEL_STYLE).pack(pady=5)
        contact_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        contact_entry.insert(0, tenant_data[2])
        contact_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Email:", **LABEL_STYLE).pack(pady=5)
        email_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        email_entry.insert(0, tenant_data[3])
        email_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="ID Number:", **LABEL_STYLE).pack(pady=5)
        id_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        id_entry.insert(0, tenant_data[4])
        id_entry.pack(pady=(0, 20))

        def update_tenant():
            success, message = self.controller.update_tenant(
                tenant_id,
                name_entry.get(),
                contact_entry.get(),
                email_entry.get(),
                id_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Update", **BUTTON_SUCCESS, command=update_tenant).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def view_tenant_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant")
            return

        tenant_id = self.tree.item(selected[0])['values'][0]
        tenant, lease = self.controller.get_tenant_details(tenant_id)

        dialog = tk.Toplevel(self.container)
        dialog.title("Tenant Details")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS['light'])

        info_frame = tk.Frame(dialog, bg=COLORS['light'], padx=20, pady=20)
        info_frame.pack(fill='both', expand=True)

        tk.Label(info_frame, text="Tenant Information", font=FONTS['heading'], **LABEL_STYLE).pack(pady=(0, 15))

        details = [
            ("Name:", tenant[1]),
            ("Contact:", tenant[2]),
            ("Email:", tenant[3]),
            ("ID Number:", tenant[4]),
            ("Status:", tenant[5])
        ]

        for label, value in details:
            row = tk.Frame(info_frame, bg=COLORS['light'])
            row.pack(fill='x', pady=5)
            tk.Label(row, text=label, font=FONTS['normal'], **LABEL_STYLE, width=15, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=FONTS['normal'], **LABEL_STYLE, anchor='w').pack(side='left')

        if lease:
            tk.Label(info_frame, text="\nLease Information", font=FONTS['heading'], **LABEL_STYLE).pack(pady=(15, 10))
            lease_details = [
                ("Room:", lease[6]),
                ("Start Date:", lease[3]),
                ("Monthly Rent:", f"₱{lease[5]:,.2f}"),
                ("Deposit:", f"₱{lease[4]:,.2f}"),
                ("Status:", lease[2])
            ]
            for label, value in lease_details:
                row = tk.Frame(info_frame, bg=COLORS['light'])
                row.pack(fill='x', pady=5)
                tk.Label(row, text=label, font=FONTS['normal'], **LABEL_STYLE, width=15, anchor='w').pack(side='left')
                tk.Label(row, text=value, font=FONTS['normal'], **LABEL_STYLE, anchor='w').pack(side='left')

        tk.Button(dialog, text="Close", **BUTTON_STYLE, command=dialog.destroy).pack(pady=10)

    def create_lease(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant")
            return

        tenant_id = self.tree.item(selected[0])['values'][0]
        tenant_name = self.tree.item(selected[0])['values'][1]

        dialog = tk.Toplevel(self.container)
        dialog.title(f"Create Lease for {tenant_name}")
        dialog.geometry("450x400")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Select Room:", **LABEL_STYLE).pack(pady=(20, 5))
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(dialog, textvariable=room_var, state='readonly', width=37)

        available_rooms = self.dashboard_controller.get_available_rooms()
        room_options = [f"{room[1]} - ₱{room[3]:,.2f}/month" for room in available_rooms]
        room_combo['values'] = room_options
        room_combo.pack(pady=(0, 10))

        tk.Label(dialog, text="Start Date (YYYY-MM-DD):", **LABEL_STYLE).pack(pady=5)
        date_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Monthly Rent:", **LABEL_STYLE).pack(pady=5)
        rent_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        rent_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Deposit:", **LABEL_STYLE).pack(pady=5)
        deposit_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        deposit_entry.pack(pady=(0, 20))

        def on_room_select(event):
            if room_combo.current() >= 0:
                room = available_rooms[room_combo.current()]
                rent_entry.delete(0, 'end')
                rent_entry.insert(0, str(room[3]))

        room_combo.bind('<<ComboboxSelected>>', on_room_select)

        def save_lease():
            if room_combo.current() < 0:
                messagebox.showerror("Error", "Please select a room")
                return

            room_id = available_rooms[room_combo.current()][0]
            success, message = self.dashboard_controller.create_lease(
                tenant_id,
                room_id,
                date_entry.get(),
                rent_entry.get(),
                deposit_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Create Lease", **BUTTON_SUCCESS, command=save_lease).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def delete_tenant(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to delete")
            return

        tenant_id = self.tree.item(selected[0])['values'][0]
        tenant_name = self.tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {tenant_name}?"):
            success, message = self.controller.delete_tenant(tenant_id)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

    def refresh_list(self):
        self.load_tenants()
