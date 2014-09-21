from django.conf.urls import patterns, url
from subscribe.views import CooperationWizardView


urlpatterns = patterns('',
    url(r'^$', CooperationWizardView.as_view(), name='cooperate-wizard'),
)
