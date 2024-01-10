from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('order/', views.OrderCreateView.as_view(), name='order-product'),
    path('order/statistics/most-ordered/', views.OrderStatisticsView.as_view(), name='ostatistics-most-ordered'),
]

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
urlpatterns += router.urls