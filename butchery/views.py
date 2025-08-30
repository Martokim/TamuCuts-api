from rest_framework import viewsets
from .models import User, Product, Order, OrderItem , ScaleReading, StockNotification , StockTransaction
from .serializers import (UserSerializer,
    ProductSerializer, OrderSerializer, OrderItemSerializer, 
    ScaleReadingSerializer, StockNotificationSerializer,StockTransactionSerializer)
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import BasePermission , IsAuthenticated
from datetime import datetime
from django.db.models import Sum 




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class ScaleReadingViewSet(viewsets.ModelViewSet):
    queryset = ScaleReading.objects.all()
    serializer_class = ScaleReadingSerializer

class StockNotificationViewSet(viewsets.ModelViewSet):
    queryset = StockNotification.objects.all()
    serializer_class = StockNotificationSerializer

class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated]

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class DailyReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, date=None):
        try:
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                transactions = StockTransaction.objects.filter(date=date_obj)
            else:
                transactions = StockTransaction.objects.all()
            opening_stock = transactions.filter(transaction_type="IN").aggregate(Sum("quantity"))["quantity__sum"] or 0
            sales = transactions.filter(transaction_type="OUT").aggregate(Sum("quantity"))["quantity__sum"] or 0
            closing_stock = transactions.filter(transaction_type="CLOSE").aggregate(Sum("quantity"))["quantity__sum"] or 0
            revenue = sum(item.get_total_price() for item in OrderItem.objects.filter(order__created_at__date=date_obj if date else None))
            return Response({
                "date": date or "all",
                "opening_stock": opening_stock,
                "sales": sales,
                "closing_stock": closing_stock,
                "revenue": revenue
            })
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
