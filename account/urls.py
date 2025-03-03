from django.urls import path

from .import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('register', views.register, name="account.register"),

    # Email verification URL's
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name="account.email-verification"),
    path('email-verification-sent', views.email_verification_sent, name="account.email-verification-sent"),
    path('email-verification-success', views.email_verification_success, name="account.email-verification-success"),
    path('email-verification-failed', views.email_verification_failed, name="account.email-verification-failed"),

    # Login / Logout urls
    path('my-login', views.my_login, name="account.my-login"),
    path('user-logout', views.user_logout, name="account.user-logout"),

    # Dashboard / profile urls
    path('dashbaord', views.dashboard, name="account.dashboard"),
    path('profile-management', views.profile_management, name="account.profile-management"),
    path('delete-account', views.delete_account, name="account.delete-account"),

    # Password management urls/view
    # 1. Submit your email form
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/password/reset.html"), name="reset_password"),

    # 2. Success message stating that a password reset email was sent
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="account/password/reset_sent.html"), name="password_reset_done"),

    # 2. Password reset link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password/reset_form.html"), name="password_reset_confirm"),

    # 2. Success message stating that our password was reset
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="account/password/reset_complete.html"), name="password_reset_complete"),
]
