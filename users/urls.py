from django.urls import path
from .views import signup_view, login_view, landing_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('landing_view', landing_view, name='landing'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
