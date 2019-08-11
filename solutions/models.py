from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from catalog.models import Category, Product
from sorl.thumbnail import ImageField
from django.utils.crypto import get_random_string


def set_image_name(instanse, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/catalog/solutions/{}.{}'.format(name, ext)
    return path


class SolProduct(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name=_('Category'), null=True, related_name='solproducts')
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(null=True, max_length=170, unique=True)
    image = ImageField(verbose_name=_('Image'), upload_to=set_image_name, blank=True, null=True)
    meta_description = models.CharField(max_length=200, verbose_name=_('META Description'), blank=True, null=True)
    meta_keywords = models.CharField(max_length=200, verbose_name=_('META Keywords'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    is_active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title[:150]

    def get_absolute_url(self):
        return reverse('solutions:detail', args=[str(self.slug)])


class SolOffer(models.Model):
    product = models.ForeignKey(SolProduct, on_delete=models.SET_NULL, related_name='offers', null=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    image = ImageField(verbose_name=_('Image'), upload_to=set_image_name, blank=True, null=True)

    class Meta:
        verbose_name = 'Оффер'
        verbose_name_plural = 'Офферы'

    def __str__(self):
        return f'{self.product.title} > {self.title[:150]}'


class SolVariant(models.Model):
    offer = models.ForeignKey(SolOffer, related_name='variants', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=_('Price'))
    products = models.ManyToManyField(Product, verbose_name=_('Products'))

    class Meta:
        verbose_name = 'Ваниант'
        verbose_name_plural = 'Ванианты'

    def __str__(self):
        return self.title[:150]
