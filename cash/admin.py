from django.contrib import admin
from .models import Departnment, Allocated_cash, Allocation_history, Spending
# Register your models here.

admin.site.register(Departnment)
admin.site.register(Allocated_cash)
admin.site.register(Allocation_history)
admin.site.register(Spending)
