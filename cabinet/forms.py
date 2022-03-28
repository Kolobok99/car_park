from django.forms import ModelForm

from .models import Car

class CarMainForm(ModelForm):
    class Meta:
        model = Car
        fields = (
            'brand',
            # 'registration_number',
            # 'region_code',
            # 'owner'
        )
