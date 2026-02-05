from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('order/<int:service_id>/', views.create_booking, name='create_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
