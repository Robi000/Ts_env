# Generated by Django 4.0.5 on 2023-11-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CERT', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='robel', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='abebe', max_length=50),
            preserve_default=False,
        ),
    ]
