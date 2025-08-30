from rest_framework import serializers
from .models import User, Product, Order, OrderItem, ScaleReading ,StockNotification,StockTransaction, SalesInsight


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone_number", "is_staff", "is_active", "password"]
        read_only_fields = ["is_staff", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "price", "stock_quantity", "created_at", "updated_at"]
        read_only_fields = ["Created_at","updated_at"
                            ]

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_id", "quantity"]
    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        if product.stock_quantity < quantity:
            raise serializers.ValidationError("Insufficient stock for this product")
        return data
    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["quantity"]
        product.stock_quantity -= quantity
        product.save()
        # Create corrssponding StockTransaction 
        StockTransaction.objects.create(
            product=product,
            transaction_type="OUT",
            quantity=quantity,
            date=timezone.now().date(),
            remarks="Sale via order"
        )
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="customer", write_only=True
    )
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "customer_id","items", "status", "created_at", "updated_at", "payment"]
        read_only_fields = ["created_at", "updated_at","items","total_price"]
    
    def get_total_price(self,obj):
        return obj.get_total_price()

class ScaleReadingSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField( queryset=Product.objects.all(), source="product", write_only=True)
    
    class Meta:
        model = ScaleReading
        fields = ["id","product","product_id","weigh_kg","price_per_kg","total_price","recorded_at"]
        read_only_fields = ["total_price","recorded_at"]

    def create(self, validated_data):
        #if price_per_kg not provided user the product's price
        product = validated_data.get("product")
        if not validated_data.get("price_per_kg"):
            validated_data["price_per_kg"] = product.price
        #total_price will be computed in model.save() 
        instance = super().create(validated_data)
        return instance 


class StockNotificationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = StockNotification
        fields = ["id", "product", "product_id", "threshold_kg", "is_triggered", "created_at"]
        read_only_fields = ["is_triggered", "created_at"]

    def validate_threshold_kg(self, value):
        if value < 0:
            raise serializers.ValidationError("threshold_kg must be non-negative.")
        return value


class StockTransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = StockTransaction
        fields = ["id", "product", "product_id", "transaction_type", "quantity", "date", "remarks", "created_at"]
        read_only_fields = ["created_at"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("quantity must be a positive integer.")
        return value
    