from django.urls import path
from .views import Payment, payment_handler

urlpatterns = [path("", Payment), path("payment/", payment_handler)]
