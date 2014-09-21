from django.conf.urls import patterns, url
from subscribe.views import CooperateView, CooperateWizard


urlpatterns = patterns('',
    url(r'^$', CooperateWizard.as_view(), name='cooperate-wizard'),
    url(r'^cooperate$', CooperateView.as_view(), name='cooperate'),
)
