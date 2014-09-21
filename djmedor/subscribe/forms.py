from django.forms import ModelForm
from subscribe.models import Cooperator


class CooperateForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Cooperator
