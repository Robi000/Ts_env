from django.contrib import admin
from .models import Stu_old


# Register your models here.
@admin.register(Stu_old)
class Stu_oldAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "claimed",
        "claimed_date",
    )  # Define which fields to display in the list view
    search_fields = ["name"]
