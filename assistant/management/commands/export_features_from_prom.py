from django.core.management.base import BaseCommand, CommandError
import csv
from assistant.models import Parameter, Product


class ExportFeatures:

    def __init__(self, filename):
        self._filename = filename
        self.products = []

    def make_product_list(self):
        with open(self._filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    continue
                self.products.append([
                    i for index, i in enumerate(row) if index in range(34, len(row)+3) or index == 0
                ])

    def save_parameters(self):
        temp = []
        for product in self.products:
            temp_list = []
            count_parameters = (len(product) - 1)//3
            if count_parameters > 0:
                x, y, z = 1, 3, 2
                for i in range(count_parameters):
                    temp_list.append((product[x], product[y] + ' ' + product[z]))
                    x, y, z = x + 3, y + 3, z + 3
                # print('')
            temp.append({product[0]: temp_list})

        for i in temp:
            for product_code, v in i.items():
                # print(product_code)
                try:
                    p = Product.objects.get(code=product_code)
                    param_list = []
                    for j in v:
                        # print('_'*8, j)
                        if len(j[1]) > 1:
                            param_list.append(Parameter(
                                product=p,
                                parameter=j[0],
                                value=j[1],
                            ))
                    Parameter.objects.bulk_create(param_list)
                except:
                    pass



class Command(BaseCommand):
    # help = 'Импорт товаров без категорий из файла экспорта prom.ua'

    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', type=str, help='Path to file on this computer')

    def handle(self, *args, **option):
        print('-'*160)
        print(' ')
        print('_'*160)
        export = ExportFeatures('prom.csv')
        export.make_product_list()
        export.save_parameters()
