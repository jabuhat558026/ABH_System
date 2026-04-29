from models.room_model import RoomModel
from models.tenant_model import TenantModel
from models.lease_model import LeaseModel
from models.payment_model import PaymentModel
from models.expense_model import ExpenseModel
from datetime import datetime

class DashboardController:
    def __init__(self, db):
        self.room_model = RoomModel(db)
        self.tenant_model = TenantModel(db)
        self.lease_model = LeaseModel(db)
        self.payment_model = PaymentModel(db)
        self.expense_model = ExpenseModel(db)

    def get_dashboard_stats(self):
        all_rooms = self.room_model.get_all_rooms()
        total_rooms = len(all_rooms)
        occupied_rooms = len([r for r in all_rooms if r[4] == 'occupied'])
        available_rooms = total_rooms - occupied_rooms

        active_tenants = len(self.tenant_model.get_active_tenants())
        active_leases = len(self.lease_model.get_active_leases())

        total_income = self.payment_model.get_total_payments()
        total_expenses = self.expense_model.get_total_expenses()

        current_month = datetime.now().strftime('%Y-%m')
        monthly_income = self.payment_model.get_total_payments_by_date_range(
            current_month + '-01',
            current_month + '-31'
        )
        monthly_expenses = self.expense_model.get_total_expenses_by_date_range(
            current_month + '-01',
            current_month + '-31'
        )

        return {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'active_tenants': active_tenants,
            'active_leases': active_leases,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'net_income': total_income - total_expenses,
            'monthly_net': monthly_income - monthly_expenses
        }

    def get_recent_payments(self, limit=5):
        all_payments = self.payment_model.get_all_payments()
        return all_payments[:limit]

    def get_active_leases(self):
        return self.lease_model.get_active_leases()

    def get_available_rooms(self):
        return self.room_model.get_available_rooms()

    def add_room(self, room_number, capacity, monthly_rent):
        try:
            capacity = int(capacity)
            monthly_rent = float(monthly_rent)
            if capacity <= 0 or monthly_rent <= 0:
                return False, "Capacity and rent must be greater than 0"
        except ValueError:
            return False, "Invalid capacity or rent value"

        return self.room_model.create_room(room_number, capacity, monthly_rent)

    def create_lease(self, tenant_id, room_id, start_date, monthly_rent, deposit):
        try:
            monthly_rent = float(monthly_rent)
            deposit = float(deposit)
            if monthly_rent <= 0 or deposit < 0:
                return False, "Invalid rent or deposit amount"
        except ValueError:
            return False, "Invalid rent or deposit value"

        return self.lease_model.create_lease(tenant_id, room_id, start_date, monthly_rent, deposit)

    def terminate_lease(self, lease_id, end_date):
        return self.lease_model.terminate_lease(lease_id, end_date)

    def record_expense(self, description, amount, expense_date, category):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount"

        return self.expense_model.create_expense(description, amount, expense_date, category)
