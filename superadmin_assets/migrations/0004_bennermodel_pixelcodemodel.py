# Generated by Django 5.0.6 on 2024-11-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin_assets', '0003_settingsmenu'),
    ]

    operations = [
        migrations.CreateModel(
            name='BennerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_img', models.ImageField(upload_to='banner_images/')),
                ('link', models.TextField()),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'banner_table',
            },
        ),
        migrations.CreateModel(
            name='PixelCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_analytics_code', models.TextField()),
                ('meta_pexel_code', models.TextField()),
                ('other_pexel_code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pixelcode_table',
            },
        ),
    ]