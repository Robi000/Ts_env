# Generated by Django 4.0.5 on 2023-10-29 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Oneday_old', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stu_old',
            name='status',
        ),
    ]
