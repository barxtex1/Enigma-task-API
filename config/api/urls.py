from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
]

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
urlpatterns += router.urls