from django.urls import path
from custom_auth import views
from custom_auth.views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/',views.dash_view,name='Dashboard'),
    path('login/',views.login_view,name='Login'),
    path('registration/',views.register_view,name='Registration'),
    path('logout/',views.logout_view,name='Logout'),
    path('password_change/',views.password_change_view,name='Passwordchange'),

    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='custom_auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='custom_auth/password_reset_complete.html'), name='password_reset_complete'),
] 
 