from django.views.generic import TemplateView

from classifieds.views import ClassifiedViewSet


__all__ = ['HomePageView', 'SearchView']

class HomePageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        super(TemplateView, self).get_context_data(**kwargs)

class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        super(TemplateView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        # Delegate ajax request to DRF view
        if request.is_ajax():
            return ClassifiedViewSet.as_view({'get': 'list'})(request)

        return super(SearchView, self).get(request, *args, **kwargs)