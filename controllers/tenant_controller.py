from models.tenant_model import TenantModel
from models.lease_model import LeaseModel

class TenantController:
    def __init__(self, db):
        self.tenant_model = TenantModel(db)
        self.lease_model = LeaseModel(db)

    def add_tenant(self, name, contact, email, id_number):
        if not name or not contact or not id_number:
            return False, "All required fields must be filled"
        return self.tenant_model.create_tenant(name, contact, email, id_number)

    def get_all_tenants(self):
        return self.tenant_model.get_all_tenants()

    def get_active_tenants(self):
        return self.tenant_model.get_active_tenants()

    def get_tenant_details(self, tenant_id):
        tenant = self.tenant_model.get_tenant_by_id(tenant_id)
        lease = self.lease_model.get_lease_by_tenant(tenant_id)
        return tenant, lease

    def update_tenant(self, tenant_id, name, contact, email, id_number):
        if not name or not contact or not id_number:
            return False, "All required fields must be filled"
        return self.tenant_model.update_tenant(tenant_id, name, contact, email, id_number)

    def delete_tenant(self, tenant_id):
        lease = self.lease_model.get_lease_by_tenant(tenant_id)
        if lease:
            return False, "Cannot delete tenant with active lease"
        return self.tenant_model.delete_tenant(tenant_id)

    def search_tenants(self, search_term):
        return self.tenant_model.search_tenants(search_term)
