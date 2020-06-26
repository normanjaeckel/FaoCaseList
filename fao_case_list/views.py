import csv

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Case, Feed


class UpdateFeed(TemplateView):
    """
    View to update all feeds and fetch new entries.
    """

    template_name = "update_feed.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        counter = 0
        for feed in Feed.objects.all():
            counter += feed.update_feed()
        return HttpResponse(
            f"All feeds updated successfully. There are {counter} new entries."
        )


def download_fao(request, *args, **kwargs):
    """
    CSV download of all cases.
    """
    if request.user.is_anonymous or not request.user.is_superadmin:
        raise PermissionDenied
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;filename=fao_cases_export.csv"
    writer = csv.writer(response)
    queryset = Case.objects.all()
    field_names = [field.name for field in queryset.model._meta.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for item in queryset:
        writer.writerow([getattr(item, field_name) for field_name in field_names])
    return response
