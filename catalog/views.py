from django.views.generic import ListView, DetailView, FormView
from telegram_bot.models import TelegramBot, TelegramUser
from .models import Category, Product, Manufacturer, Order
from .forms import OrderForm
from django.shortcuts import redirect
from django.http import JsonResponse
from telegram_bot.utils import Telegram
from django_ppf.settings import SITE_URL
import requests
from geo.models import Region


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
        categories = [i.id for i in self.category.get_descendants(include_self=True)]
        products = [i for i in Product.objects.filter(
            category__id__in=categories,
            active=True,
        )]

        return [i for i in set(products)]

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        if self.kwargs.get('region'):
            try:
                region = Region.objects.get(title_eng=self.kwargs.get('region'))
                context['region'] = region
                context['description_aux'] = self.category.description_aux.replace(
                    '#_one_#', region.title
                ).replace('#_many_#', region.title_many)
            except Region.DoesNotExist:
                pass

        context['category'] = self.category
        context['children'] = self.category.get_children_with_products()
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
        product = Product.objects.get(slug=self.kwargs.get('slug'))
        phone = self.request.POST.get('phone')
        order = Order(
            phone=phone,
            product=product,
        )
        order.save()

        api_ip_url = 'http://ip-api.com/json/{ip}'.format(
            ip=request.META.get('REMOTE_ADDR')
        )

        r = requests.get(api_ip_url)
        ip_data = r.json()

        bot = TelegramBot.objects.first()
        users = TelegramUser.objects.filter(send_message=True)

        text = '''
            📢 Заказ консультации по товару 👉 {product} \n\n
            📱 Телефон: {phone} \n
            🔗 Ссылка на товар {site_url}{address} \n\n
            🌍 {country} -> {city}
        '''.format(
                product=product.title,
                phone=phone,
                site_url=SITE_URL,
                address=product.get_absolute_url(),
                city=ip_data.get('city'),
                country=ip_data.get('country'),
            )

        telegram = Telegram(bot.token)
        for user in users:
            telegram.send_message(user.user_id, text)
            telegram.send_location(user.user_id, ip_data.get('lat'), ip_data.get('lon'))

        return JsonResponse({'status': 'true'})


class ManufacturerListView(ListView):
    template_name = ''
    context_object_name = 'manufacturers'
    model = Manufacturer


class ManufacturerDetailView(DetailView):
    template_name = 'catalog/manufacturer-detail.html'
    context_object_name = 'manufacturer'
    model = Manufacturer
