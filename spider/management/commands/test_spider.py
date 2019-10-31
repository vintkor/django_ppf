from django.core.management.base import BaseCommand, CommandError
from spider.utils.spider import Spider


class Command(BaseCommand):

    def handle(self, *args, **option):
        print('-'*150)
        print('Its work')

        spider = Spider.init()
        spider.start_parse()
