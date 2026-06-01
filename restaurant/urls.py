from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('onboarding/', views.restaurant_onboarding, name='restaurant_onboarding'),
    path('dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
]