from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput

from checks.models import Location


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
        formatted_name = self.cleaned_data['name'].capitalize()

        if Location.objects.filter(name=formatted_name).exists():
            raise ValidationError('Такой район уже есть')
        return formatted_name
