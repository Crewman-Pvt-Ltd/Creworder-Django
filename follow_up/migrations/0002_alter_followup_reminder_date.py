# Generated by Django 5.0.6 on 2024-08-12 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow_up', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='reminder_date',
            field=models.DateTimeField(),
        ),
    ]
