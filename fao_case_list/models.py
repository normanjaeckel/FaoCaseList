from django.db import models
from django.utils.translation import ugettext_lazy


class Field(models.Model):
    name = models.CharField(verbose_name=ugettext_lazy("Name"), max_length=255)

    section = models.CharField(verbose_name=ugettext_lazy("Norm"), max_length=255)

    weight = models.IntegerField(verbose_name=ugettext_lazy("Gewichtung"), default=0)

    class Meta:
        ordering = ("weight",)
        verbose_name = ugettext_lazy("Bereich")
        verbose_name_plural = ugettext_lazy("Bereiche")

    def __str__(self):
        return f"{self.name} – {self.section}"


class Category(models.Model):
    name = models.CharField(verbose_name=ugettext_lazy("Name"), max_length=255)

    group = models.IntegerField(verbose_name=ugettext_lazy("Gruppe"))

    weight = models.IntegerField(verbose_name=ugettext_lazy("Gewichtung"), default=0)

    class Meta:
        ordering = ("weight",)
        verbose_name = ugettext_lazy("Kategorie")
        verbose_name_plural = ugettext_lazy("Kategorien")

    def __str__(self):
        return f"{self.name} (Gruppe {self.group})"


class Case(models.Model):
    caption = models.CharField(
        verbose_name=ugettext_lazy("Betreff/Parteien"), max_length=255
    )

    short_caption = models.CharField(
        verbose_name=ugettext_lazy("Kurzrubrum"), max_length=255
    )

    case_number = models.CharField(
        verbose_name=ugettext_lazy("Aktenzeichen"), max_length=255
    )

    court = models.CharField(
        verbose_name=ugettext_lazy("Gericht (inkl. Aktenzeichen)"),
        max_length=255,
        blank=True,
    )

    state = models.CharField(
        verbose_name=ugettext_lazy("Stand des Verfahrens"),
        max_length=255,
        default="nicht abgeschlossen",
    )

    description = models.TextField(
        verbose_name=ugettext_lazy("Art und Umfang Tätigkeit")
    )

    field = models.ForeignKey(
        verbose_name=ugettext_lazy("Bereich"), to=Field, on_delete=models.PROTECT
    )

    category = models.ForeignKey(
        verbose_name=ugettext_lazy("Kategorie"), to=Category, on_delete=models.PROTECT
    )

    begin = models.CharField(
        verbose_name=ugettext_lazy("Beginn der Tätigkeit"), max_length=255
    )

    end = models.CharField(
        verbose_name=ugettext_lazy("Ende der Tätigkeit"), max_length=255
    )

    multiplier = models.FloatField(verbose_name=ugettext_lazy("Faktor"), default=1.0)

    class Meta:
        verbose_name = ugettext_lazy("Fall")
        verbose_name_plural = ugettext_lazy("Fälle")

    def __str__(self):
        return self.caption
