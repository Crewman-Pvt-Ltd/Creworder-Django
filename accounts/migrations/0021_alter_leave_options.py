# Generated by Django 5.0.6 on 2024-09-09 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_attendance_attendance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leave',
            options={'permissions': (('can_approve_disapprove_leave', 'Can approve disapprove leave'),)},
        ),
    ]