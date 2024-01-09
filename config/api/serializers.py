from rest_framework import serializers
from base.models import Product, Order, OrderProducts


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductsSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many = True)

    class Meta:
        model = Order
        fields = ['customer', 'delivery_address', 'products']
    

    def create(self, validated_data):
        # deserialize data for further processing
        self.data

        # Pop products from validated data
        products_data = validated_data.pop('products')
        # Create order without products - type of products is dictonary
        order = Order.objects.create(**validated_data)

        # For each item from dictonary of OrderProducts create object and join with our Order
        for item in products_data:
            OrderProducts.objects.create(order = order, **item)

        return order