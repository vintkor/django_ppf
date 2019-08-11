import requests
from django.http import JsonResponse
from django.views.generic import ListView, FormView
from catalog.forms import OrderForm
from telegram_bot.models import TelegramBot, TelegramUser
from telegram_bot.utils import Telegram
from .models import SolProduct
from django.conf import settings


class SolProductListView(ListView):
    template_name = 'solutions/solutions_list_view.html'
    model = SolProduct
    context_object_name = 'solutions'


class SolProductDetailView(FormView):
    template_name = 'solutions/solutions_detail_view.html'
    model = SolProduct
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(SolProductDetailView, self).get_context_data()
        context['solution'] = SolProduct.objects.prefetch_related(
            'offers__variants__products').get(slug=self.kwargs['slug'])
        return context

    def post(self, request, slug):
        product = SolProduct.objects.get(slug=self.kwargs['slug'])
        phone = self.request.POST.get('phone')

        api_ip_url = 'http://ip-api.com/json/{ip}'.format(
            ip=request.META.get('REMOTE_ADDR')
        )

        r = requests.get(api_ip_url)
        ip_data = r.json()

        bot = TelegramBot.objects.first()
        users = TelegramUser.objects.filter(send_message=True)

        text = '''
            📢 Заказ консультации по товару ГОТОВЫЕ РЕШЕНИЯ 👉 {product} \n\n
            📱 Телефон: {phone} \n
            🔗 Ссылка на товар {site_url}{address} \n\n
            🌍 {country} -> {city}
        '''.format(
            product=product.title,
            phone=phone,
            site_url=settings.SITE_URL,
            address=product.get_absolute_url(),
            city=ip_data.get('city'),
            country=ip_data.get('country'),
        )

        telegram = Telegram(bot.token)
        for user in users:
            telegram.send_message(user.user_id, text)
            telegram.send_location(user.user_id, ip_data.get('lat'), ip_data.get('lon'))

        return JsonResponse({'status': 'true'})
