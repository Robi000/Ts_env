from django.urls import path
from .views import (
    login_view,
    manage_user,
    delete_user,
    edit_user,
    user_detail,
    register,
    home,
    logout_view,
)

urlpatterns = [
    path("", home, name="auth_home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("manage_user/", manage_user, name="manage_user"),
    path("delete_user/<int:id>", delete_user, name="delete_user"),
    path("edituser/<int:id>", edit_user, name="edit_user"),
    path("userdetail/<int:id>", user_detail, name="user_detail"),
    path("user_register/", register, name="user_register"),
]
