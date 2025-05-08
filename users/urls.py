from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view( template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='registration/password_reset_done.html' ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view( template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
