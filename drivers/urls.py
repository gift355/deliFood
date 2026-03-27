from django.urls import path
from .views import register_driver, driver_dashboard

urlpatterns=[
    path('register/', register_driver, name='register_driver' ),
    path('dashboard/',driver_dashboard, name='driver_dashboard'),
]