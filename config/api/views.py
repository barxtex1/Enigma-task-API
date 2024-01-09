from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Customize the response data
        response_data = {
            'total price': serializer.instance.total_price,
            'payment date': serializer.instance.payment_date.strftime("%d-%m-%Y, %H:%M:%S"),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)