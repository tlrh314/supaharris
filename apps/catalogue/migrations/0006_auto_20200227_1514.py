# Generated by Django 2.2.10 on 2020-02-27 15:14

import catalogue.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_auto_20200227_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auxiliary',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=catalogue.models.get_aux_folder),
        ),
    ]
