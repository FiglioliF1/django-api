# Generated by Django 2.2.6 on 2019-10-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nums', '0002_auto_20191010_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numero',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]