import decimal

from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Feature, Delivery, Unit, Photo, RozetkaCategory, Parameter
# from jet.filters import DateRangeFilter
from .forms import (
    SetCourseForm,
    SetUnitForm,
    SetCategoryForm,
    SetCurrencyForm,
    SetPriceForm,
    SetPricePercentForm,
    SetManufacturerForm,
    SetRozetkaCategoryForm,
    SetAvailableFromPromForm,
    SetAuthorForm,
    SetPercentForOldPriceForm,
)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from xlsxwriter import Workbook
from django.http import HttpResponse
import datetime
from assistant.utils import make_xml


class ParameterInline(admin.TabularInline):
    extra = 0
    model = Parameter


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        user = request.user
        qs = super(ParameterAdmin, self).get_queryset(request)
        if user.is_superuser:
            return qs
        elif user.has_perm('assistant.Freelanser'):
            return qs.filter(product__author=user, product__is_checked=False)
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return self.readonly_fields
        elif user.has_perm('assistant.Freelanser'):
            return ['product']
        else:
            return self.readonly_fields


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title', 'created')


class ProductResource(admin.StackedInline):
    class Meta:
        model = Product


class DeliveryInline(admin.StackedInline):
    extra = 0
    model = Delivery


class FeatureInline(admin.TabularInline):
    extra = 0
    model = Feature


class PhotoInline(admin.TabularInline):
    extra = 0
    model = Photo
    fields = ('get_img_tag', 'image', 'weight')
    readonly_fields = ('get_img_tag',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['product']

    def get_queryset(self, request):
        user = request.user
        qs = super(PhotoAdmin, self).get_queryset(request)
        if user.is_superuser:
            return qs
        elif user.has_perm('assistant.Freelanser'):
            return qs.filter(product__author=user, product__is_checked=False)
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        if user.is_superuser:
            return self.readonly_fields
        elif user.has_perm('assistant.Freelanser'):
            return ['product']
        else:
            return self.readonly_fields


def import_to_rozetka(modeladmin, request, queryset):
    for item in queryset:
        item.import_to_rozetka = True
        item.save(update_fields=('import_to_rozetka',))


def import_to_prom(modeladmin, request, queryset):
    for item in queryset:
        item.import_to_prom = True
        item.save(update_fields=('import_to_prom',))


def not_import_to_prom(modeladmin, request, queryset):
    for item in queryset:
        item.import_to_prom = False
        item.save(update_fields=('import_to_prom',))


def not_import_to_rozetka(modeladmin, request, queryset):
    for item in queryset:
        item.import_to_rozetka = False
        item.save(update_fields=('import_to_rozetka',))


def re_count_on(modeladmin, request, queryset):
    for item in queryset:
        item.re_count = True
        item.save(update_fields=('re_count',))


re_count_on.short_description = 'Пересчитывать в грн'


def re_count_off(modeladmin, request, queryset):
    for item in queryset:
        item.re_count = False
        item.save(update_fields=('re_count',))


re_count_off.short_description = 'Не пересчитывать в грн'


def set_course(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установыть новый курс', 'action': 'set_course'}

    if 'apply' in request.POST:
        form = SetCourseForm(request.POST)

        if form.is_valid():
            course = form.cleaned_data['course']

            count = 0
            for item in queryset:
                item.course = course
                item.save()
                count += 1

            modeladmin.message_user(request, "Курс {} установлен у {} товаров.".format(course, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetCourseForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_course.short_description = 'Установить новый курс'


def set_author(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установыть нового автора', 'action': 'set_author'}

    if 'apply' in request.POST:
        form = SetAuthorForm(request.POST)

        if form.is_valid():
            author = form.cleaned_data['author']

            count = 0
            for item in queryset:
                item.author = author
                item.save()
                count += 1

            modeladmin.message_user(request, "Автор {} установлен у {} товаров.".format(author, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetAuthorForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_author.short_description = 'Установить нового автора'


def set_unit(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить единицу измерения', 'action': 'set_unit'}

    if 'apply' in request.POST:
        form = SetUnitForm(request.POST)

        if form.is_valid():
            unit = form.cleaned_data['unit']

            count = 0
            for item in queryset:
                item.unit = unit
                item.save()
                count += 1

            modeladmin.message_user(request, "Единица измерения '{}' установлена у {} товаров.".format(unit, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetUnitForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_unit.short_description = 'Установить единицу измерения'


def set_category(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить категорию', 'action': 'set_category'}

    if 'apply' in request.POST:
        form = SetCategoryForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']

            count = 0
            for item in queryset:
                item.category = category
                item.save()
                count += 1

            modeladmin.message_user(request, "Категория '{}' установлена у {} товаров.".format(category, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetCategoryForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_category.short_description = 'Установить категорию'


def set_category_rozetka(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить категорию Rozetka', 'action': 'set_category_rozetka'}

    if 'apply' in request.POST:
        form = SetRozetkaCategoryForm(request.POST)

        if form.is_valid():
            category_rozetka = form.cleaned_data['category_rozetka']

            count = 0
            for item in queryset:
                item.category_rozetka = category_rozetka
                item.save()
                count += 1

            modeladmin.message_user(request, "Категория для розетки '{}' установлена у {} товаров.".format(category_rozetka, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetRozetkaCategoryForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_category_rozetka.short_description = 'Установить категорию Rozetka'


def set_manufacturer(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить производителя', 'action': 'set_manufacturer'}

    if 'apply' in request.POST:
        form = SetManufacturerForm(request.POST)

        if form.is_valid():
            manufacturer = form.cleaned_data['manufacturer']

            count = 0
            for item in queryset:
                item.manufacturer = manufacturer
                item.save()
                count += 1

            modeladmin.message_user(request, "Производитель '{}' установлен у {} товаров.".format(manufacturer, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetManufacturerForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_manufacturer.short_description = 'Установить производителя'


def set_currency(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить валюту', 'action': 'set_currency'}

    if 'apply' in request.POST:
        form = SetCurrencyForm(request.POST)

        if form.is_valid():
            currency = form.cleaned_data['currency']

            count = 0
            for item in queryset:
                item.currency = currency
                item.save()
                count += 1

            modeladmin.message_user(request, "Валюта {} установлена у {} товаров.".format(currency, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetCurrencyForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_currency.short_description = 'Установить валюту'


def set_price(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить цену', 'action': 'set_price'}

    if 'apply' in request.POST:
        form = SetPriceForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data['price']

            count = 0
            for item in queryset:
                item.price = price
                item.save()
                count += 1

            modeladmin.message_user(request, "Цена {} установлена у {} товаров.".format(price, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetPriceForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_price.short_description = 'Установить цену'


def set_promo_percent(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить промо процент', 'action': 'set_promo_percent'}

    if 'apply' in request.POST:
        form = SetPriceForm(request.POST)

        if form.is_valid():
            promo_percent = form.cleaned_data['price']

            count = 0
            for item in queryset:
                item.promo_percent = promo_percent
                item.save()
                count += 1

            modeladmin.message_user(request, "Процент промо {} установлен у {} товаров.".format(promo_percent, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetPriceForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_promo_percent.short_description = 'Изменить промо процент'


def set_old_price_percent(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить процент для старой цены', 'action': 'set_old_price_percent'}

    if 'apply' in request.POST:
        form = SetPercentForOldPriceForm(request.POST)

        if form.is_valid():
            percent = form.cleaned_data['percent']

            count = 0
            for item in queryset.iterator():
                item.old_price_percent = percent
                item.save()
                count += 1

            modeladmin.message_user(request, "Значение {}% установлено у {} товаров.".format(percent, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetPercentForOldPriceForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_old_price_percent.short_description = 'Установить процент для старой цены'


def save_as_xlsx(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="ppf-catalog-{}.xlsx"'.format(datetime.datetime.now())

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

    products = [product for product in queryset if product.import_to_prom]

    for row, item in enumerate(products):
        worksheet.write(row + 1, 0, item.title)
        worksheet.write(row + 1, 1, item.category.title)
        worksheet.write(row + 1, 2, item.text.replace(chr(13), '').replace(chr(10), '').replace(
            'src="/media/uploads/', 'src="http://{}/media/uploads/'.format(request.META.get('HTTP_HOST'))))
        worksheet.write(row + 1, 3, 'r')
        worksheet.write(row + 1, 4, item.get_price_UAH())
        worksheet.write(row + 1, 5, item.get_currency_code())
        worksheet.write(row + 1, 6, item.get_unit())
        worksheet.write_string(row + 1, 7, ''.join(
            ['http://{}{}, '.format(request.META.get('HTTP_HOST'), img) for img in item.get_all_photo()]
            ))
        worksheet.write(row + 1, 8, '+')
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


save_as_xlsx.short_description = 'Сохранить в формате XLSX'


def get_percent(price, percent, action):
    price = float(price)
    percent = float(percent)
    if action == '+':
        return price + (price * percent / 100)
    if action == '-':
        return price - (price * percent / 100)


def set_percent_price(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Изменение цены на процент', 'action': 'set_percent_price'}

    if 'apply' in request.POST:
        form = SetPricePercentForm(request.POST)

        if form.is_valid():
            percent = form.cleaned_data['percent']
            action_ = form.cleaned_data['action_']

            count = 0
            for item in queryset:
                item.price = get_percent(item.price, percent, action_)
                item.save(update_fields=('price',))
                count += 1

            modeladmin.message_user(
                request,
                "Цена изменена на {}% у {} товаров.".format(percent, count),
                level=messages.SUCCESS
            )
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetPricePercentForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_percent_price.short_description = 'Изменить цену на процент'


def save_as_xml(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="ppf-catalog-{}.xml"'.format(datetime.datetime.now())

    make_xml(queryset)

    with open('rozetka.xml', 'r') as f:
        file = f.read()
        response.content = file

    return response


def set_available_from_prom(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить наличие товара для прома', 'action': 'set_available_from_prom'}

    if 'apply' in request.POST:
        form = SetAvailableFromPromForm(request.POST)

        if form.is_valid():
            available = form.cleaned_data['available']

            count = 0
            for item in queryset:
                item.availability_prom = available
                item.save()
                count += 1

            modeladmin.message_user(
                request, "Наличие {} установлено у {} товаров.".format(available, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetAvailableFromPromForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        context['form'] = form

    return render(request, template, context)


set_available_from_prom.short_description = 'Установить наличие товаров для прома'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'admin.js',
        )

    list_display = (
        "title",
        "category",
        "category_rozetka",
        "import_for_admin",
        "manufacturer",
        "code",
        "active",
        "price",
        "old_price_percent",
        "get_promo_price",
        "discont",
        "get_currency_code",
        "stock_quantity",
        "availability_prom",
        "course",
        "re_count",
        "get_price_UAH",
        "unit",
        "step",
        "get_images_count",
        "updated"
    )
    list_filter = ('currency', 're_count', 'import_to_prom', 'import_to_rozetka', 'vendor_name')
    list_editable = ('price', 're_count', 'course', 'discont')
    readonly_fields = (
        'code',
        'author',
        # 'vendor_id',
        # 'vendor_name',
    )
    search_fields = ('title', 'code', 'category__title')
    resource_class = ProductResource
    inlines = (FeatureInline, DeliveryInline, PhotoInline, ParameterInline)
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Поставщики", is_stacked=False)},
    }
    actions = (
        set_percent_price,
        set_promo_percent,
        set_category,
        set_course,
        set_unit,
        re_count_off,
        re_count_on,
        save_as_xlsx,
        set_currency,
        set_price,
        set_manufacturer,
        save_as_xml,
        set_category_rozetka,
        import_to_rozetka,
        import_to_prom,
        not_import_to_prom,
        not_import_to_rozetka,
        set_available_from_prom,
        set_author,
        set_old_price_percent,
    )
    save_on_top = True
    save_as = True

    def get_queryset(self, request):
        user = request.user
        qs = super(ProductAdmin, self).get_queryset(request)
        if user.is_superuser:
            return qs
        elif user.has_perm('assistant.Freelanser'):
            return qs.filter(author=user, is_checked=False)
        else:
            return qs


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'active'),
    list_display_links=('indented_title',),
)


admin.site.register(
    RozetkaCategory,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'active'),
    list_display_links=('indented_title',),
)
