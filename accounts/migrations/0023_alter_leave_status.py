# Generated by Django 5.0.6 on 2024-09-09 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_alter_company_options_allowedip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('disapprove', 'Disapprove')], max_length=30),
        ),
    ]
