from django_ppf.celery import app
# from awards.utils import start_point_awadr
from assistant.utils import update_mizol_prices


@app.task(name='assistant.update_mizol_prices_task')
def update_mizol_prices_task(filename):
    update_mizol_prices(filename)
