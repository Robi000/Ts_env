from django.urls import path
from .views import Payment, payment_handler, complition, complition_handler

urlpatterns = [
    path("", Payment),
    path("payment/", payment_handler),
    path("complition/", complition),
    path("complition/complitionhandler/", complition_handler),
]
