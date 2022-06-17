import datetime
from pprint import pprint

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Select, SelectDateWidget, CheckboxInput, CheckboxSelectMultiple, \
    RadioSelect, HiddenInput, DateInput, ModelChoiceField

from checks.models import Location, Object, ControlEvent, Result


class CreateLocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Название объекта',
                'size': 40,
                },
            )
        }

    def clean_name(self):
        formatted_name = self.cleaned_data['name']

        if Location.objects.filter(name=formatted_name).exists():
            raise ValidationError('Такой район уже есть')
        return formatted_name


class CreateObjectForm(ModelForm):

    class Meta:
        model = Object
        fields = ['name', 'location']
        labels = {
            'name': '',
            'location': '',
        }
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Название объекта',
            }),
            'location': Select(attrs={
                'placeholder': 'Выберите район',
                'width': 50}
            )
        }

    def clean(self):
        name = self.cleaned_data['name']
        location = self.cleaned_data['location']

        if Object.objects.filter(name=name, location=location).exists():
            raise ValidationError('Такой объект существует')

        return self.cleaned_data


class ControlEventForm(ModelForm):
    object = ModelChoiceField(queryset=Object.objects.order_by('location'), label='')

    class Meta:
        model = ControlEvent
        fields = ['date', 'object']
        labels = {
            'date': '',
        }
        widgets = {
            'date': DateInput(
                format=('%d.%m.%Y'),
                attrs = {'type': 'date'}
            ),
            'object': Select()
        }

    def clean_date(self):
        if self.cleaned_data['date'] > datetime.date.today():
            raise ValidationError('Вводимая Вами дата ещё не наступила!')

        return self.cleaned_data['date']
