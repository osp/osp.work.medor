from subscribe.forms import CooperationForm, ConfirmForm
from django.core.mail import send_mail
from django.views.generic.edit import FormView

from django.shortcuts import render
from django.contrib.formtools.wizard.views import CookieWizardView


COOPERATION_FORMS = [
    CooperationForm,
    ConfirmForm,
]

COOPERATION_TEMPLATES = [
    "subscribe/cooperation-registration.html",
    "subscribe/cooperation-confirmation.html",
]


class CooperationWizardView(CookieWizardView):
    form_list = COOPERATION_FORMS

    def get_context_data(self, form, **kwargs):
        context = super(CooperationWizardView, self).get_context_data(form=form, **kwargs)
        print(self.steps.current)
        if self.steps.current == '1':
            context.update({
                'infos': self.get_cleaned_data_for_step("0"),
                'total': self.get_cleaned_data_for_step("0")['share_number'] * 20
            })
        return context

    def get_template_names(self):
        return [COOPERATION_TEMPLATES[int(self.steps.current)]]

    def done(self, form_list, form_dict, **kwargs):
        form_list[0].save()
        #subject = form.cleaned_data['subject']
        #message = form.cleaned_data['message']
        #sender = form.cleaned_data['sender']
        #cc_myself = form.cleaned_data['cc_myself']

        #recipients = ['info@example.com']

        #if cc_myself:
            #recipients.append(sender)

        #send_mail(subject, message, sender, recipients)

        return render(self.request, 'subscribe/cooperation-done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
