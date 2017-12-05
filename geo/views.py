from django.views.generic import ListView, DetailView
from .models import Region, ObjectPPF


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
