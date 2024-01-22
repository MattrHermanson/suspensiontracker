from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.user_login, name='users-login'),
    path('account/', views.account, name='users-account'),
    path('signup/', views.signup, name='users-signup'),
    path('logout/', views.user_logout, name='users-logout'),
    path('reset/', views.reset_link, name='users-reset_link'),
    path('reset/password', views.reset_pass, name='users-reset_pass'),
    path('reset/forgot', views.forgot_pass, name='users-forgot_pass')
]