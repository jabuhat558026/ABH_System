import tkinter as tk
from tkinter import ttk, messagebox
from assets.styles import *
from datetime import datetime

class PaymentView:
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
            text="Payment Management",
            font=FONTS['title'],
            bg=COLORS['light'],
            fg=COLORS['primary']
        ).pack(side='left')

        btn_frame = tk.Frame(header, bg=COLORS['light'])
        btn_frame.pack(side='right')

        tk.Button(
            btn_frame,
            text="Record Payment",
            **BUTTON_SUCCESS,
            command=self.show_add_payment_dialog
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            **BUTTON_STYLE,
            command=self.refresh_list
        ).pack(side='left')

        summary = self.controller.get_payment_summary()

        summary_frame = tk.Frame(self.container, bg=COLORS['success'], relief='flat')
        summary_frame.pack(fill='x', pady=(0, 20))

        tk.Label(
            summary_frame,
            text=f"Total Payments: ₱{summary['total_payments']:,.2f}",
            font=FONTS['heading'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            pady=15
        ).pack()

        columns = ('ID', 'Tenant', 'Room', 'Amount', 'Date', 'Type', 'Month', 'Notes')
        self.tree = ttk.Treeview(self.container, columns=columns, show='headings', height=15)

        column_widths = {'ID': 50, 'Tenant': 150, 'Room': 80, 'Amount': 100,
                        'Date': 100, 'Type': 100, 'Month': 100, 'Notes': 150}

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])

        scrollbar = ttk.Scrollbar(self.container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        action_frame = tk.Frame(self.container, bg=COLORS['light'])
        action_frame.pack(fill='x', pady=(10, 0))

        tk.Button(
            action_frame,
            text="Delete Payment",
            **BUTTON_DANGER,
            command=self.delete_payment
        ).pack(side='left', padx=5)

        self.load_payments()

    def load_payments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        payments = self.controller.get_all_payments()
        for payment in payments:
            self.tree.insert('', 'end', values=(
                payment[0],
                payment[7],
                payment[8],
                f"₱{payment[1]:,.2f}",
                payment[2],
                payment[3],
                payment[4] if payment[4] else 'N/A',
                payment[5] if payment[5] else ''
            ))

    def show_add_payment_dialog(self):
        dialog = tk.Toplevel(self.container)
        dialog.title("Record Payment")
        dialog.geometry("450x500")
        dialog.configure(bg=COLORS['light'])

        tk.Label(dialog, text="Select Lease:", **LABEL_STYLE).pack(pady=(20, 5))
        lease_var = tk.StringVar()
        lease_combo = ttk.Combobox(dialog, textvariable=lease_var, state='readonly', width=37)

        active_leases = self.controller.get_active_leases_for_payment()
        lease_options = [f"{lease[7]} - Room {lease[8]} (₱{lease[5]:,.2f}/month)" for lease in active_leases]
        lease_combo['values'] = lease_options
        lease_combo.pack(pady=(0, 10))

        tk.Label(dialog, text="Amount:", **LABEL_STYLE).pack(pady=5)
        amount_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        amount_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Payment Type:", **LABEL_STYLE).pack(pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(dialog, textvariable=type_var, state='readonly', width=37)
        type_combo['values'] = ('Rent', 'Deposit', 'Utility', 'Other')
        type_combo.pack(pady=(0, 10))

        tk.Label(dialog, text="Payment Date (YYYY-MM-DD):", **LABEL_STYLE).pack(pady=5)
        date_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Month Covered (YYYY-MM):", **LABEL_STYLE).pack(pady=5)
        month_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        month_entry.insert(0, datetime.now().strftime('%Y-%m'))
        month_entry.pack(pady=(0, 10))

        tk.Label(dialog, text="Notes:", **LABEL_STYLE).pack(pady=5)
        notes_entry = tk.Entry(dialog, **ENTRY_STYLE, width=40)
        notes_entry.pack(pady=(0, 20))

        def on_lease_select(event):
            if lease_combo.current() >= 0:
                lease = active_leases[lease_combo.current()]
                amount_entry.delete(0, 'end')
                amount_entry.insert(0, str(lease[5]))

        lease_combo.bind('<<ComboboxSelected>>', on_lease_select)

        def save_payment():
            if lease_combo.current() < 0:
                messagebox.showerror("Error", "Please select a lease")
                return

            lease_id = active_leases[lease_combo.current()][0]
            success, message = self.controller.record_payment(
                lease_id,
                amount_entry.get(),
                date_entry.get(),
                type_var.get(),
                month_entry.get(),
                notes_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

        tk.Button(dialog, text="Save Payment", **BUTTON_SUCCESS, command=save_payment).pack(pady=5)
        tk.Button(dialog, text="Cancel", **BUTTON_STYLE, command=dialog.destroy).pack()

    def delete_payment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a payment to delete")
            return

        payment_id = self.tree.item(selected[0])['values'][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payment?"):
            success, message = self.controller.delete_payment(payment_id)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_list()
            else:
                messagebox.showerror("Error", message)

    def refresh_list(self):
        self.load_payments()
        summary = self.controller.get_payment_summary()
        self.create_ui()
