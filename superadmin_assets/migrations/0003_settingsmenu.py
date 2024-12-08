# Generated by Django 5.0.6 on 2024-11-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin_assets', '0002_rename_ulr_menumodel_url_submenumodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingsMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('url', models.TextField()),
                ('icon', models.TextField()),
                ('component_name', models.TextField()),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('for_user', models.CharField(choices=[('superadmin', 'For Super Admin'), ('admin', 'For Admin'), ('both', 'Both')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'settings_menu_table',
            },
        ),
    ]
