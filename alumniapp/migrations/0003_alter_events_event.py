# Generated by Django 5.0.4 on 2024-11-12 15:54

import alumniapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumniapp', '0002_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event',
            field=models.FileField(null=True, upload_to='events/', validators=[alumniapp.models.validate_pdf]),
        ),
    ]