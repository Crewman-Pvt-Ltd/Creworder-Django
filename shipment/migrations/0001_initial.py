# Generated by Django 5.0.6 on 2024-10-07 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0029_pickuppoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('provider_name', models.CharField(max_length=255)),
                ('credential_username', models.CharField(max_length=255, null=True)),
                ('credential_password', models.CharField(max_length=255, null=True)),
                ('credential_email', models.CharField(max_length=255, null=True)),
                ('credential_token', models.CharField(max_length=255, null=True)),
                ('same_provider_priority', models.IntegerField()),
                ('provider_priority', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')])),
                ('image', models.ImageField(upload_to='shipment_channels_image/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.branch')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
            ],
            options={
                'db_table': 'shipment_table',
            },
        ),
    ]