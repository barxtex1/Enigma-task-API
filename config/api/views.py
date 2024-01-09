from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from base.models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsVendor, IsCustomer, ReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

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
        
        # Customize the response data
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