import tkinter as tk
from config.database import Database
from controllers.dashboard_controller import DashboardController
from controllers.tenant_controller import TenantController
from controllers.payment_controller import PaymentController
from views.main_view import MainView
from views.dashboard_view import DashboardView
from views.tenant_view import TenantView
from views.payment_view import PaymentView

class ABHSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.db = Database()
        self.db.connect()
        self.db.initialize_tables()

        self.dashboard_controller = DashboardController(self.db)
        self.tenant_controller = TenantController(self.db)
        self.payment_controller = PaymentController(self.db)

        self.main_view = MainView(self.root)

        self.main_view.set_nav_command('dashboard', self.show_dashboard)
        self.main_view.set_nav_command('tenants', self.show_tenants)
        self.main_view.set_nav_command('payments', self.show_payments)

        self.show_dashboard()

    def show_dashboard(self):
        container = self.main_view.get_main_container()
        DashboardView(container, self.dashboard_controller)

    def show_tenants(self):
        container = self.main_view.get_main_container()
        TenantView(container, self.tenant_controller, self.dashboard_controller)

    def show_payments(self):
        container = self.main_view.get_main_container()
        PaymentView(container, self.payment_controller)

    def run(self):
        self.main_view.run()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

if __name__ == "__main__":
    app = ABHSystem()
    app.run()
