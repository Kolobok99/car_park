from django.shortcuts import render
from .models import *
# Create your views here.
from django.views.generic import ListView, TemplateView


class CarsView(ListView):
    """Вывод всех автомобилей"""
    template_name = "index.html"
    queryset = Car.objects.all()
    context_object_name = "cars"

    # def get_context_data(self, *, object_list=None, **kwargs):
