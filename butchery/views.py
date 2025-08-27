from rest_framework import viewsets
from .models import User, Product, Order, OrderItem , ScaleReading, StockNotification
from .serializers import (UserSerializer,
    ProductSerializer, OrderSerializer, OrderItemSerializer, 
    ScaleReadingSerializer, StockNotificationSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ScaleReadingViewSet(viewsets.ModelViewSet):
    queryset = ScaleReading.objects.all()
    serializer_class = ScaleReadingSerializer

class StockNotificationViewSet(viewsets.ModelViewSet):
    queryset = StockNotification.objects.all()
    serializer_class = StockNotificationSerializer

