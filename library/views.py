from django.views.generic import ListView
from .models import Document


class DocumentListView(ListView):
    context_object_name = 'documents'
    template_name = 'library/document-list.html'

    def get_queryset(self, category=False):
        choice_category = self.request.GET.get('category')
        documents = Document.objects.all()
        if choice_category:
            return documents.filter(category__slug=choice_category)
        return documents
