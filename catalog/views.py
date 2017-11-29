from django.views.generic import ListView
from .models import Category


class CategoryListView(ListView):
    template_name = 'catalog/category-list.html'
    context_object_name = 'category'
    model = Category

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        return category
