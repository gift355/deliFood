from django.urls import path
from . import views

urlpatterns = [
    path('accept/<int:pk>/', views.accept_delivery, name='accept_delivery'),
    path('pickup/<int:pk>/', views.pickup_delivery, name='pickup_delivery'),
    path('complete/<int:pk>/', views.complete_delivery, name='complete_delivery'),
]