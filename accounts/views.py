from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

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
    return render(request, 'index.html')

def login(request):
    print("hello")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        try:
            user = User.objects.get(email=email)
            print(user.password)
            # if check_password(password, user.password):
            if password == user.password:
                request.session['user_id'] = user.id
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
            phone=phone,
            password=hashed_password,
            role='CUSTOMER', 
        )
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
        
    return render(request, 'accounts/register.html')

def logout(request):
    request.session.flush()
    return redirect('login')

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

