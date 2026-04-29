import tkinter as tk
from tkinter import ttk
from assets.styles import *

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("ABH Boarding House Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['light'])

        self.main_container = None
        self.create_ui()

    def create_ui(self):
        title_frame = tk.Frame(self.root, **TITLE_STYLE)
        title_frame.pack(fill='x')

        tk.Label(
            title_frame,
            text="ABH Boarding House Management System",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        ).pack()

        nav_frame = tk.Frame(self.root, bg=COLORS['dark'], height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        nav_items = [
            ('dashboard', 'Dashboard'),
            ('tenants', 'Tenants'),
            ('payments', 'Payments')
        ]

        button_container = tk.Frame(nav_frame, bg=COLORS['dark'])
        button_container.pack(expand=True)

        for key, text in nav_items:
            btn = tk.Button(
                button_container,
                text=text,
                font=FONTS['normal'],
                bg=COLORS['dark'],
                fg=COLORS['white'],
                activebackground=COLORS['secondary'],
                activeforeground=COLORS['white'],
                relief='flat',
                padx=30,
                pady=10,
                cursor='hand2'
            )
            btn.pack(side='left', padx=5)
            self.nav_buttons[key] = btn

        self.main_container = tk.Frame(self.root, bg=COLORS['light'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

    def set_nav_command(self, nav_key, command):
        if nav_key in self.nav_buttons:
            self.nav_buttons[nav_key].config(command=command)

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def get_main_container(self):
        return self.main_container

    def show_message(self, title, message, msg_type='info'):
        from tkinter import messagebox
        if msg_type == 'info':
            messagebox.showinfo(title, message)
        elif msg_type == 'error':
            messagebox.showerror(title, message)
        elif msg_type == 'warning':
            messagebox.showwarning(title, message)
        elif msg_type == 'success':
            messagebox.showinfo(title, message)

    def run(self):
        self.root.mainloop()
