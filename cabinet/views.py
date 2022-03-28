from django.shortcuts import render

from .filters import CarFilter
from .forms import CarMainForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView

class Context():
    '''Получение контекста'''

    def get_car_brands(self):
        return CarBrand.objects.all()



class CarsView(ListView):
    """Вывод всех автомобилей"""
    template_name = "index.html"
    queryset = Car.objects.all()
    context_object_name = "cars"

def CarFilterView(request):
    cars = CarFilter(request.GET, queryset=Car.objects.all())
    cars_brand = CarBrand.objects.all()
    context = {
        "cars": cars,
        "cars_brand":cars_brand,
    }

    return render(request, 'index.html', context=context)
