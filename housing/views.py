from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from .exceptions import HousingValidationError
from .forms import RegistrationForm
from .models import House, MaintenanceRequest, Resident
from . import services


# HOME
def home(request):
    context = {
        "summary": services.dashboard_summary(),
        "recent_requests": services.recent_requests(),
    }
    return render(request, 'home.html', context)


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully.')
        return redirect(self.get_success_url())


# ------------------ HOUSE VIEWS ------------------

class HouseListView(ListView):
    model = House
    template_name = 'houses/house_list.html'
    context_object_name = 'houses'

    def get_queryset(self):
        return services.list_houses()


class HouseCreateView(LoginRequiredMixin, CreateView):
    model = House
    fields = ['address', 'city', 'state', 'zip_code', 'rent']
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('house_list')

    def form_valid(self, form):
        try:
            self.object = services.create_house(form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'House saved successfully.')
        return HttpResponseRedirect(self.get_success_url())


class HouseUpdateView(LoginRequiredMixin, UpdateView):
    model = House
    fields = ['address', 'city', 'state', 'zip_code', 'rent']
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('house_list')

    def form_valid(self, form):
        try:
            self.object = services.update_house(self.get_object(), form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'House updated successfully.')
        return HttpResponseRedirect(self.get_success_url())


class HouseDeleteView(LoginRequiredMixin, DeleteView):
    model = House
    template_name = 'houses/house_confirm_delete.html'
    success_url = reverse_lazy('house_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            services.delete_house(self.object)
            messages.success(request, 'House deleted successfully.')
        except HousingValidationError as exc:
            messages.error(request, str(exc))
        return HttpResponseRedirect(self.get_success_url())


# ------------------ REQUEST VIEWS ------------------

class RequestListView(ListView):
    model = MaintenanceRequest
    template_name = 'requests/request_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return services.list_requests()


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRequest
    fields = ['house', 'resident', 'title', 'description', 'status', 'category']
    template_name = 'requests/request_form_v2.html'
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        try:
            self.object = services.create_request(form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'Maintenance request created successfully.')
        return HttpResponseRedirect(self.get_success_url())


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRequest
    fields = ['house', 'resident', 'title', 'description', 'status', 'category']
    template_name = 'requests/request_form_v2.html'
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        try:
            self.object = services.update_request(self.get_object(), form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'Maintenance request updated successfully.')
        return HttpResponseRedirect(self.get_success_url())


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = MaintenanceRequest
    template_name = 'requests/request_confirm_delete_v2.html'
    success_url = reverse_lazy('request_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        services.delete_request(self.object)
        messages.success(request, 'Maintenance request deleted successfully.')
        return HttpResponseRedirect(self.get_success_url())


# ------------------ RESIDENT VIEWS ------------------

class ResidentListView(ListView):
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'

    def get_queryset(self):
        return services.list_residents()


class ResidentCreateView(LoginRequiredMixin, CreateView):
    model = Resident
    fields = ['first_name', 'last_name', 'email', 'phone', 'house']
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('resident_list')

    def form_valid(self, form):
        try:
            self.object = services.create_resident(form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'Resident created successfully.')
        return HttpResponseRedirect(self.get_success_url())


class ResidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Resident
    fields = ['first_name', 'last_name', 'email', 'phone', 'house']
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('resident_list')

    def form_valid(self, form):
        try:
            self.object = services.update_resident(self.get_object(), form.cleaned_data)
        except HousingValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'Resident updated successfully.')
        return HttpResponseRedirect(self.get_success_url())


class ResidentDeleteView(LoginRequiredMixin, DeleteView):
    model = Resident
    template_name = 'residents/resident_confirm_delete.html'
    success_url = reverse_lazy('resident_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            services.delete_resident(self.object)
            messages.success(request, 'Resident deleted successfully.')
        except HousingValidationError as exc:
            messages.error(request, str(exc))
        return HttpResponseRedirect(self.get_success_url())