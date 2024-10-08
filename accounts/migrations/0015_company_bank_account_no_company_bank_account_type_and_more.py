# Generated by Django 4.2.13 on 2024-09-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_supportticket_ticket_id_alter_userprofile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bank_account_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='bank_account_type',
            field=models.CharField(blank=True, choices=[('current', 'Current Account'), ('savings', 'Savings Account')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='bank_branch_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='bank_ifsc_code',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='bank_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='cin',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='fssai',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='gst',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='pan',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='support_email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
