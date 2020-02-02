# Generated by Django 3.0.2 on 2020-02-02 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('errdepo_api', '0008_fw_report'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='report',
            name='correspondenceHTML',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='descriptionHTML',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='correspondence',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='env',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='errmsg',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='fw',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
