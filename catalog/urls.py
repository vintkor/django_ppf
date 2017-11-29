from django.conf.urls import url
from .views import CategoryListView

urlpatterns = [
    # url(r'^$', QuestionsList.as_view(), name='all-questions'),
    # url(r'^question/(?P<pk>\d+)/$', QuestionsDetail.as_view(), name='single-question'),
    url(r'^category/(?P<pk>\d+)/$', CategoryListView.as_view(), name='catalog-category'),
    # url(r'^add/$', NewQuestionView.as_view(), name='add-question'),
]