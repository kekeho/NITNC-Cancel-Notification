# Generated by Django 2.1.4 on 2018-12-19 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancel',
            name='send_tomorrow_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cancel',
            name='send_upload_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cancel',
            name='send_week_flag',
            field=models.BooleanField(default=False),
        ),
    ]
