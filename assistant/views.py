import decimal
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from assistant.models import Product, Feature, Category, Delivery
from xlsxwriter import Workbook
from django.http import HttpResponse
from assistant.utils import make_xml
from .forms import UpdateMizolPriceForm
from django.urls import reverse_lazy
from assistant.tasks import update_mizol_prices_task, import_parameters_form_prom_task, add_new_products_by_mizol
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_ppf import settings


def index(request):
    context = {'page_name': 'home'}
    return render(request, 'index.html', context)


class CatalogList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'all-products.html'
    paginate_by = 100
    login_url = 'home'

    def get_queryset(self, **kwargs):
        queryset = Product.objects.prefetch_related('delivery_set', 'photo_set').select_related(
            'category',
            'currency',
            'unit',
            'category_rozetka',
        ).filter(active=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogList, self).get_context_data(**kwargs)
        context['nodes'] = Category.objects.all()

        return context


class CatalogCategoryList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'all-products.html'
    paginate_by = 50
    login_url = 'home'

    def get_queryset(self, **kwargs):
        self.category = Category.objects.get(id=self.kwargs.get('pk'))
        categories = (item.id for item in self.category.get_descendants(include_self=True))

        queryset = Product.objects.prefetch_related('delivery_set', 'photo_set').select_related(
            'category', 'currency', 'unit').filter(active=True, category__in=categories)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogCategoryList, self).get_context_data(**kwargs)
        context['category'] = self.category

        return context


class CatalogDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'single-product.html'
    login_url = 'home'

    def get_object(self, queryset=None):
        return Product.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CatalogDetail, self).get_context_data(**kwargs)
        context['features'] = Feature.objects.filter(product=self.object)
        context['delivery'] = Delivery.objects.select_related('provider').filter(product=self.object)
        return context


class CatalogSearch(CatalogList):

    def get_queryset(self):
        return Product.objects.filter(code__icontains=self.request.GET.get('code'))


class CatalogForPromXLSX(View):

    def get(self, request):
        queryset = Product.objects.select_related('category', 'unit').filter(active=True, import_to_prom=True)
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="prom.xlsx"'

        workbook = Workbook(response)
        worksheet = workbook.add_worksheet('Export Products Sheet')
        worksheet_2 = workbook.add_worksheet('Export Groups Sheet')

        header = (
            'Название_позиции',
            'Ключевые_слова',
            'Описание',
            'Тип_товара',
            'Цена',
            'Валюта',
            'Единица_измерения',
            'Ссылка_изображения',
            'Наличие',
            'Идентификатор_товара',
            'Идентификатор_группы',
            'Код_товара',
            'Номер_группы',
        )

        [worksheet.write(0, col, i) for col, i in enumerate(header)]

        for row, item in enumerate(queryset):
            worksheet.write(row + 1, 0, item.title)
            worksheet.write(row + 1, 1, item.category.title)
            worksheet.write(row + 1, 2, item.text.replace(chr(13), '').replace(chr(10), '').replace(
                'src="/media/uploads/', 'src="http://{}/media/uploads/'.format(self.request.META.get('HTTP_HOST'))))
            worksheet.write(row + 1, 3, 'r')
            worksheet.write(row + 1, 4, item.get_price_UAH())
            worksheet.write(row + 1, 5, item.get_currency_code())
            worksheet.write(row + 1, 6, item.get_unit())
            worksheet.write_string(row + 1, 7, ''.join(
                ['http://{}{}, '.format(request.META.get('HTTP_HOST'), img) for img in item.get_all_photo()]
            ))
            worksheet.write(row + 1, 8, item.availability_prom)
            worksheet.write(row + 1, 9, item.code)
            worksheet.write(row + 1, 10, item.category.id)
            worksheet.write(row + 1, 11, item.code)
            worksheet.write(row + 1, 12, item.category.id)

        header_2 = (
            'Номер_группы',
            'Название_группы',
            'Идентификатор_группы',
            'Номер_родителя',
            'Идентификатор_родителя',
        )

        [worksheet_2.write(0, col, i) for col, i in enumerate(header_2)]

        for row, item in enumerate(Category.objects.all()):
            worksheet_2.write(row + 1, 0, item.id)
            worksheet_2.write(row + 1, 1, item.title)
            worksheet_2.write(row + 1, 2, item.id)
            worksheet_2.write(row + 1, 3, item.get_id())
            worksheet_2.write(row + 1, 4, item.get_id())

        return response


class CatalogForRozetkaXML(View):

    def get(self, request):
        response = HttpResponse(content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="catalog-rozetka.xml"'

        make_xml()

        with open('rozetka.xml', 'r') as f:
            file = f.read()
            response.content = file

        return response


class UpdateMizolPriceView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = UpdateMizolPriceForm
    template_name = 'update_mizol.html'
    login_url = reverse_lazy('home')
    permission_required = ('assistant.can_update_mizol',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Обновление каталога продукции по компании Mizol'
        return context

    def form_valid(self, form):

        myfile = form.cleaned_data['file']
        fs = FileSystemStorage()
        name = get_random_string(20)
        filename = fs.save(name + '.xlsx', myfile)

        update_mizol_prices_task.delay(filename)

        return redirect(reverse_lazy('all-catalog'))


class ImportParametersFormPromView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    login_url = reverse_lazy('home')
    form_class = UpdateMizolPriceForm
    template_name = 'update_mizol.html'
    permission_required = ('assistant.can_update_prom_parameters',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Импорт характеристик с prom.ua'
        return context

    def form_valid(self, form):
        myfile = form.cleaned_data['file']
        fs = FileSystemStorage()
        name = get_random_string(20)
        filename = fs.save(name + '.csv', myfile)

        import_parameters_form_prom_task.delay(settings.MEDIA_ROOT + '/' + filename)

        return redirect(reverse_lazy('all-catalog'))


class AddNewMizolProducts(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('assistant.can_update_mizol',)
    login_url = reverse_lazy('home')

    def get(self, request):
        context = {
            'button_id': 'id="addNewPositionToMizol"',
            'title_page': 'Добавление новой продукции по компании Mizol',
        }
        return render(request, 'update_mizol.html', context)

    def post(self, request):
        add_new_products_by_mizol.delay()
        return redirect(reverse_lazy('all-catalog'))
