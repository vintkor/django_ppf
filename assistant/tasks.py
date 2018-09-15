from django_ppf.celery import app
from assistant.utils import update_mizol_prices, import_parameters_form_prom


@app.task(name='assistant.update_mizol_prices_task')
def update_mizol_prices_task(filename):
    update_mizol_prices(filename)


@app.task(name='assistant.import_parameters_form_prom')
def import_parameters_form_prom_task(filename):
    import_parameters_form_prom(filename)
