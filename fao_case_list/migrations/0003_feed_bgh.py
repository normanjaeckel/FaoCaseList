# Generated by Django 2.2.8 on 2019-12-11 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fao_case_list", "0002_entry_feed"),
    ]

    operations = [
        migrations.AddField(
            model_name="feed",
            name="bgh",
            field=models.BooleanField(
                default=False, verbose_name="Besonderes BGH Feed"
            ),
        ),
    ]