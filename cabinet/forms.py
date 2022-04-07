from django import forms

from .models import Car, CarBrand, Driver


class CarAddForm(forms.ModelForm):

    registration_number = forms.CharField(label='Номер:')
    brand = forms.ModelChoiceField(label='Марка:', queryset=CarBrand.objects.all()
                                   )
    region_code = forms.CharField(label='Код региона:')

    last_inspection = forms.DateField(label='Последний осмотр:')

    owner = forms.ModelChoiceField(label='Закрепить за:', queryset=Driver.objects.all())

    class Meta:
        model = Car
        fields = ('registration_number', 'brand', 'region_code', 'last_inspection', 'owner',)
