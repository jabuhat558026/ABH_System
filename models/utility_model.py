class UtilityModel:
    def __init__(self, db):
        self.db = db

    def create_utility_record(self, room_id, utility_type, reading, reading_date, amount):
        try:
            self.db.execute(
                "INSERT INTO utilities (room_id, utility_type, reading, reading_date, amount) VALUES (?, ?, ?, ?, ?)",
                (room_id, utility_type, reading, reading_date, amount)
            )
            return True, "Utility record created successfully"
        except Exception as e:
            return False, str(e)

    def get_all_utilities(self):
        query = """
            SELECT u.*, r.room_number
            FROM utilities u
            JOIN rooms r ON u.room_id = r.id
            ORDER BY u.reading_date DESC
        """
        return self.db.fetchall(query)

    def get_utilities_by_room(self, room_id):
        return self.db.fetchall(
            "SELECT * FROM utilities WHERE room_id = ? ORDER BY reading_date DESC",
            (room_id,)
        )

    def get_utilities_by_type(self, utility_type):
        query = """
            SELECT u.*, r.room_number
            FROM utilities u
            JOIN rooms r ON u.room_id = r.id
            WHERE u.utility_type = ?
            ORDER BY u.reading_date DESC
        """
        return self.db.fetchall(query, (utility_type,))

    def delete_utility(self, utility_id):
        try:
            self.db.execute("DELETE FROM utilities WHERE id = ?", (utility_id,))
            return True, "Utility record deleted successfully"
        except Exception as e:
            return False, str(e)
