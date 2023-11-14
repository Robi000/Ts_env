from django.urls import path
from .views import All_view, student_detail

urlpatterns = [
    path("", All_view, name="old_site"),
    path("<int:id>/", student_detail, name="old_id"),
]
