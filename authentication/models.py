from django.db import models

# Create your models here.

# from two_factor.

from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']