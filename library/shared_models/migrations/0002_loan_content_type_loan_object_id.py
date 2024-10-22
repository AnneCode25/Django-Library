# Generated by Django 5.1.2 on 2024-10-22 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shared_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='loan',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
