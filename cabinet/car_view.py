from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin, DeletionMixin, UpdateView, FormView

from car_bot.models import Notifications
from . import form
from .form import *
from .models import *

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
    form_class = CarAddForm

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст:
                все авто
                или
                отфильтрованные авто
        """
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all() if not len(self.request.GET) \
            else refact3_filtration_car(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'owner-none':
            # Изъятие автомобилей
            none_owner_pk = self.request.POST.getlist('owner_refuse_id')
            cars_none = Car.objects.filter(pk__in=none_owner_pk)
            for car in cars_none:
                car.owner = None
                car.save()
            # Удаление автомобилей
            delete_owner_pk = self.request.POST.getlist('owner_delete_id')
            cars_delete = Car.objects.filter(pk__in=delete_owner_pk)
            for car in cars_delete:
                car.delete()

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
    form_class = CarUpdateForm

    app_form_class = AppCreateForm
    doc_form_class = AutoDocForm

    def get_success_url(self, **kwargs):
        return self.get_object().get_absolute_url()

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

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
            if action_type == 'car_update' else self.form_class(instance=self.get_object())
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
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ удален!")
            return HttpResponseRedirect("")
        if form.is_valid():
            if action_type == 'car_update':
                messages.success(self.request, "Данные машины изменены!")
            elif action_type == 'app_create':
                form.save(commit=False)
                print(f"{form.instance.pk}")
                new_note = Notifications()
                new_note.creator = self.request.user
                new_note.recipient = MyUser.objects.get(role='m')
                new_note.content = f'Уведомление о заявки № {form.instance.pk}'
                new_note.content_object = form.instance

                new_note.save()

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
        context['drivers'] = MyUser.objects.filter(role='d') if not len(self.request.GET) \
            else refact3_filtration_driver(self.request.GET)
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
    model = MyUser

    def get_context_data(self, **kwargs):
        """
        Возвраащает контекст:
            карты без владельца
        """
        context = super(DriverView, self).get_context_data(**kwargs)
        context['free_cards'] = FuelCard.objects.filter(owner__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        """добавляет карту водителю"""
        self.object = self.get_object()
        action_type = self.request.POST.get('action')
        if action_type == 'add-card':
            card = FuelCard.objects.get(pk=request.POST.get('card'))
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
    form_class = FuelCardAddForm

    def get_context_data(self, **kwargs):
        """
       Возвраащает контекст:
           все карты
           отфильтрованные карты
       """
        context = super().get_context_data(**kwargs)
        context['all_cards'] = FuelCard.objects.all() if not len(self.request.GET) \
            else refact3_filtration_cards(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):

        action = self.request.POST.get('action')
        if action == 'owner-none':
            # Изымает карты
            owner_id_to_none = self.request.POST.getlist('owner_id_to_none')
            cards_to_none = FuelCard.objects.filter(pk__in=owner_id_to_none)
            for card in cards_to_none:
                card.owner = None
                card.save()
            # Удаляет карты
            owner_id_to_delete = self.request.POST.getlist('owner_id_to_delete')
            cards_to_delete = FuelCard.objects.filter(pk__in=owner_id_to_delete)
            for card in cards_to_delete:
                card.delete()
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
        context['all_apps'] = Application.objects.filter(is_active=True) if not len(self.request.GET) \
            else refact3_filtration_apps(self.request.GET)
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
        """Возвращает контекст:
                            форму комментирования заявки
        """
        context = super(AppView, self).get_context_data(**kwargs)
        context['manager_commit_form'] = ManagerCommitAppForm(instance=self.get_object())
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
            object.save()
        if action == 'app_confirm':
            form = ManagerCommitAppForm(self.request.POST, instance=Application.objects.get(pk=self.kwargs['pk']))
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

    form_class = UserUpdateForm
    form_change_balance = FuelCardChangeBalance
    form_add_doc = DriverDocForm

    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.request.user.pk)

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
        context['form'] = self.form_class(self.request.POST) \
            if action_type == 'user_update' else self.form_class(instance=self.get_object())
        print(f"{context=}")
        return context

    def form_invalid(self, **kwargs):
        """Формирует ответ с невалидной формой"""
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
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ успешно удален!")
            return HttpResponseRedirect("")

        if form.is_valid():
            """Формирует контекст сообщений"""
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
    """
        Контроллер: Регистрация пользователя
    """

    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('driver-activation')

    def form_valid(self, form):

        activation_code = generator_activation_code()
        form.activation_code = activation_code
        send_activation_code.delay(driver_email=form.instance.email, activation_code=activation_code)
        # send_mail(
        #     'Подтверждение регистрации',
        #     f'ВАШ КОД: {activation_code}',
        #     'izolotavin99@gmail.com',
        #     [form.instance.email],
        #     fail_silently=False
        # )

        return super(RegistrationView, self).form_valid(form)

class EmailConfirmView(FormView):

    template_name = 'user_activation.html'
    form_class = DriverActivationForm

    def form_valid(self, form):
        print(f"form.activation_code = {form.cleaned_data['activation_code']}")
        try:
            new_driver = MyUser.objects.get(is_active=False, activation_code=form.cleaned_data['activation_code'])
            new_driver.is_active = True
            new_driver.activation_code = ''
            new_driver.save()
            return HttpResponseRedirect('')
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
            context['history'] = filtration_logs(self.get_all_history(), self.request.GET)
        else:
            context['history'] = self.get_all_history()
        return context
