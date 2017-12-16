from django.views.generic import ListView, DetailView
from .models import Category, Product


class CatalogRootView(ListView):
    template_name = 'catalog/catalog-root.html'
    context_object_name = 'categories'
    model = Category
    queryset = Category.objects.filter(level=0)


class CategoryListView(ListView):
    template_name = 'catalog/category-list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = (i.id for i in self.get_queryset().get_descendants(include_self=True))
        context['children'] = self.get_queryset().get_children()
        context['products'] = Product.objects.select_related('category').filter(category_id__in=categories)
        return context


class ProductDetailView(DetailView):
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    model = Product
