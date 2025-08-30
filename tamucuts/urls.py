from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from butchery.views import (
    UserViewSet, ProductViewSet,
    OrderViewSet, OrderItemViewSet, 
    ScaleReadingViewSet, StockNotificationViewSet,
    StockTransactionViewSet ,DailyReportView )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'scale-readings', ScaleReadingViewSet)
router.register(r'notifications', StockNotificationViewSet)
router.register(r'stock-transactions', StockTransactionViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), 
    path("api/reports/<str:date>/",DailyReportView.as_view(),name="daily_report"),
] + router.urls
