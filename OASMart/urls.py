from two_factor.urls import urlpatterns as tf_urls

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mart.urls')),
    path('', include('authentication.urls')),
    path('', include('user.urls')),
    path('', include(tf_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)