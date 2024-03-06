from django.db import models
from staff.models import users
# Create your models here.


class Departnment(models.Model):
    name = models.CharField(max_length=150)
    head = models.ForeignKey(users, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        super(Departnment, self).save(*args, **kwargs)
        try:
            Allocated_cash.objects.create(department=self)
        except:
            pass

    class Meta:
        """Meta definition for Departnment."""

        verbose_name = 'Departnment'
        verbose_name_plural = 'Departnments'

    def __str__(self):
        """Unicode representation of Departnment."""
        return self.name


class Allocated_cash(models.Model):

    amount = models.PositiveIntegerField(default=0)
    department = models.OneToOneField(
        Departnment, null=True, on_delete=models.SET_NULL)
    upadated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.department) + " amount remained: " + str(self.amount)

    # def get_absolute_url(self):
    #     return reverse("Allocated_cash_detail", kwargs={"pk": self.pk})


class Allocation_history(models.Model):
    """Model definition for Allocation_history."""
    action = models.CharField(max_length=50, default="")
    typ = models.CharField(max_length=50, default="*** Not_allocation ***")
    amount = models.PositiveIntegerField(default=0)
    prev_amount = models.PositiveIntegerField(default=0)
    current_amount = models.PositiveIntegerField(default=0)
    possesd_by = models.CharField(max_length=50, default="-")
    possesd_for = models.CharField(max_length=50, default="-")
    reason = models.TextField(default="*** Not_spending ***")
    department = models.ForeignKey(
        Departnment, null=True,  on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50, default="")
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Allocation_history."""

        verbose_name = 'Allocation_history'
        verbose_name_plural = 'Allocation_historys'

    def __str__(self):
        return self.action + ": " + str(self.prev_amount) + " -> " + str(self.current_amount)


class Spending(models.Model):
    spend_catagory = models.CharField(max_length=150, default="")
    reason = models.TextField()
    amount = models.PositiveBigIntegerField(default=0)
    departnment = models.ForeignKey(
        Departnment, null=True,  on_delete=models.SET_NULL)
    departnment_name = models.CharField(max_length=50, default="-")
    submitted_by = models.CharField(max_length=50)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)
    finance_cleared = models.BooleanField(default=False)
    recpit_req = models.BooleanField(default=True)
    recpit_amount = models.PositiveBigIntegerField(default=0)
    returned_amount = models.PositiveBigIntegerField(default=0)
    recpit_ref_NO = models.CharField(
        max_length=150, default="** unavilable **")
    recpit_from = models.CharField(max_length=150, default="** unavilable **")
    recpit_TIN_no = models.CharField(
        max_length=150, default="** unavilable **")
    recpit_Date = models.DateField(null=True)
    Reviewd_by = models.CharField(max_length=50, default="** NOT_Reviewd **")
    Cleared_by = models.CharField(max_length=50, default="** NOT_CLEARED **")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    A_or_R_day = models.DateTimeField(null=True)
    clerance_day = models.DateTimeField(null=True)
    submitted_by_user = models.ForeignKey(
        users, related_name='submitted_by', null=True, on_delete=models.SET_NULL)
    Reviewd_by_user = models.ForeignKey(
        users, related_name='Reviewd_by', null=True, on_delete=models.SET_NULL)
    Cleared_by_user = models.ForeignKey(
        users, related_name='Cleared_by', null=True, on_delete=models.SET_NULL)

    class Meta:
        """Meta definition for Spending."""

        verbose_name = 'Spending'
        verbose_name_plural = 'Spendings'

    def __str__(self):
        """Unicode representation of Spending."""
        return "request id:" + str(self.id)
