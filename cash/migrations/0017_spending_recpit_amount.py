# Generated by Django 4.2.7 on 2024-03-06 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0016_spending_recpit_date_spending_recpit_tin_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='recpit_amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]