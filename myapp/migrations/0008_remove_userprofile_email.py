# Generated by Django 5.0 on 2023-12-16 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0007_userprofile_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="email",
        ),
    ]