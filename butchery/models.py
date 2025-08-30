from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


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
    payment_type = models.CharField(
    max_length=20,
    choices=[("CASH", "Cash"), ("MOBILE", "Mobile Money")],
    default="CASH"
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

class ScaleReading(models.Model):
    """
    Captures live weight data from a digital scale, links to a product,
    and calculates total price automatically.
    """
    product = models.ForeignKey(Product, related_name="scale_readings", on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # auto-calc total_price if not provided
        if not self.total_price:
            self.total_price = self.weight_kg * float(self.price_per_kg)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.weight_kg} kg {self.product.name} @ {self.price_per_kg}/kg"

class StockNotification(models.Model):
    """
    Stores threshold values for stock monitoring.
    Notifications can later trigger SMS/email.
    """
    product = models.ForeignKey(Product, related_name="notifications", on_delete=models.CASCADE)
    threshold_kg = models.FloatField(help_text="Trigger notification when stock < threshold")
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def check_and_trigger(self):
        """Simple check for low stock."""
        if self.product.stock_quantity < self.threshold_kg:
            self.is_triggered = True
            # In production, integrate SMS/email here
        else:
            self.is_triggered = False
        self.save()

    def __str__(self):
        status = "⚠️ Low Stock" if self.is_triggered else "OK"
        return f"Notification for {self.product.name} ({status})"

class SalesInsight(models.Model):
    """
    Stores lightweight sales analytics (can be auto-updated by signals or cron).
    """
    best_selling_product = models.CharField(max_length=100, blank=True, null=True)
    total_quantity_sold = models.FloatField(default=0)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insights @ {self.calculated_at}: {self.best_selling_product} ({self.total_quantity_sold} kg)"

class StockTransaction(models.Model):
    class TransactionType(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"
        CLOSE = "CLOSE", "Closing Stock"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_transactions")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.FloatField()
    date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stock Transaction"
        verbose_name_plural = "Stock Transactions"

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity} kg)"