from django.urls import path
from .views import (
    home,
    HouseListView,
    HouseCreateView,
    MaintenanceListView,
    MaintenanceCreateView,
    MaintenanceUpdateView,
    MaintenanceDeleteView,
    ResidentListView,
    ResidentCreateView,
)

urlpatterns = [
    path('', home, name='home'),

    # Houses
    path('houses/', HouseListView.as_view(), name='house_list'),
    path('houses/create/', HouseCreateView.as_view(), name='house_create'),

    # Requests
    path('requests/', MaintenanceListView.as_view(), name='request_list'),
    path('requests/create/', MaintenanceCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/update/', MaintenanceUpdateView.as_view(), name='request_update'),
    path('requests/<int:pk>/delete/', MaintenanceDeleteView.as_view(), name='request_delete'),

    # Residents
    path('residents/', ResidentListView.as_view(), name='resident_list'),
    path('residents/create/', ResidentCreateView.as_view(), name='resident_create'),
]