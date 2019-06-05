from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from . import models


class FieldAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class CaseAdmin(admin.ModelAdmin):
    list_display = ("caption", "field", "category", "begin", "end")


admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Case, CaseAdmin)

description = ugettext_lazy("{app_name} Administration").format(
    app_name=apps.get_app_config("fao_case_list").verbose_name
)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description
