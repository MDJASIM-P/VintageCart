# Generated by Django 4.2.3 on 2023-07-09 15:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0004_alter_feedbackmodel_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackmodel',
            name='datetime',
            field=models.DateTimeField(default='20230709 20:50:20'),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 9, 15, 20, 20, 421027, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='report',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 9, 20, 50, 20, 421027)),
        ),
    ]
