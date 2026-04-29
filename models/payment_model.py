class PaymentModel:
    def __init__(self, db):
        self.db = db

    def create_payment(self, lease_id, amount, payment_date, payment_type, month_covered, notes=""):
        try:
            self.db.execute(
                "INSERT INTO payments (lease_id, amount, payment_date, payment_type, month_covered, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (lease_id, amount, payment_date, payment_type, month_covered, notes)
            )
            return True, "Payment recorded successfully"
        except Exception as e:
            return False, str(e)

    def get_all_payments(self):
        query = """
            SELECT p.*, t.name as tenant_name, r.room_number, l.monthly_rent
            FROM payments p
            JOIN leases l ON p.lease_id = l.id
            JOIN tenants t ON l.tenant_id = t.id
            JOIN rooms r ON l.room_id = r.id
            ORDER BY p.payment_date DESC
        """
        return self.db.fetchall(query)

    def get_payments_by_lease(self, lease_id):
        return self.db.fetchall(
            "SELECT * FROM payments WHERE lease_id = ? ORDER BY payment_date DESC",
            (lease_id,)
        )

    def get_payments_by_month(self, month):
        query = """
            SELECT p.*, t.name as tenant_name, r.room_number
            FROM payments p
            JOIN leases l ON p.lease_id = l.id
            JOIN tenants t ON l.tenant_id = t.id
            JOIN rooms r ON l.room_id = r.id
            WHERE p.month_covered = ?
            ORDER BY p.payment_date DESC
        """
        return self.db.fetchall(query, (month,))

    def get_total_payments(self):
        result = self.db.fetchone("SELECT SUM(amount) FROM payments")
        return result[0] if result[0] else 0

    def get_total_payments_by_date_range(self, start_date, end_date):
        result = self.db.fetchone(
            "SELECT SUM(amount) FROM payments WHERE payment_date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        return result[0] if result[0] else 0

    def delete_payment(self, payment_id):
        try:
            self.db.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            return True, "Payment deleted successfully"
        except Exception as e:
            return False, str(e)
