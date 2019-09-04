from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Feed


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
