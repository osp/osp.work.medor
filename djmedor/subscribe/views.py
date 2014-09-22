# -*- coding: utf-8 -*-
from subscribe.forms import CooperationForm, SubscriptionForm, ConfirmForm
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from django.template.loader import render_to_string

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


SUBSCRIPTION_FORMS = [
    SubscriptionForm,
    ConfirmForm,
]

SUBSCRIPTION_TEMPLATES = [
    "subscribe/subscription-registration.html",
    "subscribe/subscription-confirmation.html",
]


class CooperationWizardView(CookieWizardView):
    form_list = COOPERATION_FORMS

    def get_context_data(self, form, **kwargs):
        context = super(CooperationWizardView, self).get_context_data(form=form, **kwargs)
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

        subject = "Médor SCRL FS. Détails de votre paiement"
        message = render_to_string('subscribe/cooperation-email.txt', {
                'data': form_list[0].cleaned_data,
                'amount': form_list[0].cleaned_data['share_number'] * 20,
                'communication': form_list[0].instance.communication()
            })
        sender = "medor@medor.coop"

        recipients = ['alexandre@stdin.fr']

        send_mail(subject, message, sender, recipients)

        return render(self.request, 'subscribe/cooperation-done.html', {
            'communication': form_list[0].instance.communication(),
            'form_data': [form.cleaned_data for form in form_list],
        })


class SubscriptionWizardView(CookieWizardView):
    form_list = SUBSCRIPTION_FORMS

    def get_context_data(self, form, **kwargs):
        context = super(SubscriptionWizardView, self).get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            context.update({
                'infos': self.get_cleaned_data_for_step("0"),
            })
        return context

    def get_template_names(self):
        return [SUBSCRIPTION_TEMPLATES[int(self.steps.current)]]

    def done(self, form_list, form_dict, **kwargs):
        form_list[0].save()

        subject = "Médor SCRL FS. Détails de votre paiement"
        message = render_to_string('subscribe/cooperation-email.txt', {
                'data': form_list[0].cleaned_data,
                'amount': 60,
                'communication': form_list[0].instance.communication()
            })
        sender = "medor@medor.coop"

        recipients = ['alexandre@stdin.fr']

        send_mail(subject, message, sender, recipients)

        return render(self.request, 'subscribe/cooperation-done.html', {
            'communication': form_list[0].instance.communication(),
            'form_data': [form.cleaned_data for form in form_list],
        })
