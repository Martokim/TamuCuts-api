from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Product, Order, OrderItem


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer1", email="customer1@test.com", password="pass1234"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin1234"
        )

    def test_user_list(self):
        url = reverse("user-list") 
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        url = reverse("user-list")
        data = {"username": "newuser", "email": "new@test.com", "password": "pass1234"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin1234"
        )
        self.product = Product.objects.create(
            name="Beef Steak", category="beef", price=1000.00, stock_quantity=5
        )

    def test_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        url = reverse("product-list")
        data = {"name": "Chicken Breast", "category": "chicken", "price": 750, "stock_quantity": 10}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1", email="customer@test.com", password="pass1234"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin1234"
        )
        self.product = Product.objects.create(
            name="Goat Meat", category="goat", price=1200.00, stock_quantity=3
        )
        self.order = Order.objects.create(customer=self.customer, status="PENDING")
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_list(self):
        url = reverse("order-list")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create(self):
        url = reverse("order-list")
        data = {"customer_id": self.customer.id, "status": "PENDING"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_detail(self):
        url = reverse("order-detail", args=[self.order.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1", email="customer@test.com", password="pass1234"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin1234"
        )
        self.product = Product.objects.create(
            name="Pork Ribs", category="pork", price=800.00, stock_quantity=6
        )
        self.order = Order.objects.create(customer=self.customer, status="PENDING")

    def test_add_order_item(self):
        url = reverse("orderitem-list")
        data = {"order": self.order.id, "product_id": self.product.id, "quantity": 2}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_item_detail(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        url = reverse("orderitem-detail", args=[order_item.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
