from django.views.generic import ListView, DetailView, FormView
from .models import Category, Product, Manufacturer, Order
from .forms import OrderForm
from django.shortcuts import redirect
from django.http import JsonResponse


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
        return Product.objects.filter(
            category_id__in=categories,
            active=True,
        )

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['category'] = self.category
        context['children'] = self.category.get_children()
        return context


class ProductDetailView(FormView):
    template_name = 'catalog/product-detail.html'
    context_object_name = 'product'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['product'] = Product.objects.prefetch_related(
            'gallery_set',
            'benefit_set',
            'feature_set',
        ).get(slug=self.kwargs.get('slug'))
        return context

    def form_valid(self, form):
        order = Order(
            phone=form.cleaned_data.get('phone'),
            product=Product.objects.get(slug=self.kwargs.get('slug')),
        )
        order.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def post(self, request, slug):
        order = Order(
            phone=self.request.POST.get('phone'),
            product=Product.objects.get(slug=self.kwargs.get('slug')),
        )
        order.save()
        return JsonResponse({'status': 'true'})


class ManufacturerListView(ListView):
    template_name = ''
    context_object_name = 'manufacturers'
    model = Manufacturer


class ManufacturerDetailView(DetailView):
    template_name = 'catalog/manufacturer-detail.html'
    context_object_name = 'manufacturer'
    model = Manufacturer
