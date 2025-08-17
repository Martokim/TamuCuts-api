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

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('beef', 'Beef'),
        ('pork', 'Pork'),
        ('chicken', 'Chicken'),
        ('goat', 'Goat'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    descritpion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category}) - ${self.price}"