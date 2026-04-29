from models.payment_model import PaymentModel
from models.lease_model import LeaseModel
from datetime import datetime

class PaymentController:
    def __init__(self, db):
        self.payment_model = PaymentModel(db)
        self.lease_model = LeaseModel(db)

    def record_payment(self, lease_id, amount, payment_date, payment_type, month_covered, notes=""):
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount"

        if not lease_id or not payment_date or not payment_type:
            return False, "All required fields must be filled"

        return self.payment_model.create_payment(lease_id, amount, payment_date, payment_type, month_covered, notes)

    def get_all_payments(self):
        return self.payment_model.get_all_payments()

    def get_payments_by_lease(self, lease_id):
        return self.payment_model.get_payments_by_lease(lease_id)

    def get_payments_by_month(self, month):
        return self.payment_model.get_payments_by_month(month)

    def delete_payment(self, payment_id):
        return self.payment_model.delete_payment(payment_id)

    def get_payment_summary(self):
        total = self.payment_model.get_total_payments()
        return {
            'total_payments': total
        }

    def get_active_leases_for_payment(self):
        return self.lease_model.get_active_leases()
