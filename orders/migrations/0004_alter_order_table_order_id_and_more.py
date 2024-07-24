# Generated by Django 5.0.6 on 2024-07-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_orderid_orderdetail_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_table',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]