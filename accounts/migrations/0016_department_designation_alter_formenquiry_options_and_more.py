# Generated by Django 4.2.13 on 2024-09-05 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0015_company_bank_account_no_company_bank_account_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='designations', to='accounts.branch')),
            ],
        ),
        migrations.AlterModelOptions(
            name='formenquiry',
            options={'verbose_name_plural': 'Form Enquiries'},
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(blank=True, choices=[('full', 'Full Day'), ('first', 'First Half'), ('second', 'Second Half')], max_length=30, null=True)),
                ('type', models.CharField(choices=[('casual', 'Casual'), ('sick', 'Sick'), ('earned', 'Earned')], max_length=30)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved')], max_length=30)),
                ('reason', models.CharField(max_length=500)),
                ('date', models.DateField(blank=True, null=True)),
                ('attachment', models.ImageField(blank=True, null=True, upload_to='leave_attachments/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occasion', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.department')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.designation')),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('summary', models.CharField(blank=True, max_length=255, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='accounts.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Appreciation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_given', models.DateField()),
                ('summary', models.CharField(blank=True, max_length=500, null=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.award')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appreciations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]