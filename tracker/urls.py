from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('setup/', views.setup, name='tracker-setup'),
    path('bikes/', views.bikes, name='tracker-bikes'),
    path('bikes/delete', views.delete_bike, name='tracker-delete_bike'),
    path('bikes/setups/', views.setups, name='tracker-setups'),
    path('bikes/setups/delete', views.delete_setup, name='tracker-delete_setup'),
    path('bikes/setups/revert', views.revert_setup, name='tracker-revert_setup'),
    path('bikes/setups/duplicate', views.duplicate_setup, name='tracker-duplicate_setup'),
    path('bikes/setups/favorite', views.favorite_setup, name='tracker-favorite_setup'),
    path('bikes/setups/timeline', views.timeline, name='tracker-timeline'),
]