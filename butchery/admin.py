from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Product,Order,OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username")
    ordering = ("email",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category","price","stock_quantity","created_at","updated_at")
    list_filter = ("category","created_at")
    search_fields = ("name", "category")
    ordering = ("-created_at",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
    search_fields = ("product__name",)
    