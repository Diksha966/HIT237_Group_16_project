from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # HOUSES
    path('houses/', views.HouseListView.as_view(), name='house_list'),
    path('houses/create/', views.HouseCreateView.as_view(), name='house_create'),
    path('houses/<int:pk>/update/', views.HouseUpdateView.as_view(), name='house_update'),
    path('houses/<int:pk>/delete/', views.HouseDeleteView.as_view(), name='house_delete'),

    # REQUESTS
    path('requests/', views.RequestListView.as_view(), name='request_list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/update/', views.RequestUpdateView.as_view(), name='request_update'),
    path('requests/<int:pk>/delete/', views.RequestDeleteView.as_view(), name='request_delete'),

    # RESIDENTS
    path('residents/', views.ResidentListView.as_view(), name='resident_list'),
    path('residents/create/', views.ResidentCreateView.as_view(), name='resident_create'),
]