# Generated by Django 4.2.7 on 2024-02-20 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0011_spending_departnment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spending',
            name='Cleared_by',
            field=models.CharField(default='** NOT_CLEARED **', max_length=50),
        ),
        migrations.AlterField(
            model_name='spending',
            name='Reviewd_by',
            field=models.CharField(default='** NOT_Reviewd **', max_length=50),
        ),
        migrations.AlterField(
            model_name='spending',
            name='recpit_from',
            field=models.CharField(default='** unavilable **', max_length=150),
        ),
        migrations.AlterField(
            model_name='spending',
            name='recpit_ref_NO',
            field=models.CharField(default='** unavilable **', max_length=150),
        ),
    ]
