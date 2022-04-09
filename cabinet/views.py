import random

import union as union
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from itertools import chain
from .filters import CarFilter
from .forms import CarAddForm, FuelCardAddForm
from .models import *

from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView

from .services import filtration_car, filtration_driver, filtration_document, Context, filtration_cards


class CarsView(Context,ListView):
    """Вывод всех автомобилей"""
    template_name = "cars.html"
    context_object_name = "cars"
    success_url = '/cars'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CarAddForm(initial={
#             'registration_number': 'G155PP'
#         })
#         return context
#
#     # def post(self, request):
#     #     form = self.form_class(request.POST)
#     #     if form.is_valid():
#     #         form = form.save(commit=False)
#     #         form.registration_number = form.registration_number.upper()
#     #         form.save()
#     #         print("SAVE!")
#     #         return HttpResponseRedirect(self.success_url)
#     #     else:
#     #         return
#
#     def get_queryset(self):
#         if len(self.request.GET) == 0:
#             return Car.objects.all()
#         else:
#             return filtration_car(self.request.GET)


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

    
class DriversView(Context, TemplateView):
    template_name = 'drivers.html'
    # queryset = Driver.objects.all()
    # context_object_name = 'drivers'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['drivers'] = Driver.objects.all()
        else:
            context['drivers'] = filtration_driver(self.request.GET)
        return context


    # def setup(self, request, *args, **kwargs):
    #     print(self.)
    #     super(DriversView, self).setup(request, *args, **kwargs)


class DocumentsView(Context, TemplateView):
    template_name = 'documents.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_docs'] = super(DocumentsView, self).get_all_docs()
        else:
            context['all_docs'] = filtration_document(self.request.GET)
        return context

class CardCreateView(Context, CreateView):
    """Создание и вывод топилвных карт"""

    template_name = 'cards.html'
    success_url = '/cards'
    form_class = FuelCardAddForm

    def get_context_data(self, **kwargs):
        context = super(CardCreateView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_cards'] = FuelCard.objects.exclude(owner=None)
        else:
            context['all_cards'] = filtration_cards(self.request.GET)
        return context

# class CartUpdateView(UpdateView):
#     template_name = 'cards.html'
#     success_url = '/cards'
#     form_class =

