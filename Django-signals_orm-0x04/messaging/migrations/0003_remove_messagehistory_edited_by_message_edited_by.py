# Generated by Django 5.1.4 on 2025-01-11 21:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_edited_messagehistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagehistory',
            name='edited_by',
        ),
        migrations.AddField(
            model_name='message',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]