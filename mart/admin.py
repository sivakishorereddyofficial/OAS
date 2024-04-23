from django.contrib import admin
from . import models
# Register your models here.

models = [models.Product, models.ProdutGallery, models.Cart ]

admin.site.register(models)