from subscribe.forms import CooperateForm
from django.views.generic.edit import FormView


class CooperateView(FormView):
    template_name = 'subscribe/cooperate.html'
    form_class = CooperateForm
    success_url = '/thanks/'
