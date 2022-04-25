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


class CarsView(Context, ListView):
    """Вывод всех автомобилей"""

    template_name = "cars.html"
    context_object_name = "cars"
    success_url = '/cars'


class CarCreateView(Context, LoginRequiredMixin, CreateView):
    '''добавление нового автомобиля'''
    template_name = "cars.html"
    # context_object_name = "cars"
    success_url = '/cars'
    form_class = CarAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['cars'] = CarFilter(self.request.GET, query_set=Car.objects.all())
        if len(self.request.GET) == 0:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = refact3_filtration_car(self.request.GET)
        return context


class DriversView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'drivers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['drivers'] = MyUser.objects.filter(role='d')
        else:
            context['drivers'] = refact3_filtration_driver(self.request.GET)
        return context


class DocumentsView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'documents.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_docs'] = super(DocumentsView, self).get_all_docs()
        else:
            if len(self.request.GET.getlist('aorm')) == 2:
                context['all_docs'] = chain(
                    refact3_filtration_documents(model=AutoDoc, get_params=self.request.GET),
                    refact3_filtration_documents(model=UserDoc, get_params=self.request.GET)
                )
            elif self.request.GET.get('aorm') == 'car':
                context['all_docs'] = refact3_filtration_documents(model=AutoDoc, get_params=self.request.GET)
            elif self.request.GET.get('aorm') == 'man':
                context['all_docs'] = refact3_filtration_documents(model=UserDoc, get_params=self.request.GET)

            context['get_parametrs'] = self.request.GET.items()
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
            context['all_cards'] = refact3_filtration_cards(self.request.GET)
        return context


class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """Вывод заявок"""
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_apps'] = Application.objects.all()
        else:
            context['all_apps'] = refact3_filtration_apps(self.request.GET)

        return context

class AppView(LoginRequiredMixin,UpdateView, DeletionMixin):
    '''Просмотр, изменение и удаление заявки'''

    model = Application
    form_class = AppForm
    template_name = 'app.html'
    # success_url = "/applications"

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
        print("form_valid")
        print(self.request.POST['action'])
        if self.request.POST['action'] == 'app_update':
            if form.is_valid():
                return super(AppView, self).form_valid(form)
        # if self.request.POST['action'] == 'delete-yes':
        #     app_to_delete
        # print(self.request.POST['action'])
        # print(self.kwargs)
        # if self.request.POST['action'] == 'app_update':
        #     form = AppForm(self.request.POST, instance=self.kwargs['pk'])
        #     return super(AppView, self).form_valid(form)



        # if self.request.POST['action'] == 'delete-yes':
        #     print("del-yes!")
        #     app_to_delete = Application.objects.get(pk=self.kwargs['slug'])
        #     app_to_delete.delete()
        #     return super(AppView, self).form_valid(form)


class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     super(RegistrationView, self).form_valid(form)
    #     email = form.cleaned_data['email']
    #     password = form.cleaned_data['password']
    #     user = authenticate(email, password)
    #     return login(self.request, user)


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
#         'app_create': AppForm,
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

# form_class = AppForm
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
        if 'change_balance' in action_type:
            card_id = "".join([i for i in action_type if i.isdigit()])
            print(card_id)
            card = FuelCard.objects.get(pk=card_id)
            card.balance = self.request.POST['balance']
            card.save()
            return HttpResponseRedirect("")
        elif action_type == 'doc_create':
            form = DriverDocForm(self.request.POST)
            form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("")
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            return HttpResponseRedirect("")
        else:
            return super(AccountView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.fields)
        action_type = self.request.POST['action']
        if action_type == 'user_update':
            form.instance.pk = self.request.user.pk
            form.instance.password = self.request.user.password
            list_of_fields = ['first_name', 'last_name', 'patronymic',
                              'phone', 'email']
            for field in list_of_fields:
                if form.cleaned_data[field] is None:
                    setattr(form.instance, field, getattr(self.request.user, field))
            if form.is_valid():
                return super().form_valid(form)


class CarView(LoginRequiredMixin, UpdateView):
    template_name = 'car.html'
    form_class = CarAddForm
    success_url = reverse_lazy('cars')

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        # car = Car.objects.get(registration_number=self.kwargs['slug'])
        app_create_form = AppForm()
        doc_create_form = AutoDocForm()
        context = super().get_context_data(**kwargs)
        # context['car'] = car
        context['app_create_form'] = app_create_form
        context['doc_create_form'] = doc_create_form

        return context

    def post(self, request, *args, **kwargs):
        action_type = self.request.POST.get('action')
        form = None
        if action_type == 'app_create':
            form = AppForm(self.request.POST)
            form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
            form.instance.status = 'O'
            form.instance.owner = self.request.user
            # print(form.instance.owner)
            print(form.errors)
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST)
            form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
        if form != None and form.is_valid():
            form.save()
        return HttpResponseRedirect("")
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


class CarsView(Context, ListView):
    """Вывод всех автомобилей"""

    template_name = "cars.html"
    context_object_name = "cars"
    success_url = '/cars'


class CarCreateView(Context, LoginRequiredMixin, CreateView):
    '''добавление нового автомобиля'''
    template_name = "cars.html"
    # context_object_name = "cars"
    success_url = '/cars'
    form_class = CarAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['cars'] = CarFilter(self.request.GET, query_set=Car.objects.all())
        if len(self.request.GET) == 0:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = refact3_filtration_car(self.request.GET)
        return context


class DriversView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'drivers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['drivers'] = MyUser.objects.filter(role='d')
        else:
            context['drivers'] = refact3_filtration_driver(self.request.GET)
        return context


class DocumentsView(Context, LoginRequiredMixin, TemplateView):
    template_name = 'documents.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_docs'] = super(DocumentsView, self).get_all_docs()
        else:
            if len(self.request.GET.getlist('aorm')) == 2:
                context['all_docs'] = chain(
                    refact3_filtration_documents(model=AutoDoc, get_params=self.request.GET),
                    refact3_filtration_documents(model=UserDoc, get_params=self.request.GET)
                )
            elif self.request.GET.get('aorm') == 'car':
                context['all_docs'] = refact3_filtration_documents(model=AutoDoc, get_params=self.request.GET)
            elif self.request.GET.get('aorm') == 'man':
                context['all_docs'] = refact3_filtration_documents(model=UserDoc, get_params=self.request.GET)

            context['get_parametrs'] = self.request.GET.items()
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
            context['all_cards'] = refact3_filtration_cards(self.request.GET)
        return context


class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """Вывод заявок"""
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_apps'] = Application.objects.all()
        else:
            context['all_apps'] = refact3_filtration_apps(self.request.GET)

        return context

class AppView(LoginRequiredMixin,UpdateView, DeletionMixin):
    '''Просмотр, изменение и удаление заявки'''

    model = Application
    form_class = AppForm
    template_name = 'app.html'
    # success_url = "/applications"

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
        print("form_valid")
        print(self.request.POST['action'])
        if self.request.POST['action'] == 'app_update':
            if form.is_valid():
                return super(AppView, self).form_valid(form)
        # if self.request.POST['action'] == 'delete-yes':
        #     app_to_delete
        # print(self.request.POST['action'])
        # print(self.kwargs)
        # if self.request.POST['action'] == 'app_update':
        #     form = AppForm(self.request.POST, instance=self.kwargs['pk'])
        #     return super(AppView, self).form_valid(form)



        # if self.request.POST['action'] == 'delete-yes':
        #     print("del-yes!")
        #     app_to_delete = Application.objects.get(pk=self.kwargs['slug'])
        #     app_to_delete.delete()
        #     return super(AppView, self).form_valid(form)


class RegistrationView(CreateView):
    '''Регистрация пользователя'''

    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     super(RegistrationView, self).form_valid(form)
    #     email = form.cleaned_data['email']
    #     password = form.cleaned_data['password']
    #     user = authenticate(email, password)
    #     return login(self.request, user)


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
#         'app_create': AppForm,
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

# form_class = AppForm
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
        if 'change_balance' in action_type:
            card_id = "".join([i for i in action_type if i.isdigit()])
            print(card_id)
            card = FuelCard.objects.get(pk=card_id)
            card.balance = self.request.POST['balance']
            card.save()
            return HttpResponseRedirect("")
        elif action_type == 'doc_create':
            form = DriverDocForm(self.request.POST)
            form.instance.owner = MyUser.objects.get(pk=self.request.user.pk)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("")
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = UserDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            return HttpResponseRedirect("")
        else:
            return super(AccountView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.fields)
        action_type = self.request.POST['action']
        if action_type == 'user_update':
            form.instance.pk = self.request.user.pk
            form.instance.password = self.request.user.password
            list_of_fields = ['first_name', 'last_name', 'patronymic',
                              'phone', 'email']
            for field in list_of_fields:
                if form.cleaned_data[field] is None:
                    setattr(form.instance, field, getattr(self.request.user, field))
            if form.is_valid():
                return super().form_valid(form)


class CarView(LoginRequiredMixin, UpdateView):
    template_name = 'car.html'
    form_class = CarAddForm
    success_url = reverse_lazy('cars')

    def get_object(self, queryset=None):
        return Car.objects.get(registration_number=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        # car = Car.objects.get(registration_number=self.kwargs['slug'])
        app_create_form = AppForm()
        doc_create_form = AutoDocForm()
        context = super().get_context_data(**kwargs)
        # context['car'] = car
        context['app_create_form'] = app_create_form
        context['doc_create_form'] = doc_create_form

        return context

    def post(self, request, *args, **kwargs):
        action_type = self.request.POST.get('action')
        form = None
        if action_type == 'app_create':
            form = AppForm(self.request.POST)
            form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
            form.instance.status = 'O'
            form.instance.owner = self.request.user
            # print(form.instance.owner)
            print(form.errors)
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST)
            form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
        if form != None and form.is_valid():
            form.save()
        return HttpResponseRedirect("")
