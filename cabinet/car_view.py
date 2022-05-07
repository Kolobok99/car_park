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

    def get_success_url(self):
        return self.request.path_info

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
            form_class = self.form_class
            form_name = 'car_update'

        elif action_type == 'app_create':
            form_class = self.app_form_class
            form_name = 'app_create'

        elif action_type == 'doc_create':
            form_class = self.doc_form_class
            form_name = 'doc_create'


        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})