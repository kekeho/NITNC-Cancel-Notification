# Generated by Django 2.1.4 on 2018-12-14 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('cancel_date', models.DateTimeField(blank=True, null=True)),
                ('supplementary_date', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('place', models.CharField(blank=True, max_length=100, null=True)),
                ('major', models.CharField(blank=True, max_length=1, null=True)),
                ('low_grade_class', models.IntegerField(blank=True, null=True)),
                ('teacher', models.CharField(blank=True, max_length=50, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
