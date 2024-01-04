from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('setup/', views.setup, name='tracker-setup'),
    path('bikes/', views.bikes, name='tracker-bikes'),
    path('bikes/setups/', views.setups, name='tracker-setups'),
    path('bikes/setups/delete', views.delete_setup, name='tracker-delete_setup'),
    path('bikes/setups/revert', views.revert_setup, name='tracker-revert_setup'),
]