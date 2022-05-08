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

# 1. рендерядтся form_class,


class PerfectCarView(LoginRequiredMixin, UpdateView):

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
        if action_type == 'car_update':
            context['form'] = self.form_class(self.request.POST)
        else:
            context['form'] = self.form_class(instance=self.get_object())
        if action_type == 'app_create':
            context['app_create_form'] = self.app_form_class(self.request.POST)
        else:
            context['app_create_form'] = self.app_form_class()
        if action_type == 'doc_create':
            context['doc_create_form'] = self.doc_form_class(self.request.POST)
        else:
            context['doc_create_form'] = self.doc_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action_type = self.request.POST.get('action')
        if action_type == 'car_update':
            form = self.get_form()
            form_name = 'car_update'
        elif action_type == 'app_create':
            print(self.request.POST)
            form = AppCreateForm(self.request.POST, user=self.request.user)
            form_name = 'app_create'
            form.instance.car = Car.objects.get(registration_number=self.kwargs['slug'])
            # form.instance.owner = self.request.user
            if self.request.user.role == 'm':
                form.instance.status = 'R'
        elif action_type == 'doc_create':
            form = AutoDocForm(self.request.POST, self.request.FILES)
            form_name = 'doc_create'
            form.instance.owner = Car.objects.get(registration_number=self.kwargs['slug'])
        elif "doc-" in action_type:
            doc_pk_to_delete = "".join([i for i in action_type if i.isdigit()])
            doc_to_delete = AutoDoc.objects.get(pk=doc_pk_to_delete)
            doc_to_delete.delete()
            messages.success(self.request, "Документ удален!")
            return HttpResponseRedirect("")
        if form.is_valid():
            if form_name == 'car_update':
                list_of_fields = ['registration_number', 'brand', 'region_code',
                                  'last_inspection']
                self.get_object()
                for field in list_of_fields:
                    if form.cleaned_data[field] is None:
                        setattr(form.instance, field, getattr(self.get_object(), field))
                messages.success(self.request, "Данные машины изменены!")
            elif form_name == 'app_create':
                messages.success(self.request, "Заявка добавлена!")
            elif form_name == 'doc_create':
                messages.success(self.request, "Документ добавлен!")

            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

