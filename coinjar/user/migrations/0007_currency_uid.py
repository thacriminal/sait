# Generated by Django 3.0.8 on 2020-09-28 14:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auser_reference_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='uid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
