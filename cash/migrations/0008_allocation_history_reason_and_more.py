# Generated by Django 4.2.7 on 2024-02-20 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0007_allocation_history_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation_history',
            name='reason',
            field=models.TextField(default='*** Not_spending ***'),
        ),
        migrations.AlterField(
            model_name='allocation_history',
            name='typ',
            field=models.CharField(default='*** Not_allocation ***', max_length=50),
        ),
    ]
