# Generated by Django 5.0.6 on 2024-11-22 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_allowedip_company_allowedip_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowedip',
            name='ip_from',
            field=models.CharField(choices=[('home', 'Home'), ('office', 'Office')], default='office', max_length=100),
        ),
    ]
