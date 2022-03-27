from .forms import CarMainForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView


class CarsView(ListView, FormView):
    """Вывод всех автомобилей"""
    template_name = "index.html"
    queryset = Car.objects.all()
    context_object_name = "cars"

    form_class = CarMainForm()



