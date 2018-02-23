from django.views.generic import ListView, DetailView
from .models import Category, Product, Manufacturer
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class CatalogRootView(ListView):
    template_name = 'catalog/catalog-root.html'
    context_object_name = 'categories'
    model = Category
    queryset = Category.objects.filter(level=0)


class ProductListView(ListView):
    template_name = 'catalog/category-list.html'
    context_object_name = 'products'
    paginate_by = 24
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs.get('slug'))
        categories = (i.id for i in self.category.get_descendants(include_self=True))
        return Product.objects.filter(category_id__in=categories)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['category'] = self.category
        context['children'] = self.category.get_children()
        return context


class ProductDetailView(DetailView):
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    model = Product


class ProductEditView(LoginRequiredMixin, ProductDetailView):
    template_name = 'catalog/editor/editor.html'

    def post(self, request, pk):
        content = json.loads(str(self.request.body, 'UTF-8')).get('content')

        product = Product.objects.get(id=pk)
        product.text = content
        product.save(update_fields=('text',))

        return JsonResponse({'save': 'true'})


class ManufacturerListView(ListView):
    template_name = ''
    context_object_name = 'manufacturers'
    model = Manufacturer


class ManufacturerDetailView(DetailView):
    template_name = 'catalog/manufacturer-detail.html'
    context_object_name = 'manufacturer'
    model = Manufacturer
