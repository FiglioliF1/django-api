# Generated by Django 2.2.6 on 2019-10-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nums', '0004_auto_20191018_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numero',
            name='num_id',
            field=models.AutoField(default='', primary_key=True, serialize=False),
        ),
    ]
