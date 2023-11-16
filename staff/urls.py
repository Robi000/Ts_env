from django.urls import path
from .views import login_view, manage_user, delete_user

urlpatterns = [
    path("login/", login_view, name="login"),
    path("manage_user/", manage_user, name="manage_user"),
    path("delete_user/<int:id>", delete_user, name="delete_user"),
]
