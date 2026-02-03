from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('PROVIDER', 'Provider'),
    )

    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # store hashed password
    phone = models.IntegerField()

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"
    
class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True)

    service_radius_km = models.IntegerField(default=10)

    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    rating = models.FloatField(default=0)
    total_jobs = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Provider: {self.user.full_name}"
