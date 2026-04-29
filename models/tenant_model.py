class TenantModel:
    def __init__(self, db):
        self.db = db

    def create_tenant(self, name, contact, email, id_number):
        try:
            self.db.execute(
                "INSERT INTO tenants (name, contact, email, id_number) VALUES (?, ?, ?, ?)",
                (name, contact, email, id_number)
            )
            return True, "Tenant created successfully"
        except Exception as e:
            return False, str(e)

    def get_all_tenants(self):
        return self.db.fetchall("SELECT * FROM tenants ORDER BY name")

    def get_active_tenants(self):
        return self.db.fetchall("SELECT * FROM tenants WHERE status = 'active' ORDER BY name")

    def get_tenant_by_id(self, tenant_id):
        return self.db.fetchone("SELECT * FROM tenants WHERE id = ?", (tenant_id,))

    def update_tenant(self, tenant_id, name, contact, email, id_number):
        try:
            self.db.execute(
                "UPDATE tenants SET name = ?, contact = ?, email = ?, id_number = ? WHERE id = ?",
                (name, contact, email, id_number, tenant_id)
            )
            return True, "Tenant updated successfully"
        except Exception as e:
            return False, str(e)

    def update_tenant_status(self, tenant_id, status):
        self.db.execute("UPDATE tenants SET status = ? WHERE id = ?", (status, tenant_id))

    def delete_tenant(self, tenant_id):
        try:
            self.db.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))
            return True, "Tenant deleted successfully"
        except Exception as e:
            return False, str(e)

    def search_tenants(self, search_term):
        query = "SELECT * FROM tenants WHERE name LIKE ? OR contact LIKE ? OR id_number LIKE ?"
        return self.db.fetchall(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
