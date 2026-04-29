class RoomModel:
    def __init__(self, db):
        self.db = db

    def create_room(self, room_number, capacity, monthly_rent):
        try:
            self.db.execute(
                "INSERT INTO rooms (room_number, capacity, monthly_rent) VALUES (?, ?, ?)",
                (room_number, capacity, monthly_rent)
            )
            return True, "Room created successfully"
        except Exception as e:
            return False, str(e)

    def get_all_rooms(self):
        return self.db.fetchall("SELECT * FROM rooms ORDER BY room_number")

    def get_available_rooms(self):
        return self.db.fetchall("SELECT * FROM rooms WHERE status = 'available' ORDER BY room_number")

    def get_room_by_id(self, room_id):
        return self.db.fetchone("SELECT * FROM rooms WHERE id = ?", (room_id,))

    def update_room(self, room_id, room_number, capacity, monthly_rent):
        try:
            self.db.execute(
                "UPDATE rooms SET room_number = ?, capacity = ?, monthly_rent = ? WHERE id = ?",
                (room_number, capacity, monthly_rent, room_id)
            )
            return True, "Room updated successfully"
        except Exception as e:
            return False, str(e)

    def update_room_status(self, room_id, status):
        self.db.execute("UPDATE rooms SET status = ? WHERE id = ?", (status, room_id))

    def delete_room(self, room_id):
        try:
            self.db.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
            return True, "Room deleted successfully"
        except Exception as e:
            return False, str(e)
