# Generated by Django 4.2.7 on 2024-02-20 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0003_alter_departnment_head'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation_history',
            name='typ',
            field=models.CharField(default='add', max_length=50),
            preserve_default=False,
        ),
    ]