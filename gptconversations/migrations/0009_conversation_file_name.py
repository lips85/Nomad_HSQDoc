# Generated by Django 5.1.2 on 2024-10-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gptconversations", "0008_alter_conversation_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="file_name",
            field=models.CharField(blank=True, default="", max_length=150, null=True),
        ),
    ]