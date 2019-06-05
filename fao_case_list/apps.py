from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class FaoCaseListAppConfig(AppConfig):
    """
    Django application configuration for this website.
    """

    name = "fao_case_list"
    verbose_name = ugettext_lazy("Fallliste nach der Fachanwaltsordnung")
