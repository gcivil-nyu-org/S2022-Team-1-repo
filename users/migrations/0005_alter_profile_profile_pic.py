# Generated by Django 4.0.2 on 2022-04-05 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_profile_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_pic",
            field=models.ImageField(
                default="blank-profile-picture.webp", null=True, upload_to=""
            ),
        ),
    ]
