# Generated by Django 3.2.3 on 2021-08-14 19:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='lead_api_key',
            field=models.CharField(default=uuid.UUID('ec4d55da-3a86-474b-aeeb-4f8bd2130254'), max_length=50),
        ),
    ]