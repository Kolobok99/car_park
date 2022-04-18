from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin, DeletionMixin, UpdateView

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


class CarCreateView(Context, LoginRequiredMixin, CreateView):
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


class AplicationsView(Context, LoginRequiredMixin, TemplateView):
    """Вывод заявок"""
    template_name = 'applications.html'

    def get_context_data(self, **kwargs):
        context = super(AplicationsView, self).get_context_data(**kwargs)
        if len(self.request.GET) == 0:
            context['all_apps'] = Application.objects.all()
        else:
            context['all_apps'] = filtration_apps(self.request.GET)

        return context

class AppView(LoginRequiredMixin,UpdateView, DeletionMixin):
    '''Просмотр, изменение и удаление заявки'''

    model = Application
    form_class = AppCreateForm
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
        #     form = AppCreateForm(self.request.POST, instance=self.kwargs['pk'])
        #     return super(AppView, self).form_valid(form)



        # if self.request.POST['action'] == 'delete-yes':
        #     print("del-yes!")
        #     app_to_delete = Application.objects.get(pk=self.kwargs['slug'])
        #     app_to_delete.delete()
        #     return super(AppView, self).form_valid(form)


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

class AccountView(LoginRequiredMixin, TemplateView):
    '''Обработка страницы ЛК'''

    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['user'] = MyUser.objects.get(pk=self.request.user.pk)

        return context


class CarView(LoginRequiredMixin, TemplateView):
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
        form = None
        if action_type == 'app_create':
            form = AppCreateForm(self.request.POST)
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
