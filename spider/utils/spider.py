from spider.models import Source
from .errors import ConfigError
from . import handlers


class Spider:

    def __init__(self):
        self.sourses = None

    @classmethod
    def init(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self.sourses = Source.objects.filter(active=True)
        return self

    @staticmethod
    def handler(type_):
        type__ = type_.lower()
        if type__ == 'VitanHandler'.lower():
            return handlers.VitanHandler
        elif type__ == 'OptovikHandler'.lower():
            return handlers.OptovikHandler
        else:
            raise ConfigError('Handler for type {} not found'.format(type_))

    def start_parse(self):
        print('Start parsing...')
        for sourse in self.sourses:
            try:
                handler = self.handler(sourse.rules['type'])(sourse=sourse)
                handler.parse()
            except ConfigError as err:
                print(str(err))
