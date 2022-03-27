from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView


class CarsView(TemplateView):
    """Вывод всех автомобилей"""
    template_name = "index.html"