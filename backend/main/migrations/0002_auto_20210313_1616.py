# Generated by Django 3.1.6 on 2021-03-13 15:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='id',
            field=models.UUIDField(default=uuid.UUID('22d893e6-4f19-4d6a-8c8c-6d5ba734d499'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
