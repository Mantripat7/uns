from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
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
            if check_password(password, user.password):
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
            full_name=username,
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
        email = request.POST.get('email')
        
        user.email = email
        user.full_name = f"{first_name} {last_name}".strip()
        user.save()
        messages.success(request, 'Profile updated successfully')
        
    # Prepare user object for template compatibility
    # The template expects: username, email, first_name, last_name
    # User model has: full_name, email
    
    # Inject temporary attributes for template display
    user.username = user.full_name
    names = user.full_name.split(' ', 1)
    user.first_name = names[0]
    user.last_name = names[1] if len(names) > 1 else ''
    
    return render(request, 'accounts/profile.html', {'user': user})

def dashboard(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    # Inject temporary attributes if needed by dashboard
    user.username = user.full_name
    
    return render(request, 'accounts/dashboard.html', {'user': user})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

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