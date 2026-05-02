from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    path('all-meals/', views.food_list, name='food_list'),
]