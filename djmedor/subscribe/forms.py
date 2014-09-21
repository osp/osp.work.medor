from django import forms
from django.forms.models import model_to_dict, fields_for_model
from subscribe.models import Person, Cooperation, Subscription


class ConfirmForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    confirm = forms.BooleanField()


class CooperationForm(forms.ModelForm):
    """
    http://stackoverflow.com/questions/15889794/creating-one-django-form-to-save-two-models
    """
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        _fields = [f.name for f in Person._meta.fields]
        _fields.remove(u'id')
        _fields = tuple(_fields)
        _initial = model_to_dict(instance.person, _fields) if instance is not None else {}
        kwargs['initial'] = _initial
        super(CooperationForm, self).__init__(*args, **kwargs)
        self.fields.update(fields_for_model(Person, _fields))

    class Meta:
        model = Cooperation
        exclude = ('person',)

    def save(self, *args, **kwargs):
        u = self.instance.person
        print(self._fields)
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        cooperation = super(CooperationForm, self).save(*args,**kwargs)
        return cooperation
