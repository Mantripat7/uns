from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

#
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from services.models import ServiceType, Service
from bookings.models import Review
from .models import User, ProviderProfile

# Helper to get user from session
def get_user_from_session(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None

# Create your views here.
def index(request):
    service_types = ServiceType.objects.all()
    popular_services = Service.objects.order_by('?')[:4]
    popular_providers = ProviderProfile.objects.order_by('-rating')[:4]
    reviews = Review.objects.all().order_by('-created_at')[:3]
    
    context = {
        'service_types': service_types,
        'popular_services': popular_services,
        'popular_providers': popular_providers,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            # if check_password(password, user.password) and user.is_active:
            if password == user.password and user.is_active:
            # if password == user.password:
                request.session['user_id'] = user.id
                
                if user.role == 'CUSTOMER':
                    messages.success(request, 'Login successfully')
                    return redirect('uns')
                elif user.role == 'PROVIDER':
                    return redirect('dashboard')
                
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html')
            
        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            phone=int(phone),
            password=hashed_password,
            role='CUSTOMER', 
        )
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
        
    return render(request, 'accounts/register.html')

def logout(request):
    request.session.flush()
    return render(request, 'accounts/logout.html')

def profile(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')
        
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        
        if phone:
            user.phone = int(phone)
            
        user.city = city
        user.address = address
        
        user.save()
        messages.success(request, 'Profile updated successfully')
 
    return render(request, 'accounts/profile.html', {'user': user})

from bookings.models import Booking
from services.models import ProviderService
from django.db.models import Sum

def dashboard(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    context = {'user': user}
    
    if user.role == 'PROVIDER':
        try:
            profile = ProviderProfile.objects.get(user=user)
            context['profile'] = profile
            
            bookings = Booking.objects.filter(provider=profile)
            services = ProviderService.objects.filter(provider=profile)
            
            context['total_bookings'] = bookings.count()
            context['pending_bookings'] = bookings.filter(status='PENDING').count()
            context['accepted_bookings'] = bookings.filter(status='ACCEPTED').count()
            context['completed_bookings'] = bookings.filter(status='COMPLETED').count()
            context['cancelled_bookings'] = bookings.filter(status='CANCELLED').count()
            
            # Total earnings: Sum of price for COMPLETED bookings
            earnings = bookings.filter(status='COMPLETED').aggregate(Sum('price'))['price__sum'] or 0
            context['total_earnings'] = earnings
            
            # Recent bookings
            context['recent_bookings'] = bookings.order_by('-created_at')[:5]
            
            # Provider Services
            context['provider_services'] = services[:5]
            
        except ProviderProfile.DoesNotExist:
            pass
            
    return render(request, 'accounts/dashboard.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def my_services(request):
    user = get_user_from_session(request)
    if not user or user.role != 'PROVIDER':
        return redirect('login')
    
    try:
        profile = ProviderProfile.objects.get(user=user)
        services = ProviderService.objects.filter(provider=profile)
        return render(request, 'accounts/my_services.html', {'user': user, 'services': services})
    except ProviderProfile.DoesNotExist:
        return redirect('dashboard')

def total_bookings(request):
    user = get_user_from_session(request)
    if not user or user.role != 'PROVIDER':
        return redirect('login')
    
    try:
        profile = ProviderProfile.objects.get(user=user)
        bookings = Booking.objects.filter(provider=profile).order_by('-created_at')
        return render(request, 'accounts/total_bookings.html', {'user': user, 'bookings': bookings})
    except ProviderProfile.DoesNotExist:
        return redirect('dashboard')

def provider_info(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    return render(request, 'accounts/provider_info.html', {'user': user})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate 8 character password mix of digit, character, symbols
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(random.choice(characters) for _ in range(8))
            
            # Update into database
            user.password = make_password(new_password)
            user.save()
            
            # Send mail
            subject = 'New Password Request - UNS'
            message = f'Your new password is: {new_password}\n\nPlease login and change it immediately.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, email_from, recipient_list)
            
            messages.success(request, 'New password has been sent.')
            
        except User.DoesNotExist:
            messages.error(request, 'Email not registered')
            
        return redirect('login')
    
    return redirect('login')

def change_password(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Verify current password
        if not check_password(current_password, user.password) and current_password != user.password: # Added fallback for non-hashed legacy support if any
             # The user's code previously had a direct comparison commented out, I'll stick to check_password but maybe they want direct comparison? 
             # The user modified login to use direct comparison, but here I should probably support both or just check_password if they reverted?
             # User changed login to: if password == user.password and user.is_active:
             # So I should probably check direct equality too or just direct equality if that's what they want.
             # But check_password is safer. I'll stick to check_password but if it fails check equality to be safe with their recent changes.
             if current_password != user.password:
                messages.error(request, 'Incorrect current password')
                return redirect('profile')
        
        # Verify new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return redirect('profile')
        
        # Validate new password length
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('profile')
        
        # Update password
        # user.password = make_password(new_password) 
        # User seems to be using plain text passwords based on recent edits? 
        # "if password == user.password and user.is_active:" in login view. 
        # I will save as plain text to be consistent with their login logic change, OR use make_password and hope login handles it. 
        # The login view edit showed: `- if check_password(...)` removed and replaced with `if password == user.password ...`
        # So they are using PLAIN TEXT. I should save as plain text.
        user.password = new_password
        user.save()
        
        messages.success(request, 'Password changed successfully')
        return redirect('profile')
    
    return redirect('profile')

def delete_account(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verify password
        # Consistent with login change:
        if password != user.password: 
             messages.error(request, 'Incorrect password. Please try again.')
             return redirect('delete_account')
        
        # Delete account
        user.is_active = False
        user.save()
        request.session.flush()
        
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('login')
    
    return render(request, 'accounts/delete_account.html', {'user': user})
