# Generated by Django 2.1.7 on 2019-03-08 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketcore', '0002_auto_20190308_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='added_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
