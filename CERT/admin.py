from django.contrib import admin
from .models import Student, Payment_log, CourceAndPrice

# Register your models here.
admin.site.register(Student)
admin.site.register(Payment_log)
admin.site.register(CourceAndPrice)
