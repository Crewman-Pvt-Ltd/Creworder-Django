# Generated by Django 5.0.6 on 2024-09-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_shiftroster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='clock_out',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
