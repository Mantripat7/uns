from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='services_list'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('provider/<int:provider_id>/', views.service_by_provider, name='service_by_provider'),
]
