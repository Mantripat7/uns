from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceType, ProviderService
from accounts.models import ProviderProfile

def services_list(request):
    services = Service.objects.filter(is_active=True)
    categories = ServiceType.objects.filter(is_active=True)
    return render(request, 'services/services.html', {
        'services': services, 
        'categories': categories
    })

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    # Get providers offering this service
    provider_services = ProviderService.objects.filter(service=service, is_active=True)
    return render(request, 'services/service_detail.html', {
        'service': service,
        'provider_services': provider_services
    })

def service_by_provider(request, provider_id):
    provider = get_object_or_404(ProviderProfile, id=provider_id)
    # Get services offered by this provider
    provider_services = ProviderService.objects.filter(provider=provider, is_active=True)
    return render(request, 'services/service_by_provider.html', {
        'provider': provider,
        'provider_services': provider_services
    })
