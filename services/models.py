from django.db import models

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    category = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name="services")

    image = models.ImageField(upload_to="service_images/", null=True, blank=True)
    icon = models.ImageField(upload_to="service_icons/", null=True, blank=True)

    name = models.CharField(max_length=150)
    description = models.TextField()

    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_duration_minutes = models.IntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
from accounts.models import ProviderProfile
class ProviderService(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="provider_services")

    custom_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.service.name}"
    

