from django import template
from news.models import News
from geo.models import ObjectPPF
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category

register = template.Library()


@register.inclusion_tag('django_ppf/partials/_last-news-tag.html')
def last_news():
    news = News.objects.all()[:5]
    return {'last_news': news}


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('django_ppf/partials/_favorite-objects-tag.html')
def favorite_objects():
    objects = ObjectPPF.objects.prefetch_related('objectimage_set').filter(favorite=True)[:5]
    return {'objects': objects}


@register.inclusion_tag('catalog/partials/_catalog-list__breadcrumbs.html')
def catalog_breadcrumbs(category, product_title=False, root_name=False, root_route_name=False):
    pages = [i for i in category.get_ancestors(ascending=False, include_self=True)]
    context = dict()

    if product_title:
        context['pages'] = pages
        context['product'] = product_title
    else:
        context['pages'] = pages[:-1]
        context['product'] = pages[-1]

    context['root_name'] = root_name
    context['root_link'] = reverse(root_route_name)

    return context


@register.inclusion_tag('catalog/partials/_breadcrumbs-news.html')
def news_breadcrumbs(nav_item=False, nav_item_rout=False, page=False):
    context = dict()
    context['nav_item'] = nav_item

    if nav_item_rout:
        context['nav_item_route'] = reverse(nav_item_rout)

    context['page'] = page
    return context


@register.inclusion_tag('catalog/partials/_profile.html')
def profile(user):
    return {'user': User.objects.select_related('profile').get(id=user.id)}
