from subscribe.forms import CooperateForm, ConfirmForm
from django.views.generic.edit import FormView

from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import CookieWizardView



class CooperateView(FormView):
    template_name = 'subscribe/cooperate.html'
    form_class = CooperateForm
    success_url = '/thanks/'


class CooperateWizard(CookieWizardView):
    template_name = "subscribe/wizard.html"
    form_list = [CooperateForm, ConfirmForm]

    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
