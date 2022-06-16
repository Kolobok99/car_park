from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeletionMixin, UpdateView

from to_delete.early_forms import *

from django.views.generic import TemplateView, CreateView

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
    # success_message = "Машина добавлена!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reguest_GET = self.request.GET
        if len(reguest_GET) == 0:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = refact3_filtration_car(reguest_GET)
        return context

    def post(self, request, *args, **kwargs):
        print('post!')
        action = self.request.POST.get('action')
        print(action)
        if action == 'owner-none':
            none_owner_pk = self.request.POST.getlist('owner_id')
            print(none_owner_pk)
            cars = Car.objects.filter(pk__in=none_owner_pk)
            print(cars)
            for car in cars:
                car.owner = None
                car.save()
        else:
            return super(CarsCreateAndFilterView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect("")
    
    def form_valid(self, form):
        messages.success(self.request, "Машина добавлена")
        return super(CarsCreateAndFilterView, self).form_valid(form)

    # def form_invalid(self, form):
    #     messages.error(self.request, "Ошибка добавления!")
    #     form = CarForm(self.request.POST)
    #     return super(CarsCreateAndFilterView, self).form_invalid(form)
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
        request_GET = self.request.GET
        if len(request_GET) == 0:
            context['all_cards'] = FuelCard.objects.all()
        else:
            context['all_cards'] = refact3_filtration_cards(request_GET)
        return context

    def post(self, request, *args, **kwargs):
        print('post!')
        action = self.request.POST.get('action')
        print(action)
        if action == 'owner-none':
            none_owner_pk = self.request.POST.getlist('owner_id')
            print(none_owner_pk)
            cards = FuelCard.objects.filter(pk__in=none_owner_pk)
            print(cards)
            for card in cards:
                card.owner = None
                card.save()
        else:
            print('111')
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
            app = Application.objects.get(pk=self.kwargs['pk'])
            return reverse('choose-car', args=[app.car.registration_number])
        elif self.request.POST['action'] == 'app_update': return ""

    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        context['app'] = Application.objects.get(pk=self.kwargs['pk'])
        context['manager_commit_form'] = ManagerCommitAppForm(instance=Application.objects.get(pk=self.kwargs['pk']))
        return context

    def post(self, request, *args, **kwargs):
        action = self.request.POST['action']
        if action == 'delete-yes':
            return self.delete(request, *args, **kwargs)
        if action == 'refuse-yes':
            instanse = Application.objects.get(pk=self.kwargs['pk'])
            instanse.status = 'T'
            instanse.save()
        if action == 'app_confirm':
                form = ManagerCommitAppForm(self.request.POST, instance=Application.objects.get(pk=self.kwargs['pk']))
                form.instance.status = 'R'
                if form.is_valid(): form.save()

        return super(AppView, self).post(request, *args, **kwargs)




class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = UserCreateForm
    # success_url = reverse_lazy('account')

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super(RegistrationView, self).form_valid(form)

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
            messages.success(self.request, "Баланс карты изменен!")
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.error(self.request, "Документ успешно удален!")
        elif action_type == 'doc_create':
            form = DriverDocForm(self.request.POST, self.request.FILES)
            form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
            if form.is_valid():
                messages.success(self.request, "Документ успешно добавлен")
                form.save()
        else:
            return super().post(request, *args, **kwargs)
        return HttpResponseRedirect("")

    def form_valid(self, form):
        # self.post()
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
        if form.is_valid():
            messages.success(self.request, "Данные аккаунта изменены!")
            return super().form_valid(form)
        else:
            print("error")
            messages.error(self.request, "Ошибка ввода!")
        return HttpResponseRedirect("")


class CarView(LoginRequiredMixin, UpdateView):
    """Обработка страницы Машины"""

    template_name = 'car.html'
    form_class = CarUpdateForm

    def get_success_url(self):
        return self.request.path_info

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form1' in context:
            if context['form1'] == 'app_form':
                context['app_create_form'] = AppCreateForm(self.request.POST)
                context['doc_create_form'] = AutoDocForm()
            elif context['form1'] == 'doc_form':
                context['app_create_form'] = AppCreateForm()
                context['doc_create_form'] = AutoDocForm(self.request.POST)
        else:
            context['app_create_form'] = AppCreateForm()
            context['doc_create_form'] = AutoDocForm()
        return context

    def post(self, request, *args, **kwargs):
        print("YES_IS_POST")
        action_type = self.request.POST.get('action')
        self.object = self.get_object()
        print(action_type)
        if "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
        if action_type == 'app_create':
            form = AppCreateForm(self.request.POST)
            form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
            form.instance.owner = self.request.user
            form1 = 'app_form'
            if self.request.user.role == 'm':
                form.instance.status = 'R'
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST, self.request.FILES)
            form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
            form1 = 'doc_form'
        else:
            return super().post(request, *args, **kwargs)
        return HttpResponseRedirect("")


    def form_valid(self, form):
        action_type = self.request.POST['action']
        print("YES_IS_VALID")
        if action_type == 'car_update':
            list_of_fields = ['registration_number', 'brand', 'region_code',
                              'last_inspection']
            self.get_object()
            for field in list_of_fields:
                if form.cleaned_data[field] is None:
                    setattr(form.instance, field, getattr(self.get_object(), field))
            return super(CarView, self).form_valid(form)
        # elif action_type == 'doc_create':
        #     form = DriverDocForm(self.request.POST)
        #     form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
        # if action_type == 'app_create':
        #     form = AppCreateForm(self.request.POST)
        #     form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
        #     form.instance.owner = self.request.user
        #     # if self.request.user.is_manager:
        #     #     form.instance.status = 'R'
        # elif action_type == 'doc_create':
        #     form = AutoDocForm(self.request.POST, self.request.FILES)
        #     form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
        # print(f"{form=}")
        if form.is_valid():
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
        # return HttpResponseRedirect("")

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

class GoodCar(LoginRequiredMixin, UpdateView):
    """Обработка страницы Машины"""

    template_name = 'car.html'
    form_class = CarUpdateForm
    app_form_class = AppCreateForm
    doc_form_class = AutoDocForm


    def get_success_url(self):
        return self.request.path_info

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form1' in context:
            if context['form1'] == 'app_form':
                context['app_create_form'] = AppCreateForm(self.request.POST)
                context['doc_create_form'] = AutoDocForm()
            elif context['form1'] == 'doc_form':
                context['app_create_form'] = AppCreateForm()
                context['doc_create_form'] = AutoDocForm(self.request.POST)
        else:
            context['app_create_form'] = AppCreateForm()
            context['doc_create_form'] = AutoDocForm()
        return context


class DriverView(LoginRequiredMixin, UpdateView):
    """Страница выбранного водителя"""

    template_name = 'driver.html'
    slug_field = 'pk'
    form_class = UserUpdateForm
    success_url = reverse_lazy('choose-driver', slug_field)
    context_object_name = 'driver'

    def get_object(self, queryset=None):
        return MyUser.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DriverView, self).get_context_data(**kwargs)
        context['free_cards'] = FuelCard.objects.filter(owner__isnull=True)

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
            # action = request.POST['action']
        if action == 'add-card':
            card = FuelCard.objects.get(pk=request.POST.get('card'))
            card.owner = self.get_object()
            card.save()
        return HttpResponseRedirect("")

# class NewCarView(UpdateView):
#     template_name = "car.html"
#     success_url = '/'
#     model = Car
#     slug_field = 'registration_number'
#     # fields = "__all__"
#     # form_class = NewCarUpdateForm
#
#     def form_valid(self, form):
#         print("valit!")
#         return super(NewCarView, self).form_valid(form)


from django.http import FileResponse
import os

def show_pdf(request):
    filepath = os.path.join('static', 'sample.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def example(request):
    messages.info(request, "Документ удален!")
    return render(request, 'example.html')