from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()


# create a model for provider:
# suitables fields