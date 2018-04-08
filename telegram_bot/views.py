from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import TelegramUser, TelegramBot
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, HttpResponse
import json


@method_decorator(csrf_exempt, name='dispatch')
class WebHookUpdate(View):
    data_info = None

    def get_user_id(self):
        return self.data_info['message']['from']['id']

    def get_username(self):
        return self.data_info['message']['from']['username']

    def save_user(self):
        user_id = int(self.get_user_id())
        try:
            TelegramUser.objects.get(user_id=user_id)
        except TelegramUser.DoesNotExist:
            new_user = TelegramUser(username=self.get_username(), user_id=user_id)
            new_user.save()

    def post(self, request, token):

        try:
            bot = TelegramBot.objects.get(token=token)
        except TelegramBot.DoesNotExist:
            return HttpResponseForbidden()

        self.data_info = json.loads(request.body.decode('utf-8'))
        self.save_user()

        return HttpResponse()
