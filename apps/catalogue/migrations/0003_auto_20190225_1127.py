# Generated by Django 2.1.5 on 2019-02-25 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20190219_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='ads_url',
            field=models.URLField(help_text="Please insert the ADS/arXiv url. All other paramters will automatically be retrieved on save!. For example: 'http://adsabs.harvard.edu/abs/1996AJ....112.1487H'", max_length=256, unique=True, verbose_name='ADS url'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='bib_code',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='Bibliographic Code [ADS/arXiv]'),
        ),
    ]
