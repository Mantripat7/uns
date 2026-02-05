from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceType, ProviderService
from accounts.models import ProviderProfile

from django.db.models import Q, Avg, Count

def services_list(request):
    services = Service.objects.filter(is_active=True).annotate(
        avg_rating=Avg('booking__review__rating'),
        review_count=Count('booking__review')
    )

    categories = ServiceType.objects.filter(is_active=True)

    # Filters
    search_query = request.GET.get('keyword', '')
    category_filters = request.GET.getlist('categories')
    rating_filters = request.GET.getlist('ratings')
    sort_by = request.GET.get('sort', '')

    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filters:
        services = services.filter(category__id__in=category_filters)

    if rating_filters:
        rating_queries = Q()
        for rating in rating_filters:
            rating = int(rating)
            rating_queries |= Q(avg_rating__exact=rating)
        
        if rating_queries:
            services = services.filter(rating_queries)

    # Sorting
    if sort_by == 'price_low':
        services = services.order_by('base_price')
    elif sort_by == 'price_high':
        services = services.order_by('-base_price')
    elif sort_by == 'rating':
        services = services.order_by('-avg_rating')
    
    context = {
        'services': services, 
        'categories': categories,
        'search_query': search_query,
        'selected_categories': [int(x) for x in category_filters],
        'selected_ratings': [int(x) for x in rating_filters],
        'sort_by': sort_by,
        'total_services': services.count()
    }
    return render(request, 'services/services.html', context)

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
