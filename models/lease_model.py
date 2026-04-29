class LeaseModel:
    def __init__(self, db):
        self.db = db

    def create_lease(self, tenant_id, room_id, start_date, monthly_rent, deposit):
        try:
            self.db.execute(
                "INSERT INTO leases (tenant_id, room_id, start_date, monthly_rent, deposit) VALUES (?, ?, ?, ?, ?)",
                (tenant_id, room_id, start_date, monthly_rent, deposit)
            )
            self.db.execute("UPDATE rooms SET status = 'occupied' WHERE id = ?", (room_id,))
            return True, "Lease created successfully"
        except Exception as e:
            return False, str(e)

    def get_all_leases(self):
        query = """
            SELECT l.*, t.name as tenant_name, r.room_number
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN rooms r ON l.room_id = r.id
            ORDER BY l.start_date DESC
        """
        return self.db.fetchall(query)

    def get_active_leases(self):
        query = """
            SELECT l.*, t.name as tenant_name, r.room_number
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN rooms r ON l.room_id = r.id
            WHERE l.status = 'active'
            ORDER BY l.start_date DESC
        """
        return self.db.fetchall(query)

    def get_lease_by_id(self, lease_id):
        query = """
            SELECT l.*, t.name as tenant_name, r.room_number
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN rooms r ON l.room_id = r.id
            WHERE l.id = ?
        """
        return self.db.fetchone(query, (lease_id,))

    def get_lease_by_tenant(self, tenant_id):
        query = """
            SELECT l.*, r.room_number
            FROM leases l
            JOIN rooms r ON l.room_id = r.id
            WHERE l.tenant_id = ? AND l.status = 'active'
        """
        return self.db.fetchone(query, (tenant_id,))

    def terminate_lease(self, lease_id, end_date):
        try:
            lease = self.db.fetchone("SELECT room_id FROM leases WHERE id = ?", (lease_id,))
            if lease:
                self.db.execute(
                    "UPDATE leases SET status = 'terminated', end_date = ? WHERE id = ?",
                    (end_date, lease_id)
                )
                self.db.execute("UPDATE rooms SET status = 'available' WHERE id = ?", (lease[0],))
                return True, "Lease terminated successfully"
            return False, "Lease not found"
        except Exception as e:
            return False, str(e)

    def update_lease(self, lease_id, monthly_rent):
        try:
            self.db.execute(
                "UPDATE leases SET monthly_rent = ? WHERE id = ?",
                (monthly_rent, lease_id)
            )
            return True, "Lease updated successfully"
        except Exception as e:
            return False, str(e)
