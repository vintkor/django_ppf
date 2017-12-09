from django.conf.urls import url
from .views import RegionListView, ObjectPPFDetailView, RegionRootView

urlpatterns = [
    # url(r'^$', QuestionsList.as_view(), name='all-questions'),
    # url(r'^question/(?P<pk>\d+)/$', QuestionsDetail.as_view(), name='single-question'),
    url(r'^$', RegionRootView.as_view(), name='geo-root'),
    url(r'^region/(?P<pk>\d+)/$', RegionListView.as_view(), name='geo-region'),
    url(r'^object/(?P<pk>\d+)/$', ObjectPPFDetailView.as_view(), name='geo-object'),
    # url(r'^add/$', NewQuestionView.as_view(), name='add-question'),
]