from django.urls import path
from . import views

app_name = 'common'
urlpatterns = [
    path('', views.home, name='common-home'),
    path('contact/', views.contact, name='common-contact'),
    path('feedback/', views.feedback, name='common-feedback'),
]