from django.db import models

from authentication.models import User

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length= 300)
    short_name = models.CharField(max_length=50, null=True)
    description = models.TextField()

    original_cost = models.FloatField()
    discount_percentage = models.FloatField()

    delivery_charges = models.FloatField()
    making_charges = models.FloatField()

    is_machine_made = models.BooleanField(default=False)
    
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=2)
    origin_country = models.CharField(max_length=50, default="USA")
    seller_address = models.TextField()

    count = models.IntegerField(default=1)

    def __str__(self) -> str:
         return self.name


class ProdutGallery(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     images = models.ImageField(upload_to='product_gallery_store')

     def __str__(self) -> str:
          return self.product.name
     
class Cart(models.Model):
     product =  models.ForeignKey(Product, on_delete=models.CASCADE)
     user =  models.ForeignKey(User, on_delete=models.CASCADE)
     count = models.IntegerField(default=1)
     
     def __str__(self) -> str:
          return self.product.name