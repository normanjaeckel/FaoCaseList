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


class FeedAdmin(admin.ModelAdmin):
    """
    Admin configuration for feeds.

    If you add a new feed via admin, it is updateded immediatelly.
    """

    readonly_fields = ("metadata", "last_update")

    # TODO: Add transaction if you like.
    def save_model(self, request, obj, form, change):
        return_value = super().save_model(request, obj, form, change)
        obj.update_feed()
        return return_value


class EntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for entries.

    Shows some data in list and detail view.
    """

    list_display = (
        "feed",
        "guid",
        "published",
        "leitsatzentscheidung",
        "link_html",
        "read",
    )
    list_editable = ("read",)
    readonly_fields = (
        "feed",
        "guid",
        "published",
        "leitsatzentscheidung",
        "link_html",
        "data",
    )
    list_filter = ("feed__bgh",)


admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Case, CaseAdmin)
admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.Entry, EntryAdmin)

description = ugettext_lazy("{app_name} Administration").format(
    app_name=apps.get_app_config("fao_case_list").verbose_name
)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description
