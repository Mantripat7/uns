from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

from services.models import ServiceType

# Create your views here.
def home(request):
    service_types = ServiceType.objects.filter(is_active=True)
    return render(request, "index.html", {'service_types': service_types})

def index(request):
    return render(request, "base.html")

def login(request):
    if request.method=="POST":
        form_email = request.POST.get("email")
        form_password = request.POST.get("password")
        try:
            user = User.objects.get(email=form_email)
            if user:
                if user.password == form_password:
                    # session create
                    request.session['user_id'] = user.id
                    return redirect("home")
                else:
                    print("Password is incorrect")
                    return redirect("login")
            else:
                print("User not found")
                return redirect("login")
        except:
            print("User not found")

    return render(request, "login.html")

def register(request):
    if request.method=="POST":
        username = request.POST.get("fname")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone")
        password = request.POST.get("password")

        User.objects.create(
            username = username,
            email = email,
            phone = phone_number,
            password = password,
            active=True
        )
        return redirect("login")
        

    return render(request, "register.html")



def about(request):
    return render(request, "accounts/about.html")


def contact(request):
    return render(request, "accounts/contact.html")


# 2 function define service provider -- login and registration
# also design html files 