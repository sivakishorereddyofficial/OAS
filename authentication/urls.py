


from django.urls import path, include

from .import views, APIs

urlpatterns = [
  path('login', views.login_homepage, name='login'),
  path('signup', views.register, name='register'),
  path('register-user', views.register_user, name='register-user'), 
  path('test-totp', APIs.confirm_otp),
  path('logout', views.logout_user, name='logout'),
  path('complete-setup', views.register2fa, name='complete-setup'),
  path('otp-challenge', views.otp_challenge, name="otp-challenge"),
  path('login-verify-user',views.login_verify_user),
  path('verify-otp', APIs.verify_otp, name='verify-otp-api'),
]
