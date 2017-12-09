from django.views.generic import ListView, DetailView, View
from .models import Region, ObjectPPF
from catalog.models import Category
from django.shortcuts import render
from django.http import JsonResponse


class RegionRootView(View):
    template_name = 'geo/geo-root.html'

    def get(self, request, *args, **kwargs):
        regions_all = Region.objects.filter(code__iregex='UA')
        regions = [item for item in regions_all if item.count_objects() > 0]
        categories = Category.objects.filter(level=0)
        context = {
            'regions': regions,
            'categories': categories,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        id = Region.objects.get(code=code).id
        return JsonResponse({'id': id})


class RegionListView(ListView):
    template_name = 'geo/region-list.html'
    context_object_name = 'region'
    model = Region

    def get_queryset(self):
        category = Region.objects.get(pk=self.kwargs.get('pk'))
        return category


class ObjectPPFDetailView(DetailView):
    template_name = 'geo/object-detail.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        queryset = ObjectPPF.objects.prefetch_related('objectimage_set').get(pk=self.kwargs.get('pk'))
        return queryset
