from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

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
    path('residents/<int:pk>/update/', views.ResidentUpdateView.as_view(), name='resident_update'),
    path('residents/<int:pk>/delete/', views.ResidentDeleteView.as_view(), name='resident_delete'),
]