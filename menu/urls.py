from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    path('all-meals/', views.food_list, name='food_list'),
    path('restaurant/<slug:restaurant_slug>/add-food/', views.food_create, name='food_create'),
    path('food/<int:pk>/edit/', views.food_update, name='food_update'),
    path('food/<int:pk>/delete/', views.food_delete, name='food_delete'),
]