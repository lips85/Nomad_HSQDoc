# Generated by Django 5.1.2 on 2024-10-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_api_key"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="api_key",
            new_name="claude_api_key",
        ),
        migrations.AddField(
            model_name="user",
            name="openai_api_key",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]