# Generated by Django 5.0.3 on 2024-04-20 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dropbox", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dropbox",
            name="name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]