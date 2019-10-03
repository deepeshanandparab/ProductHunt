from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name='register_page'),
    path('login/', views.logInPage, name='log_in_page'),
    path('logout/', views.logOutPage, name='log_out_page'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password-reset-done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('updateprofile/<id>/', views.updateProfilePage, name='update_profile_page')
]