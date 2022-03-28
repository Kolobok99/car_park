from django.db.models import Q
from django.shortcuts import render

from .filters import CarFilter
from .forms import CarMainForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView

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

class FilterCars(Context, ListView):
    """фильтрация авто"""
    template_name = 'index.html'
    context_object_name = "cars"
    def get_queryset(self):
        reg_number = self.request.GET.getlist('registration_number')
        if len(reg_number) != 0:
            reg_number = '`'
        else:
            reg_number = " ".join(reg_number)
        query_set= Car.objects.filter(
            Q(registration_number__icontains=reg_number) |
            Q(brand__in = self.request.GET.getlist('brand')) |
            Q(owner__in=self.request.GET.getlist('driver')) |
            Q(region_code__in=self.request.GET.getlist('region'))

        )
        # print(query_set)
        return query_set

class CarsView(Context,ListView):
    """Вывод всех автомобилей"""
    template_name = "index.html"
    queryset = Car.objects.all()
    context_object_name = "cars"
    #
    # def setup(self, request, *args, **kwargs):
    #     print(self.get_types_of_app())
    #     super(CarsView, self).setup(request, *args, **kwargs)

def CarFilterView(request):
    cars = CarFilter(request.GET, queryset=Car.objects.all())
    cars_brand = CarBrand.objects.all()
    context = {
        "cars": cars,
        "cars_brand":cars_brand,
    }

    return render(request, 'index.html', context=context)
