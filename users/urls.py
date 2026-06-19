from django.urls import path
from .views import signup_view, login_view, landing_view, home_view, profile_view, activate_account,password_reset_request,password_reset_confirm,password_reset_done,password_reset_complete, account_activation_notice
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('landing_view', landing_view, name='landing'),
    path('home/', home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('password_reset_request/', password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/done/',password_reset_done, name='password_reset_done'),
    path('password_reset_complete/',password_reset_complete, name='password_reset_complete'),
    path('account-activation-notice/',account_activation_notice, name='account_activation_notice'),
]
