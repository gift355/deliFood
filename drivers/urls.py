from django.urls import path
from .views import register_driver, driver_dashboard, driver_earnings, my_deliveries

urlpatterns=[
    path('register/', register_driver, name='register_driver' ),
    path('dashboard/',driver_dashboard, name='driver_dashboard'),
    path('earnings/', driver_earnings, name='driver_earnings'),
    path('my_deliveries/', my_deliveries, name='my_deliveries')
]