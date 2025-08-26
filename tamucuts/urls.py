from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from butchery.views import UserViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
