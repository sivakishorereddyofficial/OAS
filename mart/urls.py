
from django.urls import path, include

from .import views, apis

urlpatterns = [
    path('home', views.homePage, name='logged-in-user-home'),
    path('admin-home', views.admin_home, name='admin-home'),
    path('home/', views.homePageRedirect),
    path('create-product', views.createProductView),
    path('products/<int:id>', views.productDetailedView),
    path('view-cart', views.cart),


    path('api/product', apis.Product.as_view(), name='prodct-manager'),
    path('api/product-images/', apis.ProductGallery.as_view(), name='product-images-api'),
    path('api/product-images/<int:id>', apis.ProductGallery.as_view(), name='product-images-api'),

    path('api/cart', apis.Cart.as_view()),
    path('api/cart/<int:prod_id>', apis.Cart.as_view())
]
