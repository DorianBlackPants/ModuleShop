# Generated by Django 3.1.2 on 2020-10-31 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='funds',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
