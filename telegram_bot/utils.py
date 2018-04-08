from django_ppf.settings import TELEGRAM_API_URL
import requests


class Telegram:

    def __init__(self, token):
        self.url = TELEGRAM_API_URL
        self.token = token

    def send_message(self, user_id, text):
        data = {
            "chat_id": user_id,
            "text": text,
            "disable_web_page_preview": 0,
        }

        r = requests.post(
            url='{}bot{}/sendMessage'.format(self.url, self.token),
            json=data,
        )
        # TODO сделать проверку на ответ запроса
        return True
