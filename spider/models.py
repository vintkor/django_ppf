from django.db import models
import jsonfield


class Source(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    rules = jsonfield.JSONField()
    for_assistant = models.BooleanField(default=True)
    active = models.BooleanField()

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.title
