from .models import Tenant

def host_name_from_request(request):
    """
    Returns the host name from the request.
    """
    host = request.META['HTTP_HOST']
    return host.split(':')[0].lower()

def tenant_from_request(request):
  hostname = hostname_from_request(request)
  subdomain_prefix = hostname.split('.')[0]
  return Tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()