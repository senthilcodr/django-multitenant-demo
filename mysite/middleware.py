from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import (get_tenant_model, get_public_schema_name)
from django.db import connection

class HeaderTenantMiddleware(BaseTenantMiddleware):
    """
    Determines tenant by the value of the ``COMPANY`` HTTP header.
    """
    def get_tenant(self, model, hostname, request):
        schema_name = request.META.get('HTTP_COMPANY', get_public_schema_name())
        return model.objects.get(schema_name=schema_name)

    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()

        hostname = self.hostname_from_request(request)
        TenantModel = get_tenant_model()

        try:
            # get_tenant must be implemented by extending this class.
            tenant = self.get_tenant(TenantModel, hostname, request)
            assert isinstance(tenant, TenantModel)
            request.tenant = tenant
            connection.set_tenant(request.tenant)  
        except TenantModel.DoesNotExist:
            # Nothing to be done.  We don't have a public tenant
            pass

