from __future__ import absolute_import, unicode_literals
from django_ppf.celery import app
from assistant.utils import (
    update_prices,
    import_parameters_form_prom,
    parse_mizol,
)


@app.task(name='assistant.update_mizol_prices_task')
def update_mizol_prices_task(filename, vendor_name):
    update_prices(filename, vendor_name)


@app.task(name='assistant.import_parameters_form_prom')
def import_parameters_form_prom_task(filename):
    import_parameters_form_prom(filename)


@app.task(name='assistant.add_new_products_by_mizol')
def add_new_products_by_mizol():
    parse_mizol()


@app.task
def update_horoz_task():
    from assistant.utils import ParseHoroz
    ph = ParseHoroz(link='https://horozua.com/index.php?route=feed/yandex_yml', my_currency_code='USD')
    ph.set_products()
    ph.add_or_update_products_in_db()
