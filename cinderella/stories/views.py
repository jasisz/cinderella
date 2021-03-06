from django.http.response import HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from .models import Variant


class VariantView(DetailView):
    model = Variant
    context_object_name = 'variant'
    template_name = 'stories/variant.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        variant = self.object
        context_data.update({
            'step': variant.get_ancestors().count(),
            'descendants_count': variant.get_descendant_count(),
            'children': variant.get_children(),
            'share_link': 'http://{0}{1}'.format(self.request.get_host(), variant.get_share_url()),
        })
        return context_data


class MutateView(DetailView):
    model = Variant

    def get(self, request, *args, **kwargs):
        variant = self.get_object()
        mutant = variant.mutate()
        return HttpResponseRedirect(mutant.get_absolute_url())
