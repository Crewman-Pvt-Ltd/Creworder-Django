# Generated by Django 4.2.13 on 2024-12-10 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_alter_department_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='designations', to='accounts.branch'),
        ),
    ]