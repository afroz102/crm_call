# Generated by Django 3.2.3 on 2021-08-14 19:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='api_key',
            field=models.CharField(default=uuid.UUID('820251b7-10fc-4598-8006-8154f0e39dd8'), max_length=50),
        ),
    ]
