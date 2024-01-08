from django.db import models
from django_advance_thumbnail import AdvanceThumbnailField


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
