import django_filters
from django.forms import TextInput
from django_filters.widgets import RangeWidget

from cabinet.models import Car


class CarFilter(django_filters.FilterSet):
    '''Фильтр машин'''
    registration_number = django_filters.CharFilter(widget=TextInput(attrs={
        'placeholder': 'номер',
        'class':'foo',
    }), lookup_expr='icontains')

    # brand = django_filters.

    class Meta:
        model = Car
        fields = ['registration_number', 'brand']
        # widgets = {
        #     'registration_number': TextInput(attrs={'placeholder': 'номер'})
        # }
