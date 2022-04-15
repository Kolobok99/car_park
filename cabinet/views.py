from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormMixin

from .forms import *
from .models import *

from django.views.generic import ListView, TemplateView, CreateView, DetailView

from cabinet.services.services import filtration_car, filtration_driver, filtration_document, Context, filtration_cards, \
    filtration_apps
from .services.multiforms import MultiFormsView


class CarsView(Context, ListView):
    """Вывод всех автомобилей"""

    template_name = "cars.html"
    context_object_name = "cars"
    success_url = '/cars'


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


class DriversView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'drivers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['drivers'] = MyUser.objects.filter(role='d')
        else:
            context['drivers'] = filtration_driver(self.request.GET)
        return context


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


class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = DriverCreateForm
    success_url = '/cars'


# class CarView(MultiFormsView, DetailView):
#     '''Отображение страницы машины'''
#
#     template_name = 'car.html'
#     slug_field = 'registration_number'
#
#     def get_queryset(self):
#         return Car.objects.filter(registration_number=self.kwargs['slug'])
#
#     form_class = {
#         'app_create': AppCreateForm,
#         'doc_create': AutoDocForm,
#     }
#
#     success_url = {
#         'app_create': '/',
#         'doc_create': '/',
#     }
#
#     def app_create_form_valid(self, form):
#         form_name = form.cleaned_data.get('action')
#
#         return HttpResponseRedirect(self.get_success_url(form_name))
#
#     def doc_create_form_valid(self, form):
#         form_name = form.cleaned_data.get('action')
#
#         return HttpResponseRedirect(self.get_success_url(form_name))

# form_class = AppCreateForm
#
# def get_success_url(self):
#     return f"{self.kwargs['slug']}"
#
# def get_queryset(self):
#     return Car.objects.filter(registration_number=self.kwargs['slug'])

# def post(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     form = self.get_form()
#     print(f"{form=}")
#     if form.is_valid():
#         print(1)
#         form.save()
#         return self.form_valid(form)
#     else:
#         print(0)
#         return self.form_invalid(form)

class AccountView(TemplateView):
    '''Обработка страницы ЛК'''

    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['user'] = MyUser.objects.get(pk=self.request.user.pk)

        return context


class CarView(TemplateView):
    template_name = 'car.html'

    def get_context_data(self, **kwargs):
        car = Car.objects.get(registration_number=self.kwargs['slug'])
        app_create_form = AppCreateForm()
        doc_create_form = AutoDocForm()

        context = super().get_context_data(**kwargs)
        context['car'] = car
        context['app_create_form'] = app_create_form
        context['doc_create_form'] = doc_create_form

        return context

    def post(self, request, *args, **kwargs):
        action_type = self.request.POST.get('action')
        if action_type == 'app_create':
            form = AppCreateForm(self.request.POST)
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST)
        else:
            form = None
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись добавлена!')

        return HttpResponseRedirect("")
