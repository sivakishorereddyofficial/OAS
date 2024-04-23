
from django.urls import path, include

from .import views

urlpatterns = [
  path('users', views.get_all_users, name='get_all_users'),
  path('count', views.count)
]
