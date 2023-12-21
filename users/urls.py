from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.user_login, name='users-login'),
    path('account/', views.account, name='users-account'),
    path('signup/', views.signup, name='users-signup'),
    path('login/error', views.user_login, name='users-login-error'),
    path('logout/', views.user_logout, name='users-logout'),
]