from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from base.models import Product
from .serializers import ProductSerializer
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'category', 'description', 'price']

    ordering_fields = ['name', 'category', 'price']



    # permission_classes = [IsAuthenticated]
