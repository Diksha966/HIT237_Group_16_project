from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import House, MaintenanceRequest, Resident


# HOME
def home(request):
    return render(request, 'home.html')


# ========================
# HOUSE VIEWS
# ========================

class HouseListView(ListView):
    model = House
    template_name = 'houses/house_list.html'


class HouseCreateView(CreateView):
    model = House
    fields = '__all__'
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('house_list')


# ========================
# MAINTENANCE REQUEST VIEWS
# ========================

class MaintenanceListView(ListView):
    model = MaintenanceRequest
    template_name = 'requests/request_list.html'


class MaintenanceCreateView(CreateView):
    model = MaintenanceRequest
    fields = '__all__'
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request_list')


class MaintenanceUpdateView(UpdateView):
    model = MaintenanceRequest
    fields = '__all__'
    template_name = 'requests/request_form.html'
    success_url = reverse_lazy('request_list')


class MaintenanceDeleteView(DeleteView):
    model = MaintenanceRequest
    template_name = 'requests/request_confirm_delete.html'
    success_url = reverse_lazy('request_list')


# ========================
# RESIDENT VIEWS
# ========================

class ResidentListView(ListView):
    model = Resident
    template_name = 'residents/resident_list.html'


class ResidentCreateView(CreateView):
    model = Resident
    fields = ['name']
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('house_list')