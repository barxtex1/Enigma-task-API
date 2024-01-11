from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from base.models import (
    Product, 
    ProductCategory,
    Order, 
    OrderProducts,
)


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ProductSerializer(serializers.ModelSerializer):
    category = CreatableSlugRelatedField(
        slug_field='name',
        queryset=ProductCategory.objects.all()
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image']


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
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    num_products = serializers.IntegerField()