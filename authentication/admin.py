from django.contrib import admin

# Register your models here.
from . models import *

tables = [User]

admin.site.register(tables)