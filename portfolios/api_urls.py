from django.urls import path

from . import views

app_name = 'portfolio_api'

urlpatterns = [
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<slug:slug>/', views.profile_api_detail, name='profile_api_detail'),
    path('profiles/<slug:slug>/contact/', views.contact_api, name='contact_api'),
]
