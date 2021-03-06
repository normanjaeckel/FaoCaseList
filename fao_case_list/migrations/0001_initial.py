# Generated by Django 2.2.2 on 2019-06-05 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("group", models.IntegerField(verbose_name="Gruppe")),
                ("weight", models.IntegerField(default=0, verbose_name="Gewichtung")),
            ],
            options={
                "verbose_name": "Kategorie",
                "verbose_name_plural": "Kategorien",
                "ordering": ("weight",),
            },
        ),
        migrations.CreateModel(
            name="Field",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("section", models.CharField(max_length=255, verbose_name="Norm")),
                ("weight", models.IntegerField(default=0, verbose_name="Gewichtung")),
            ],
            options={
                "verbose_name": "Bereich",
                "verbose_name_plural": "Bereiche",
                "ordering": ("weight",),
            },
        ),
        migrations.CreateModel(
            name="Case",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "caption",
                    models.CharField(max_length=255, verbose_name="Betreff/Parteien"),
                ),
                (
                    "short_caption",
                    models.CharField(max_length=255, verbose_name="Kurzrubrum"),
                ),
                (
                    "case_number",
                    models.CharField(max_length=255, verbose_name="Aktenzeichen"),
                ),
                (
                    "court",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="Gericht (inkl. Aktenzeichen)",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        default="nicht abgeschlossen",
                        max_length=255,
                        verbose_name="Stand des Verfahrens",
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Art und Umfang Tätigkeit"),
                ),
                (
                    "begin",
                    models.CharField(
                        max_length=255, verbose_name="Beginn der Tätigkeit"
                    ),
                ),
                (
                    "end",
                    models.CharField(max_length=255, verbose_name="Ende der Tätigkeit"),
                ),
                ("multiplier", models.FloatField(default=1.0, verbose_name="Faktor")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fao_case_list.Category",
                        verbose_name="Kategorie",
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fao_case_list.Field",
                        verbose_name="Bereich",
                    ),
                ),
            ],
            options={"verbose_name": "Fall", "verbose_name_plural": "Fälle"},
        ),
    ]
