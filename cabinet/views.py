from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin, DeletionMixin, UpdateView, FormView

from cabinet import forms

from django.views.generic import ListView, TemplateView, CreateView, DetailView

from cabinet.services.filtration import *

from cabinet.services.services import Context, generator_activation_code
from .tasks import send_activation_code


class CarsCreateAndFilterView(Context, LoginRequiredMixin, CreateView):
    """
    Контроллер: Автомобили (только менеджер)
    Функционал:
                Выводит:
                        список автомобилей
                        список отфильтрованных автомобилей
                Добавляет:
                        новый автомобиль
                Удаляет и Изымает:
                        выбранные автомобили
    """
    template_name = "cars.html"
    success_url = '/cars'
    form_class = forms.CarAddForm

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
                все авто
                или
                отфильтрованные авто
        """
        context = super().get_context_data(**kwargs)
        context['cars'] = models.Car.objects.all() if not len(self.request.GET) \
            else filtration_car(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'owner-none':
            # Изъятие автомобилей
            none_owner_pk = self.request.POST.getlist('owner_refuse_id')
            models.Car.objects.filter(pk__in=none_owner_pk).update(owner=None)
            # Удаление автомобилей
            delete_owner_pk = self.request.POST.getlist('owner_delete_id')
            models.Car.objects.filter(pk__in=delete_owner_pk).delete()
        else:
            return super().post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        messages.success(self.request, "Машина добавлена")
        return super().form_valid(form)

class CarView(LoginRequiredMixin, UpdateView):
    """
        Контроллер: выбранное авто
        Менеджер + владелец авто:
                                Выводит информацию о конкретном авто
                                Добавление:
                                            заявки
                                            документа
                                Удаление:
                                        документа
        Менеджер:
                Изменение данных авто
    """

    template_name = 'car.html'
    form_class = forms.CarUpdateForm

    app_form_class = forms.AppCreateForm
    doc_form_class = forms.AutoDocForm

    def get_success_url(self, **kwargs):
        return self.get_object().get_absolute_url()

    def get_object(self, queryset=None):
        return models.Car.objects.get(registration_number=self.kwargs['slug'])

    def form_invalid(self, **kwargs):
        """Формирует ответ с невыалидной формой"""
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
            формы:
                Добавления документа:
                Добавления заявки:
                Изменения данных машины:
        """
        context = super().get_context_data(**kwargs)
        action_type = self.request.POST.get('action')

        context['doc_create_form'] = self.doc_form_class(self.request.POST) \
            if action_type == 'doc_create' else self.doc_form_class()
        context['app_create_form'] = self.app_form_class(self.request.POST)\
            if action_type == 'app_create' else self.app_form_class()
        context['form'] = self.form_class(self.request.POST) \
            if action_type == 'car_update' else self.form_class(instance=self.get_object(), car=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        """
        Обновление данных машины
        Создание заявки
        Добавление документа
        Удаление документа
        """
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
            doc_to_delete = models.AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ удален!")
            return HttpResponseRedirect("")
        if form.is_valid():
            #  Формирует сообщение
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
        Контроллер: Водители (только менеджер)
        Функционал:
                    Выводит список водителей
                    Выводит список отфильтрованных водителей
    """
    template_name = 'drivers.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
            все водители
            отфильтрованные водители
        """
        context = super(DriversFilterView, self).get_context_data(**kwargs)
        context['drivers'] = models.MyUser.objects.filter(role='d') if not len(self.request.GET) \
            else filtration_driver(self.request.GET)
        return context

class DriverView(LoginRequiredMixin, DetailView):
    """
        Контроллер: выбранный водитель (только менеджер)
        Функционал:
                    Выводит:
                            Информацию о водители
                            Записанные автомобили
                            Заявки
                            Документы
                    Добавляет:
                            топливную карту водителю

    """

    template_name = 'driver.html'
    context_object_name = 'driver'
    model = models.MyUser

    def get_context_data(self, **kwargs):
        """
        Возвраащает контекст:
            карты без владельца
        """
        context = super(DriverView, self).get_context_data(**kwargs)
        context['free_cards'] = models.FuelCard.objects.filter(owner__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        """добавляет карту водителю"""
        self.object = self.get_object()
        action_type = self.request.POST.get('action')
        if action_type == 'add-card':
            card = models.FuelCard.objects.get(pk=request.POST.get('card'))
            card.owner = self.get_object()
            card.save()
        return HttpResponseRedirect("")

class DocumentsView(Context, LoginRequiredMixin, TemplateView):
    """
        Контроллер: Документы (только менеджер)
        Функционал:
                    Выводит список документов
                    Выводит список отфильтрованных документов
    """
    template_name = 'documents.html'

    def get_context_data(self, **kwargs):
        """
        Возвраащает контекст документов:
           все авто + водители
           отфильтрованные:
                            авто + водители
                            авто
                            водители
        """
        context = super().get_context_data(**kwargs)
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['all_docs'] = super().get_all_docs()
        else:
            if len(request_GET.getlist('aorm')) == 2:
                context['all_docs'] = list(chain(
                    filtration_documents(model=models.AutoDoc, get_params=request_GET),
                    filtration_documents(model=models.UserDoc, get_params=request_GET)
                ))
            elif request_GET.get('aorm') == 'car':
                context['all_docs'] = filtration_documents(model=models.AutoDoc, get_params=request_GET)
            elif request_GET.get('aorm') == 'man':
                context['all_docs'] = filtration_documents(model=models.UserDoc, get_params=request_GET)

            context['get_parametrs'] = request_GET.items()
        return context

class CardFilterAndCreateView(Context, LoginRequiredMixin, CreateView):
    """
        Контроллер: Топливные карты (только менеджер)
        Функционал:
                    Выводит:
                            список топливных карт
                            список отфильтрованных топливных карт
                    Добавляет:
                            новую карту
                    Удаляет и Изымает:
                            выбранные карты
    """
    template_name = 'cards.html'
    success_url = '/cards'
    form_class = forms.FuelCardAddForm

    def get_context_data(self, **kwargs):
        """
       Возвраащает контекст:
           все карты
           отфильтрованные карты
       """
        context = super().get_context_data(**kwargs)
        context['all_cards'] = models.FuelCard.objects.all() if not len(self.request.GET) \
            else filtration_cards(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):

        action = self.request.POST.get('action')
        if action == 'owner-none':
            # Изымает карты
            owner_id_to_none = self.request.POST.getlist('owner_id_to_none')
            models.FuelCard.objects.filter(pk__in=owner_id_to_none).update(owner=None)

            # Удаляет карты
            owner_id_to_delete = self.request.POST.getlist('owner_id_to_delete')
            models.FuelCard.objects.filter(pk__in=owner_id_to_delete).delete()
        else:
            return super(CardFilterAndCreateView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        messages.success(self.request, "Карта добавлена!")
        return super(CardFilterAndCreateView, self).form_valid(form)

class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """
        Контроллер: Заявки (только менеджер)
        Функционал:
                    Выводит:
                            список активных заявок
                            список отфильтрованных активных заявок
    """
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
             все активные заявки
             отфильтрованные активные заявки
        """
        context = super(AplicationsView, self).get_context_data(**kwargs)
        context['all_apps'] = models.Application.objects.filter(is_active=True) if not len(self.request.GET) \
            else filtration_apps(self.request.GET)
        return context

class AppView(LoginRequiredMixin,UpdateView, DeletionMixin):
    '''
        Контроллер: выбранная заявка
        Функционал:
            Менеджер + Владелец заявки:
                     просмотр заявки
            Менеджер:
                     одобрение заявки (отправка механикам)
                     возврат заявки на доработку
            Владелец заявки:
                     удаление заявки
                     изменение заявки
    '''

    model = models.Application
    form_class = forms.AppUpdateForm
    template_name = 'app.html'
    context_object_name = 'app'

    def get_success_url(self):
        if self.request.POST['action'] == 'delete-yes':
            return reverse('choose-car', args=[self.get_object().car.registration_number])
        else:
            return ""

    def get_context_data(self, **kwargs):
        """Возвращает контекст:
                            форму комментирования заявки
        """
        context = super(AppView, self).get_context_data(**kwargs)
        context['manager_commit_form'] = forms.ManagerCommitAppForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        """
            Удаляет заявку
            Возвращает заявку на доработку
            Подтверждает заявку
        """
        action = self.request.POST['action']
        if action == 'delete-yes':
            return self.delete(request, *args, **kwargs)
        if action == 'refuse-yes':
            object = self.get_object()
            object.status = 'T'
            object.manager_descr = None
            object.engineer = None
            object.save()
        if action == 'app_confirm':
            form = forms.ManagerCommitAppForm(self.request.POST, instance=models.Application.objects.get(pk=self.kwargs['pk']))
            if form.is_valid():
                form.save()
        return super(AppView, self).post(request, *args, **kwargs)

class AccountView(LoginRequiredMixin, UpdateView):
    """
        Контроллер: личная страница пользователя
        Функционал:
                    Вывод:
                          автомобилей
                          заявок
                          документов
                    Изменение:
                          личный данных
                          баланса карты
                    Добавление:
                          документов
    """

    template_name = 'account.html'

    form_class = forms.UserUpdateForm
    form_change_balance =forms.FuelCardChangeBalance
    form_add_doc = forms.DriverDocForm

    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return models.MyUser.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
            формы:
                добавления документа:
                изменение баланса:
                изменение данных пользователя:
        """
        context = super().get_context_data(**kwargs)
        action_type = self.request.POST.get('action')

        context['doc_create_form'] = self.form_add_doc(self.request.POST) \
            if action_type == 'doc_create' else self.form_add_doc()
        context['form_change_balance'] = self.form_change_balance(self.request.POST) \
            if action_type == 'change_balance' else self.form_change_balance()
        context['form'] = self.form_class(self.request.POST, instance=self.get_object(), user=self.get_object()) \
            if action_type == 'user_update' else self.form_class(instance=self.get_object(), user=self.get_object())
        return context

    def form_invalid(self, **kwargs):
        """Формирует ответ с невалидной формой"""
        print("Перед render_to_response")
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        """
        Изменение личных данных
        Изменение баланса карты
        Добавление документа
        Удаление документа
        """
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
            doc_to_delete = models.UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ успешно удален!")
            return HttpResponseRedirect("/account/")

        if form.is_valid():
            """Формирует контекст сообщений"""
            if action_type == 'change_balance':
                messages.success(self.request, "<span>Баланс изменен!</span>")
            elif action_type == 'doc_create':
                messages.success(self.request, "<span>Документ добавлен!</span>")
            elif action_type == 'user_update':
                messages.success(self.request, "<span>Данные изменены!</span>")

            return self.form_valid(form)
        else:
            print('Перед вызовом form_invalid')
            return self.form_invalid(**{action_type: form})

class RegistrationView(CreateView):
    """
        Контроллер: Регистрация пользователя
    """

    template_name = 'registration.html'
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('driver-activation')

    def form_valid(self, form):
        # User'у присвается код активации аккаунта
        activation_code = generator_activation_code()
        form.activation_code = activation_code
        # Код активации отправляется user'у
        send_activation_code.delay(driver_email=form.instance.email, activation_code=activation_code)

        return super(RegistrationView, self).form_valid(form)

class EmailConfirmView(FormView):

    template_name = 'user_activation.html'
    form_class = forms.DriverActivationForm

    def form_valid(self, form):
        # При вводе кода активации, код сбрасывается,
        # а аккаунт становится активным
        try:
            new_driver = models.MyUser.objects.get(is_active=False, activation_code=form.cleaned_data['activation_code'])
            new_driver.is_active = True
            new_driver.activation_code = ''
            new_driver.save()
            return HttpResponseRedirect('/')
        except:
            return HttpResponseRedirect('/registration')

class HistoryView(Context, TemplateView):
    """
        Контроллер: выводит историю действия user'ов
    """

    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        if len(self.request.GET):
            context['history'] = filtration_history(self.get_all_history(), self.request.GET)
        else:
            context['history'] = self.get_all_history()
        return context
