# Generated by Django 4.2.13 on 2024-07-23 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userrole_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='package',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]