from django_ppf.celery import app
from assistant.utils import (
    update_mizol_prices,
    import_parameters_form_prom,
    parse_mizol,
    ParseHoroz,
)


@app.task(name='assistant.update_mizol_prices_task')
def update_mizol_prices_task(filename):
    update_mizol_prices(filename)


@app.task(name='assistant.import_parameters_form_prom')
def import_parameters_form_prom_task(filename):
    import_parameters_form_prom(filename)


@app.task(name='assistant.add_new_products_by_mizol')
def add_new_products_by_mizol():
    parse_mizol()


@app.task(name='update_horoz_task')
def update_horoz_task():
    ph = ParseHoroz(link='https://horozua.com/index.php?route=feed/yandex_yml', my_currency_code='USD')
    ph.set_products()
    ph.add_or_update_products_in_db()
