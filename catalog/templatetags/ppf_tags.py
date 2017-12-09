from django import template
from news.models import News


register = template.Library()


@register.inclusion_tag('django_ppf/partials/_last-news-tag.html')
def last_news():
    news = News.objects.all()[:5]
    return {'last_news': news}
