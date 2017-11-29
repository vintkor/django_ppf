from django.views.generic import View
from catalog.models import Category
from django.shortcuts import render


class HomeView(View):

    def get(self, request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'django_ppf/home.html', context)
