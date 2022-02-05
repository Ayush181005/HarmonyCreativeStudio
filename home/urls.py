from django.urls import path
from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),

    path('signup/', views.handleSignup, name='handleSignup'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('my-account/', views.myAccount, name='myAccount'),
    path('delete-account/', views.deleteAccount, name='deleteAccount'),
    path('update-account/', views.updateAccount, name='updateAccount'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='home/account/reset_password.html'), name='reset_password'),
    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='home/account/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/account/reset_password_form.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/account/reset_password_completed.html'), name='password_reset_complete'),

    path('portfolio/<str:slug>', views.dispPortfolio, name='dispPortfolio'),
]