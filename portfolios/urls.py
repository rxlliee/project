from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    path('api/', views.profile_list, name='profile_list'),
    path('api/<slug:slug>/', views.profile_api_detail, name='profile_api_detail'),
    path('api/<slug:slug>/contact/', views.contact_api, name='contact_api'),
    path('<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('<slug:profile_slug>/projects/<slug:project_slug>/', views.project_detail, name='project_detail'),
]
