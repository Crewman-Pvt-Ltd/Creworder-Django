# Generated by Django 5.0.6 on 2024-07-30 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_chat_chat_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chat_session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.chatsession'),
        ),
    ]
