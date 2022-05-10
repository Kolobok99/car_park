from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin, DeletionMixin, UpdateView

from .forms import *
from .models import *

from django.views.generic import ListView, TemplateView, CreateView, DetailView

from cabinet.services.filtration import *

from cabinet.services.services import Context


class CarsCreateAndFilterView(Context, LoginRequiredMixin, CreateView):
    """
    Выводит список автомобилей
    Фильтрует автомобили
    Добавляет новый автомобиль
    """
    template_name = "cars.html"
    success_url = '/cars'
    form_class = CarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all() if not len(self.request.GET) \
            else refact3_filtration_car(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'owner-none':
            none_owner_pk = self.request.POST.getlist('owner_id')
            cars = Car.objects.filter(pk__in=none_owner_pk)
            for car in cars:
                car.owner = None
                car.save()
        else:
            return super().post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        messages.success(self.request, "Машина добавлена")
        return super().form_valid(form)

class CarView(LoginRequiredMixin, UpdateView):
    template_name = 'car.html'
    form_class = CarUpdateForm

    app_form_class = AppCreateForm
    doc_form_class = AutoDocForm

    def get_success_url(self, **kwargs):
        return self.get_object().get_absolute_url()

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action_type = self.request.POST.get('action')

        context['doc_create_form'] = self.doc_form_class(self.request.POST) \
            if action_type == 'doc_create' else self.doc_form_class()
        context['app_create_form'] = self.app_form_class(self.request.POST)\
            if action_type == 'app_create' else self.app_form_class()
        context['form'] = self.form_class(self.request.POST) \
            if action_type == 'car_update' else self.form_class(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action_type = self.request.POST.get('action')
        if action_type == 'car_update':
            form = self.form_class(self.request.POST, request.FILES, instance=self.object, car=self.get_object())
        elif action_type == 'app_create':
            form = self.app_form_class(self.request.POST, user=self.request.user, car=self.object)
        elif action_type == 'doc_create':
            form = self.doc_form_class(self.request.POST, self.request.FILES, car=self.object)
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ удален!")
            return HttpResponseRedirect("")
        if form.is_valid():
            if action_type == 'car_update':
                messages.success(self.request, "Данные машины изменены!")
            elif action_type == 'app_create':
                messages.success(self.request, "Заявка добавлена!")
            elif action_type == 'doc_create':
                messages.success(self.request, "Документ добавлен!")

            return self.form_valid(form)
        else:
            return self.form_invalid(**{action_type: form})

class DriversFilterView(Context, LoginRequiredMixin, TemplateView):
    """
    Выводит список водителей
    Фильтрует список водителей
    """
    template_name = 'drivers.html'

    def get_context_data(self, **kwargs):
        context = super(DriversFilterView, self).get_context_data(**kwargs)
        context['drivers'] = MyUser.objects.filter(role='d') if not len(self.request.GET) \
            else refact3_filtration_driver(self.request.GET)
        return context

class DriverView(LoginRequiredMixin, DetailView):
    """Страница выбранного водителя"""

    template_name = 'driver.html'
    context_object_name = 'driver'
    model = MyUser

    def get_context_data(self, **kwargs):
        context = super(DriverView, self).get_context_data(**kwargs)
        context['free_cards'] = FuelCard.objects.filter(owner__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action_type = self.request.POST.get('action')
        if action_type == 'add-card':
            card = FuelCard.objects.get(pk=request.POST.get('card'))
            card.owner = self.get_object()
            card.save()
        return HttpResponseRedirect("")

class DocumentsView(Context, LoginRequiredMixin, TemplateView):
    """
        Выводит список документов (водители+авто)
        Фильтрует список документов (водители+авто)
    """
    template_name = 'documents.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['all_docs'] = super().get_all_docs()
        else:
            if len(request_GET.getlist('aorm')) == 2:
                context['all_docs'] = list(chain(
                    refact3_filtration_documents(model=AutoDoc, get_params=request_GET),
                    refact3_filtration_documents(model=UserDoc, get_params=request_GET)
                ))
            elif request_GET.get('aorm') == 'car':
                context['all_docs'] = refact3_filtration_documents(model=AutoDoc, get_params=request_GET)
            elif request_GET.get('aorm') == 'man':
                context['all_docs'] = refact3_filtration_documents(model=UserDoc, get_params=request_GET)

            context['get_parametrs'] = request_GET.items()
        return context

class CardFilterAndCreateView(Context, LoginRequiredMixin, CreateView):
    """
        Выводит список топливных карт
        Фильтрует топливные карты
        Добавляет новые топливные карты
    """
    template_name = 'cards.html'
    success_url = '/cards'
    form_class = FuelCardAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_cards'] = FuelCard.objects.all() if not len(self.request.GET) \
            else refact3_filtration_cards(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'owner-none':
            none_owner_pk = self.request.POST.getlist('owner_id')
            cards = FuelCard.objects.filter(pk__in=none_owner_pk)
            for card in cards:
                card.owner = None
                card.save()
        else:
            return super(CardFilterAndCreateView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        messages.success(self.request, "Карта добавлена!")
        return super(CardFilterAndCreateView, self).form_valid(form)

class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """
        Выводит список активных заявок
        Фильтрует активные заявок
    """
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        context['all_apps'] = Application.objects.all() if not len(self.request.GET) \
            else refact3_filtration_apps(self.request.GET)
        return context

class AppView(LoginRequiredMixin,UpdateView, DeletionMixin):
    '''
    Просмотр выбраной заявки
    изменение выбраной заявки
    удаление выбраной заявки
    '''

    model = Application
    form_class = AppUpdateForm
    template_name = 'app.html'
    context_object_name = 'app'

    def get_success_url(self):
        if self.request.POST['action'] == 'delete-yes':
            return reverse('choose-car', args=[self.get_object().car.registration_number])
        else:
            return ""

    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        context['manager_commit_form'] = ManagerCommitAppForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST['action']
        if action == 'delete-yes':
            return self.delete(request, *args, **kwargs)
        if action == 'refuse-yes':
            object = self.get_object()
            object.status = 'T'
            object.save()
        if action == 'app_confirm':
            form = ManagerCommitAppForm(self.request.POST, instance=Application.objects.get(pk=self.kwargs['pk']))
            if form.is_valid():
                form.save()
        return super(AppView, self).post(request, *args, **kwargs)

class AccountView(LoginRequiredMixin, UpdateView):
    '''Обработка страницы ЛК'''

    template_name = 'account.html'

    form_class = UserUpdateForm
    form_change_balance = FuelCardChangeBalance
    form_add_doc = DriverDocForm

    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doc_create_form'] = DriverDocForm
        action_type = self.request.POST.get('action')

        context['form_add_doc'] = self.form_add_doc(self.request.POST) \
            if action_type == 'doc_create' else self.form_add_doc()
        context['form_change_balance'] = self.form_change_balance(self.request.POST) \
            if action_type == 'change_balance' else self.form_change_balance()
        context['form'] = self.form_class(self.request.POST) \
            if action_type == 'user_update' else self.form_class(instance=self.get_object())

        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action_type = self.request.POST.get('action')

        if action_type == 'user_update':
            form = self.form_class(self.request.POST, request.FILES, instance=self.get_object(), user=self.get_object())
        elif action_type == 'change_balance':
            form = self.form_change_balance(request.POST, instance=self.object.my_card)
        elif action_type == 'doc_create':
            form = self.form_add_doc(self.request.POST, self.request.FILES, user=request.user)
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ успешно удален!")
            return HttpResponseRedirect("")

        if form.is_valid():
            if action_type == 'change_balance':
                messages.success(self.request, "Баланс изменен!")
            elif action_type == 'doc_create':
                messages.success(self.request, "Документ добавлен!")
            elif action_type == 'user_update':
                messages.success(self.request, "Данные изменены!")

            return self.form_valid(form)
        else:
            return self.form_invalid(**{action_type: form})


class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

