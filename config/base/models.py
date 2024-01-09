from django.db import models
from django_advance_thumbnail import AdvanceThumbnailField
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


# --- Product Models ---
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='products_pics/')
    thumbnail = AdvanceThumbnailField(source_field='image', 
                                      upload_to='thumbnails/', 
                                      null=True, 
                                      blank=True, 
                                      size=(200, 200))

    def __str__(self) -> str:
        return self.name


# --- Order Models ---
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    customer_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50, 
                                      choices=PAYMENT_STATUS_CHOICES, 
                                      default='PAYMENT_STATUS_PENDING')
    
    products = models.ManyToManyField(Product, through='OrderProducts')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Set order_date if not already set
        if not self.order_date:
            self.order_date = timezone.now()
        # Set payment_date to order_date + 5 days
        self.payment_date = self.order_date + timedelta(days=5)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)