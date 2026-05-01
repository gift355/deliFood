from django.urls import path
from . import views

urlpatterns = [
    path('update-status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),

]