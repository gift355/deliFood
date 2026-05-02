from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
]