from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Product, Order, OrderItem, ScaleReading, StockNotification, SalesInsight, StockTransaction


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123", role="admin")
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse("user-list")
        data = {"username": "newuser", "password": "pass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123", role="admin")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Beef", price=500.00, stock_quantity=10.0)

    def test_list_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        url = reverse("product-list")
        data = {"name": "Goat Meat", "price": 650.00, "stock_quantity": 8.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="pass123", role="staff")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Chicken", price=300.00, stock_quantity=5.0)
        self.order = Order.objects.create(customer=self.user)

    def test_list_orders(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        url = reverse("order-list")
        data = {"customer": self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="itemuser", password="pass123", role="staff")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Fish", price=400.00, stock_quantity=6.0)
        self.order = Order.objects.create(customer=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_list_order_items(self):
        url = reverse("orderitem-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_item(self):
        url = reverse("orderitem-list")
        data = {"order": self.order.id, "product": self.product.id, "quantity": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_item_with_stock_deduction(self):
        url = reverse("orderitem-list")
        data = {"order": self.order.id, "product": self.product.id, "quantity": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 4.0)
        transaction = StockTransaction.objects.get(product=self.product, transaction_type="OUT")
        self.assertEqual(transaction.quantity, 2)


class ScaleReadingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="scaleuser", password="pass123", role="staff")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Mutton", price=700.00, stock_quantity=20.0)
        self.scale_reading = ScaleReading.objects.create(product=self.product, weight_kg=2.5, price_per_kg=700.00, total_price=1750.00)

    def test_list_scale_readings(self):
        url = reverse("scalereading-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_scale_reading(self):
        url = reverse("scalereading-list")
        data = {"product": self.product.id, "weight_kg": 3.0, "price_per_kg": 700.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StockNotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="notificationuser", password="pass123", role="admin")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Lamb", price=800.00, stock_quantity=15.0)
        self.notification = StockNotification.objects.create(product=self.product, threshold_kg=5.0, is_triggered=False)

    def test_list_notifications(self):
        url = reverse("stocknotification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_notification(self):
        url = reverse("stocknotification-list")
        data = {"product": self.product.id, "threshold_kg": 3.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SalesInsightTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="insightuser", password="pass123", role="admin")
        self.client.force_authenticate(user=self.user)
        self.insight = SalesInsight.objects.create(best_selling_product="Duck", total_quantity_sold=10.0)

    def test_list_insights(self):
        url = reverse("salesinsight-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_insight(self):
        url = reverse("salesinsight-list")
        data = {"best_selling_product": "Duck", "total_quantity_sold": 15.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)