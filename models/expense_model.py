class ExpenseModel:
    def __init__(self, db):
        self.db = db

    def create_expense(self, description, amount, expense_date, category):
        try:
            self.db.execute(
                "INSERT INTO expenses (description, amount, expense_date, category) VALUES (?, ?, ?, ?)",
                (description, amount, expense_date, category)
            )
            return True, "Expense recorded successfully"
        except Exception as e:
            return False, str(e)

    def get_all_expenses(self):
        return self.db.fetchall("SELECT * FROM expenses ORDER BY expense_date DESC")

    def get_expenses_by_category(self, category):
        return self.db.fetchall(
            "SELECT * FROM expenses WHERE category = ? ORDER BY expense_date DESC",
            (category,)
        )

    def get_expenses_by_date_range(self, start_date, end_date):
        return self.db.fetchall(
            "SELECT * FROM expenses WHERE expense_date BETWEEN ? AND ? ORDER BY expense_date DESC",
            (start_date, end_date)
        )

    def get_total_expenses(self):
        result = self.db.fetchone("SELECT SUM(amount) FROM expenses")
        return result[0] if result[0] else 0

    def get_total_expenses_by_date_range(self, start_date, end_date):
        result = self.db.fetchone(
            "SELECT SUM(amount) FROM expenses WHERE expense_date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        return result[0] if result[0] else 0

    def delete_expense(self, expense_id):
        try:
            self.db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            return True, "Expense deleted successfully"
        except Exception as e:
            return False, str(e)
