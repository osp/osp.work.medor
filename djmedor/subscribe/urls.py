from django.conf.urls import patterns, url
from subscribe.views import CooperateView


urlpatterns = patterns('',
    url(r'^$', CooperateView.as_view(), name='cooperate'),
)
