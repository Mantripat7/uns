from django.db import models
from accounts.models import User, ProviderProfile
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_bookings")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="provider_bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    service_address = models.TextField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=(
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ))
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'bookings_payment'

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"

from accounts.models import User, ProviderProfile
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
