# Generated by Django 4.2.7 on 2024-01-01 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CERT', '0005_student_report_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_log',
            name='created',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2024, 1, 1, 6, 52, 37, 675241, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]