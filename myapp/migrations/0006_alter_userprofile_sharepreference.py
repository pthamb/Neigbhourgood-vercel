# Generated by Django 5.0 on 2023-12-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0005_alter_userprofile_latitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="sharePreference",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
