import union as union
from django.db.models import Q
from django.shortcuts import render

from .filters import CarFilter
from .forms import CarAddForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView, CreateView


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
    # queryset = Car.objects.all()
    context_object_name = "cars"

    form_class = CarAddForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarAddForm()
        return context

    def get_queryset(self):
        if len(self.request.GET) == 0:
            return Car.objects.all()
        else:
            reg_number = self.request.GET.get('registration_number')
            if reg_number == '': reg_number = '`'
            # print(f"{reg_number=}")

            query_set = Car.objects.filter(
                Q(registration_number__icontains=reg_number) |
                Q(brand__in=self.request.GET.getlist('brand')) |
                Q(owner__in=self.request.GET.getlist('driver')) |
                Q(region_code__in=self.request.GET.getlist('region')) |
                (Q(applications__type_of_id__in=self.request.GET.getlist('type_of_app')) & Q(
                    applications__is_active=True))

            )

            return query_set.distinct()
        # print(self.request.GET)
        # return Car.objects.all()

class CarCreateView(CreateView):
    '''добавление нового автомобиля'''
    template_name = "cars.html"
    # queryset = Car.objects.all()
    context_object_name = "cars"
    form_class = CarAddForm

    success_url = 'cars'




class DriversView(Context, ListView):
    template_name = 'drivers.html'
    queryset = Driver.objects.all()
    context_object_name = "drivers"

    # def setup(self, request, *args, **kwargs):
    #     print(self.queryset)
    #     super(DriversView, self).setup(request, *args, **kwargs)