from rest_framework import viewsets, filters, generics
from base.models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

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