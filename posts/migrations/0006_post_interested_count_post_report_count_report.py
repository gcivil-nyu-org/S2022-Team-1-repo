# Generated by Django 4.0.2 on 2022-04-01 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0005_alter_post_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="interested_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="report_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.post"
                    ),
                ),
                (
                    "reported_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("post", "reported_by")},},
        ),
    ]
