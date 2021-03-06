# Generated by Django 2.2.5 on 2020-02-28 22:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20200227_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayMo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('momentum_score', models.FloatField(blank=True, default=None, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('analyzed_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Stock')),
            ],
        ),
    ]
