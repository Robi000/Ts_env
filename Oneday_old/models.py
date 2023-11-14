from django.db import models
from datetime import timedelta


# Create your models here.
class Stu_old(models.Model):
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=60, blank=True, null=True)
    Age = models.CharField(max_length=2)
    claimed = models.CharField(max_length=50)
    claimed_date = models.DateField()
    expire_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate expire_date based on claimed_date + 2 years
        self.expire_date = self.claimed_date + timedelta(days=365 * 2)
        super(Stu_old, self).save(*args, **kwargs)

    class Meta:
        """Meta definition for Stu_old."""

        verbose_name = "Stu_old"
        verbose_name_plural = "Stu_olds"

    def __str__(self):
        """Unicode representation of Stu_old."""
        return f"Name:{self.name}"
