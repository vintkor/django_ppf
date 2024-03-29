from django.views.generic import DetailView
from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
