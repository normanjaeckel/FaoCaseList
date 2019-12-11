import feedparser
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext, ugettext_lazy
from jsonfield import JSONField

# This text snippet can be stripped away in the BGH feed.
FILTER_TEXT = (
    "<strong><span style='color:#800000;'> Diese Entscheidung wird "
    "nur zur nicht gewerblichen Nutzung kostenfrei bereitgestellt "
    "(§ 11 Abs. 2 Satz 2 JVKostG)</span></strong>"
)


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


class Feed(models.Model):
    """
    Model for RSS or Atom feeds.
    """

    url = models.CharField(verbose_name=ugettext_lazy("URL"), max_length=255)

    metadata = JSONField(verbose_name=ugettext_lazy("Metadaten"))

    last_update = models.DateTimeField(
        verbose_name=ugettext_lazy("Aktualisierung"), auto_now=True
    )

    bgh = models.BooleanField(
        verbose_name=ugettext_lazy("Besonderes BGH Feed"), default=False,
    )  # This is a useless field, sorry.

    class Meta:
        verbose_name = ugettext_lazy("Feed")
        verbose_name_plural = ugettext_lazy("Feeds")

    def __str__(self):
        return self.metadata.get("title", "ERROR")

    def update_feed(self):
        """
        Updates this feed. Returns an integer with the number of new entries.
        """
        counter = 0
        data = feedparser.parse(self.url)
        self.metadata = data["feed"]
        if self.metadata == {}:
            self.metadata = {"error": True}
        else:
            for entry in data["entries"]:
                guid = entry.get("id")
                if guid:
                    if Entry.objects.filter(guid=guid).exists():
                        continue
                else:
                    if Entry.objects.filter(data=entry).exists():
                        continue
                Entry.objects.create(feed=self, guid=guid, data=entry)
                counter += 1
        self.save()
        return counter


class Entry(models.Model):
    """
    Model for feed entries.
    """

    feed = models.ForeignKey(
        verbose_name=ugettext_lazy("Feed"), to=Feed, on_delete=models.CASCADE
    )

    guid = models.CharField(
        verbose_name=ugettext_lazy("GUID"), max_length=255, null=True
    )

    data = JSONField(verbose_name=ugettext_lazy("Daten"))

    read = models.BooleanField(
        verbose_name=ugettext_lazy("Gelesen"), blank=True, default=False
    )

    class Meta:
        verbose_name = ugettext_lazy("Eintrag")
        verbose_name_plural = ugettext_lazy("Einträge")

    def __str__(self):
        return self.guid or self.data.get("title", ugettext("Kein Titel vorhanden"))

    @property
    def link_html(self):
        link = self.data.get("link")
        if link:
            return_value = format_html(f'<a href="{link}">{link}</a>')
        else:
            return_value = ugettext("Kein Link vorhanden")
        return return_value

    @property
    def published(self):
        return self.data.get("published", ugettext("Unbekannt"))

    @property
    def leitsatzentscheidung(self):
        """
        Special property for the BGH feed."
        """
        summary = self.data.get("summary", "")
        return summary.replace(FILTER_TEXT, "")
