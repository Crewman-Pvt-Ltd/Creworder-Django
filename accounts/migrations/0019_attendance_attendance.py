# Generated by Django 5.0.6 on 2024-09-09 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_appreciation_award_image_attendance_shift'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attendance',
            field=models.CharField(choices=[('A', 'A'), ('P', 'P')], default='office', max_length=80),
        ),
    ]
