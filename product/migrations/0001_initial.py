# Generated by Django 5.0.6 on 2024-07-15 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sr', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.CharField(max_length=100, unique=True)),
                ('product_cat_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('product_sku', models.CharField(max_length=255)),
                ('product_price', models.CharField(max_length=100)),
                ('product_gst', models.CharField(max_length=20)),
                ('product_hsn', models.CharField(max_length=200)),
                ('product_qty', models.IntegerField(default=0)),
                ('product_image', models.TextField()),
                ('product_availability', models.IntegerField(choices=[(0, 'InStock'), (1, 'OutOfStock')])),
                ('product_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Suspended'), (3, 'Deleted')])),
                ('product_created', models.DateTimeField(auto_now_add=True)),
                ('product_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'Product',
            },
        ),
    ]
