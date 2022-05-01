from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
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
        reguest_GET = self.request.GET
        if len(reguest_GET) == 0:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = refact3_filtration_car(reguest_GET)
        return context

class DriversFilterView(Context, LoginRequiredMixin, TemplateView):
    """
    Выводит список водителей
    Фильтрует список водителей
    """
    template_name = 'drivers.html'

    def get_context_data(self, **kwargs):
        context = super(DriversFilterView, self).get_context_data(**kwargs)
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['drivers'] = MyUser.objects.filter(role='d')
        else:
            context['drivers'] = refact3_filtration_driver(request_GET)
        return context

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
                context['all_docs'] = chain(
                    refact3_filtration_documents(model=AutoDoc, get_params=request_GET),
                    refact3_filtration_documents(model=UserDoc, get_params=request_GET)
                )
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
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['all_cards'] = FuelCard.objects.all()
        else:
            context['all_cards'] = refact3_filtration_cards(request_GET)
        return context


class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """
        Выводит список активных заявок
        Фильтрует активные заявок
    """
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['all_apps'] = Application.objects.all()
        else:
            context['all_apps'] = refact3_filtration_apps(request_GET)

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

    def get_success_url(self):
        if self.request.POST['action'] == 'delete-yes':
            return "/applications"
        elif self.request.POST['action'] == 'app_update':
            return ""
    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        context['app'] = Application.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST['action'] == 'delete-yes':
            return self.delete(request, *args, **kwargs)
        else:
            return super(AppView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.POST['action'] == 'app_update':
            if form.is_valid():
                return super(AppView, self).form_valid(form)


class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')


class AccountView(LoginRequiredMixin, UpdateView):
    '''Обработка страницы ЛК'''

    template_name = 'account.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doc_create_form'] = DriverDocForm
        return context

    def post(self, request, *args, **kwargs):
        action_type = self.request.POST['action']
        print("IS_POST_USER!!!")
        if 'change_balance' in action_type:
            card_id = "".join([i for i in action_type if i.isdigit()])
            card = FuelCard.objects.get(pk=card_id)
            card.balance = self.request.POST['balance']
            card.save()
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
        else:
            return super(AccountView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        print(form.fields)
        print("YES_VALID!!!")
        action_type = self.request.POST['action']
        print(action_type)
        if action_type == 'user_update':
            form.instance.password = self.request.user.password
            list_of_fields = ['first_name', 'last_name', 'patronymic',
                              'phone', 'email']
            for field in list_of_fields:
                if form.cleaned_data[field] is None:
                    setattr(form.instance, field, getattr(self.request.user, field))
        elif action_type == 'doc_create':
            form = DriverDocForm(self.request.POST, self.request.FILES)
            form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
        if form.is_valid():
            return super().form_valid(form)
        return HttpResponseRedirect("")

class CarView(LoginRequiredMixin, UpdateView):
    """Обработка страницы Машины"""

    template_name = 'car.html'
    form_class = CarUpdateForm
    success_url = ''

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_create_form'] = AppCreateForm()
        context['doc_create_form'] = AutoDocForm()

        return context

    def post(self, request, *args, **kwargs):
        print("YES_IS_POST")
        action_type = self.request.POST.get('action')
        print(action_type)
        if "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
        else:
            return super().post(request, *args, **kwargs)

        return HttpResponseRedirect("")

    def form_valid(self, form):
        action_type = self.request.POST['action']
        print("YES_IS_VALID")
        if action_type == 'car_update':
            list_of_fields = ['registration_number', 'brand', 'region_code',
                              'last_inspection', 'owner']
            self.get_object()
            for field in list_of_fields:
                if form.cleaned_data[field] is None:
                    setattr(form.instance, field, getattr(self.get_object(), field))
        elif action_type == 'doc_create':
            form = DriverDocForm(self.request.POST)
            form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
        if action_type == 'app_create':
            form = AppCreateForm(self.request.POST)
            form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
            form.instance.owner = self.request.user
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST)
            form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
        if form.is_valid():
            return super().form_valid(form)
        return HttpResponseRedirect("")


class DriverView(LoginRequiredMixin, UpdateView):
    """Страница выбранного водителя"""

    template_name = 'driver.html'
    slug_field = 'pk'
    form_class = UserUpdateForm
    success_url = reverse_lazy('choose-driver', slug_field)
    context_object_name = 'driver'

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.kwargs['pk'])

class NewCarView(UpdateView):
    template_name = "car.html"
    success_url = '/'
    model = Car
    slug_field = 'registration_number'
    # fields = "__all__"
    # form_class = NewCarUpdateForm

    def form_valid(self, form):
        print("valit!")
        return super(NewCarView, self).form_valid(form)


from django.http import FileResponse
import os

def show_pdf(request):
    filepath = os.path.join('static', 'sample.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')