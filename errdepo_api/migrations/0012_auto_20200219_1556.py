# Generated by Django 3.0.2 on 2020-02-19 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('errdepo_api', '0011_auto_20200219_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(default='/image/profIcon/defo.png', max_length=100),
        ),
    ]
