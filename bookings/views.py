from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from services.models import Service, ProviderService
from accounts.models import ProviderProfile, User
from .models import Booking

def create_booking(request, service_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, id=user_id)
    service = get_object_or_404(Service, id=service_id)
    provider_services = ProviderService.objects.filter(service=service)
    
    selected_provider_id = request.GET.get('provider_id')
    if selected_provider_id:
        try:
            selected_provider_id = int(selected_provider_id)
        except ValueError:
            selected_provider_id = None

    if request.method == 'POST':
        provider_id = request.POST.get('provider')
        city = request.POST.get('city')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not provider_id:
            messages.error(request, "Please select a provider.")
            return render(request, 'bookings/order.html', {'service': service, 'provider_services': provider_services})

        provider = get_object_or_404(ProviderProfile, id=provider_id)
        
        # Get custom price if available, else base price
        try:
            ps = ProviderService.objects.get(provider=provider, service=service)
            price = ps.custom_price
        except ProviderService.DoesNotExist:
            price = service.base_price

        booking = Booking.objects.create(
            customer=user,
            provider=provider,
            service=service,
            city=city,
            service_address=address,
            booking_date=date,
            booking_time=time,
            price=price,
            status='PENDING'
        )
        
        request.session['last_booking_id'] = booking.id
        messages.success(request, "Booking request sent successfully!")
        return redirect('bookings:booking_success')

    context = {
        'service': service,
        'provider_services': provider_services,
        'selected_provider_id': selected_provider_id,
    }
    return render(request, 'bookings/order.html', context)


def booking_success(request):
    booking_id = request.session.get('last_booking_id')
    booking = None
    user = request.session.get('user_id')
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id, customer=user)
    
    return render(request, 'bookings/checkout.html', {'booking': booking})

def my_bookings(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(customer=user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)
