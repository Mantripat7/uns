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
    path('change-password/', views.change_password, name="change_password"),
    path('delete-account/', views.delete_account, name="delete_account"),
    path('my_services/', views.my_services, name="my_services"),
    path('total_bookings/', views.total_bookings, name="total_bookings"),
    path('personal-info/', views.provider_info, name="provider_info"),
]