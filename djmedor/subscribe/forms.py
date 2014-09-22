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
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        self._person_fields = [f.name for f in Person._meta.fields]
        self._person_fields.remove(u'id')
        self._person_fields = tuple(self._person_fields)
        _initial = model_to_dict(instance.person, _fields) if instance is not None else {}
        kwargs['initial'] = _initial
        super(CooperationForm, self).__init__(*args, **kwargs)
        self.fields.update(fields_for_model(Person, self._person_fields))
        self.fields['birth_date'].widget.attrs["placeholder"] = "JJ/MM/AAAA"
        self.fields['phone_number'].widget.attrs["placeholder"] = "+32 "

    class Meta:
        model = Cooperation
        exclude = ('person',)

    def save(self, *args, **kwargs):
        d = {}
        for key in self._person_fields:
            d[key] = self.cleaned_data[key]

        person = Person(**d)
        person.save()
        self.instance.person = person

        cooperation = super(CooperationForm, self).save(*args,**kwargs)
        return cooperation
