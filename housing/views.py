from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import House, MaintenanceRequest, Resident


# HOME
def home(request):
    return render(request, 'home.html')


# ------------------ HOUSE VIEWS ------------------

class HouseListView(ListView):
    model = House
    template_name = 'houses/house_list.html'
    context_object_name = 'houses'


class HouseCreateView(CreateView):
    model = House
    fields = ['address', 'city', 'state', 'zip_code', 'rent']
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('house_list')


class HouseUpdateView(UpdateView):
    model = House
    fields = ['address', 'city', 'state', 'zip_code', 'rent']
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('house_list')


class HouseDeleteView(DeleteView):
    model = House
    template_name = 'houses/house_confirm_delete.html'
    success_url = reverse_lazy('house_list')


# ------------------ REQUEST VIEWS ------------------

class RequestListView(ListView):
    model = MaintenanceRequest
    template_name = 'requests/request_list.html'
    context_object_name = 'object_list'


class RequestCreateView(CreateView):
    model = MaintenanceRequest
    fields = ['house', 'resident', 'title', 'description', 'status', 'category']
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request_list')


class RequestUpdateView(UpdateView):
    model = MaintenanceRequest
    fields = ['house', 'resident', 'title', 'description', 'status', 'category']
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request_list')


class RequestDeleteView(DeleteView):
    model = MaintenanceRequest
    template_name = 'requests/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')


# ------------------ RESIDENT VIEWS ------------------

class ResidentListView(ListView):
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'

class ResidentCreateView(CreateView):
    model = Resident
    fields = ['first_name', 'last_name', 'email', 'phone', 'house']
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('resident_list')