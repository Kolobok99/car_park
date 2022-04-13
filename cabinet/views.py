import random

import union as union
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from itertools import chain

from django.views import View
from django.views.generic.edit import FormMixin

from .filters import CarFilter
from .forms import *
from .models import *

from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView, DetailView

from .services import filtration_car, filtration_driver, filtration_document, Context, filtration_cards, filtration_apps


class CarsView(Context, ListView):
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


class CarCreateView(Context,  CreateView):
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

    
class DriversView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'drivers.html'
    # queryset = Driver.objects.all()
    # context_object_name = 'drivers'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['drivers'] = MyUser.objects.filter(role='d')
        else:
            context['drivers'] = filtration_driver(self.request.GET)
        return context


    # def setup(self, request, *args, **kwargs):
    #     print(self.)
    #     super(DriversView, self).setup(request, *args, **kwargs)


class DocumentsView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'documents.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_docs'] = super(DocumentsView, self).get_all_docs()
        else:
            context['all_docs'] = filtration_document(self.request.GET)
        return context

class CardCreateView(Context, LoginRequiredMixin, CreateView):
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

class AplicationsView(Context, TemplateView):
    """Вывод заявок"""
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_apps'] = Application.objects.all()
        else:
            context['all_apps'] = filtration_apps(self.request.GET)

        return context


# class CartUpdateView(UpdateView):
#     template_name = 'cards.html'
#     success_url = '/cards'
#     form_class =

class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = DriverCreateForm
    success_url = '/cars'

class CarView(FormMixin, DetailView):
    '''Отображение страницы машины'''

    template_name = 'car.html'
    slug_field = 'registration_number'
    form_class = AppCreateForm

    def get_success_url(self):
        return f"{self.kwargs['slug']}"

    def get_queryset(self):
        return Car.objects.filter(registration_number=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            print(1)
            form.save()
            return self.form_valid(form)
        else:
            print(0)
            return self.form_invalid(form)

    # def form_invalid(self, form):
    #     print("FAIL:-(")
    #     super(CarView, self).form_invalid(form)
    # def get_context_data(self, **kwargs):
    #     context = super(CarView, self).get_context_data(**kwargs)
    #     context['form_app'] = AppCreateForm
    #
    #     return context

# class AppCreateView(FormView):
#     """Создании заявки на автомобиль"""
#
#     success_url = '/cars'
#     form_class = AppCreateForm
#
#     def get_initial(self):
#         return {
#                 'car': self.request.user,
#                 'owner': Car.objects.get(registration_number=self.kwargs['slug'])
#             }
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user_id'] = self.request.user.id
    #     kwargs['registration_number'] =self.kwargs['slug']
    #
    #     print(f"{kwargs=}")
    #     return kwargs

    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.owner = MyUser.objects.get(pk=self.request.user.id)
    #     instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
    #
    #     instance.save()
    #     return instance


class AccountView(TemplateView):
    '''Обработка страницы ЛК'''

    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['user'] = MyUser.objects.get(pk=self.request.user.pk)

        return context