# Generated by Django 5.0.6 on 2024-12-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_remove_department_branch_department_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
