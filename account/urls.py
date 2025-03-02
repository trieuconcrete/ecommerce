from django.urls import path

from .import views

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

]
