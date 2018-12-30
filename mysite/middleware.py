from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_public_schema_name

class HeaderTenantMiddleware(BaseTenantMiddleware):
    """
    Determines tenant by the value of the ``COMPANY`` HTTP header.
    """
    def get_tenant(self, model, hostname, request):
        schema_name = request.META.get('HTTP_COMPANY', get_public_schema_name())
        print("Schema Name:"+schema_name)
        return model.objects.get(schema_name=schema_name)
