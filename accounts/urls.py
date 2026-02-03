from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="uns"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
]