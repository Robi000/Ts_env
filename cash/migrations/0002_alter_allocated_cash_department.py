# Generated by Django 4.2.7 on 2024-02-17 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocated_cash',
            name='department',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cash.departnment'),
        ),
    ]