# Generated by Django 3.1.4 on 2020-12-17 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201217_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.deliveryinformation'),
        ),
    ]
