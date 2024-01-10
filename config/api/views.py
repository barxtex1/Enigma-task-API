from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from base.models import Product, Order, OrderProducts
from .serializers import (
    ProductSerializer, 
    OrderSerializer, 
    OrderStatisticsSerializer,
)
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsVendor, IsCustomer, ReadOnly
from collections import defaultdict

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    ordering = ['-id']

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'description', 'price']

    ordering_fields = ['name', 'category', 'price']

    permission_classes = [(IsAuthenticated&IsVendor)|ReadOnly]


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [(IsAuthenticated&IsCustomer)|ReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send email confirmation
        self.send_confirmation_email(serializer.instance)
        
        # Response data
        response_data = {
            'total price': serializer.instance.total_price,
            'payment date': serializer.instance.payment_date.strftime("%d-%m-%Y, %H:%M:%S"),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


    def send_confirmation_email(self, instance):
        subject = 'Order Confirmation'
        message = render_to_string('base/order_confirmation_email.html', {'order': instance})
        plain_message = strip_tags(message)
        from_email = User.objects.filter(username="admin").first().email
        to_email = instance.user.email

        send_mail(
            subject, 
            plain_message, 
            from_email, 
            [to_email], 
            fail_silently=False
        )


class OrderStatisticsView(generics.ListCreateAPIView):
    serializer_class = OrderStatisticsSerializer
    permission_classes = [IsAuthenticated&IsVendor]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        num_products = serializer.validated_data['num_products']

        # Filter orders based on the specified date range
        ordered_products = OrderProducts.objects.filter(order__order_date__range=[start_date, end_date])

        # Count the occurrences of each product
        product_counts = defaultdict(int)
        for order in ordered_products:
            product_id = order.product.id
            product_counts[product_id] += 1 # most frequently ordered, not the most ordered
            

        # Sort products by order count
        sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)

        # Extract only selected number of products
        top_products = [
            {
                "id": product_id,
                "name": Product.objects.get(id=product_id).name,
                "count": count
            } 
            for product_id, count in sorted_products[:num_products]]


        # Response data
        response_data = {
            'Most frequently ordered products': top_products
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
