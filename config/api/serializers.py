from rest_framework import serializers
from base.models import (
    Product, 
    Order, 
    OrderProducts,
)


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
        fields = ['customer_name', 'delivery_address', 'products']
    

    def create(self, validated_data):
        # Retrieve the user associated with the authentication token
        user = self.context['request'].user

        # Set the customer field to the authenticated user
        validated_data['user'] = user

        # Pop products from validated data
        products_data = validated_data.pop('products')

        # Calculate total price based on products in the order
        validated_data['total_price'] = sum(item['product'].price * item['quantity'] for item in products_data)

        # deserialize data for further processing
        self.data

        # Create order without products - type of products is dictonary
        order = Order.objects.create(**validated_data)

        # For each item from dictonary of OrderProducts create object (save to db) and join with our Order
        for item in products_data:
            OrderProducts.objects.create(order = order, **item)

        return order
    

class OrderStatisticsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    num_products = serializers.IntegerField()