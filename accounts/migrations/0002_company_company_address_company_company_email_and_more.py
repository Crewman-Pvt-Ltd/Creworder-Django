# Generated by Django 4.2.13 on 2024-07-15 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_address',
            field=models.CharField(default='company address', max_length=200),
        ),
        migrations.AddField(
            model_name='company',
            name='company_email',
            field=models.EmailField(default='abc@gmail.com', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='123456789', max_length=128, region=None, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_website',
            field=models.CharField(default='abc@gmail.com', max_length=100),
        ),
        migrations.AddField(
            model_name='company',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.package'),
        ),
        migrations.AlterField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
