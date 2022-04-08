import union as union
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .filters import CarFilter
from .forms import CarAddForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView, CreateView

from .services import filtration_car


class Context():
    '''Получение контекста'''

    def get_car_brands(self):
        return CarBrand.objects.all()

    def get_drivers(self):
        return Driver.objects.all()

    def get_regions(self):
        return Car.objects.all().values('region_code').distinct()

    def get_types_of_app(self):
        return TypeOfAppl.objects.all()

class CarsView(Context,ListView):
    """Вывод всех автомобилей"""
    template_name = "cars.html"
    context_object_name = "cars"
    success_url = '/cars'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarAddForm(initial={
            'registration_number': 'G155PP'
        })
        return context

    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form = form.save(commit=False)
    #         form.registration_number = form.registration_number.upper()
    #         form.save()
    #         print("SAVE!")
    #         return HttpResponseRedirect(self.success_url)
    #     else:
    #         return

    def get_queryset(self):
        if len(self.request.GET) == 0:
            return Car.objects.all()
        else:
            return filtration_car(self.request.GET)


class CarCreateView(Context, CreateView):
    '''добавление нового автомобиля'''
    template_name = "cars.html"
    # context_object_name = "cars"
    success_url = '/cars'
    form_class = CarAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = filtration_car(self.request.GET)
        return context
    
    # def form_invalid(self, form):
    #     print(form.errors)
    #     return super(CarCreateView, self).form_invalid(form)
    
class DriversView(Context, ListView):
    template_name = 'drivers.html'
    queryset = Driver.objects.all()
    context_object_name = "drivers"
    

    # def setup(self, request, *args, **kwargs):
    #     print(self.queryset)
    #     super(DriversView, self).setup(request, *args, **kwargs)