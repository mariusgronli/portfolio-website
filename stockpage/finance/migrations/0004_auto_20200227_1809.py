# Generated by Django 2.2.5 on 2020-02-27 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20200227_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='company',
            field=models.CharField(max_length=35),
        ),
    ]