from django import forms
from subscribe.models import Cooperator


class CooperateForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Cooperator


class ConfirmForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    confirm = forms.BooleanField()
