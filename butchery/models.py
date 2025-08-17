from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Extra fields for TamuCuts users
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('staff', 'Staff'), ('customer', 'Customer')],
        default='customer'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"