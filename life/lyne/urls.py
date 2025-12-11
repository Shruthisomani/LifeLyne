from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from lyne import views
urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("help/", views.help_view, name="help"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("matches/", views.matches, name="matches"),
    path("profile/<int:user_id>/", views.profile_full, name="profile_full"),
    
    path('edit/', views.edit_demo, name='edit_profile'),



    path('register/', views.register_page, name='register'),
    
    path('register/bride/', views.bride_registration, name='bride_registration'),

    path('register/groom/', views.groom_registration, name='groom_registration'),

    path('register/lgbtq/', views.lgbtq_registration, name='lgbtq_registration'),

    path("register/submit/", views.register_user_submit, name="register_user_submit"),

    path("register/success/", views.registration_success, name="registration_success"),

    path("login-page/", views.login_view, name="login_page"),
    # Password reset (Django built-in views with custom templates)
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
]
