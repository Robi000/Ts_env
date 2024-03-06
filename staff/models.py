from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class users(models.Model):
    first_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    dept = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name


@receiver(post_save, sender=users)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        username = (
            instance.first_name
            + f"_{instance.role}_"
            + str(users.objects.all().count())
        )
        password = instance.password
        user = User.objects.create_user(username, password=password)
        instance.user = user
        instance.password = ""
        instance.save()
