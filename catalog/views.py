from django.views.generic import ListView, DetailView
from .models import Category, Product


class CatalogRootView(ListView):
    template_name = 'catalog/catalog-root.html'
    context_object_name = 'categories'
    model = Category


class CategoryListView(ListView):
    template_name = 'catalog/category-list.html'
    context_object_name = 'category'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        return category


class ProductDetailView(DetailView):
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    model = Product
