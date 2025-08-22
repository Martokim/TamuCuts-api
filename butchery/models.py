from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        CUSTOMER = "customer", "Customer"

    # Extra fields for TamuCuts users
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Product(models.Model):
    class Category(models.TextChoices):
        BEEF = "beef", "Beef"
        PORK = "pork", "Pork"
        CHICKEN = "chicken", "Chicken"
        GOAT = "goat", "Goat"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) - ${self.price}"

    def is_in_stock(self):
        """Check if product is available in stock."""
        return self.stock_quantity > 0


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

    def get_total_price(self):
        """Calculate total order cost from items."""
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("order", "product")
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """Get total price for this order item."""
        return self.quantity * self.product.price
