from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICE = [
        ('admin', "Admin"),
        ('manager', "Manager"),
        ('staff', "Staff")
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self) -> str:
        return self.username