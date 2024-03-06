from django.db import models

# Create your models here.


class CourceAndPrice(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"name:{self.name} price:{self.price}Birr"


class Student(models.Model):
    """Model definition for Student."""

    PAYMENT_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Batch = models.PositiveIntegerField(null=True, blank=True)
    registration = models.DateTimeField(auto_now=False, auto_now_add=False)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    age = models.IntegerField()
    edu_lev = models.CharField(max_length=50)
    org = models.CharField(max_length=300)
    occ = models.CharField(max_length=300)
    cource = models.CharField(max_length=50)
    cert_rec_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    cert_type = models.CharField(max_length=50)
    photo_url = models.URLField(max_length=200)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, default="pending"
    )
    finished = models.BooleanField(default=False)
    report_Generated = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Student."""

        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        """Unicode representation of Student."""
        return f"{self.first_name} {self.last_name}"


class Payment_log(models.Model):
    user = models.ForeignKey("staff.users", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    field = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    refunded = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Payment_log"
        verbose_name_plural = "Payment_logs"

    def __str__(self):
        string = "-> refunded" if self.refunded else ""
        return (
            f"{self.user.first_name} {self.user.Last_name} resived {self.amount} birr" + string
        )
