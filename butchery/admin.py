from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username")
    ordering = ("email",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_quantity", "is_in_stock", "created_at", "updated_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "category")
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="In Stock?")
    def is_in_stock(self, obj):
        return obj.is_in_stock()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "get_total", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username",)
    ordering = ("-created_at",)

    @admin.display(description="Total Price")
    def get_total(self, obj):
        return obj.get_total_price()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "get_total")
    search_fields = ("product__name",)

    @admin.display(description="Total")
    def get_total(self, obj):
        return obj.get_total_price()
