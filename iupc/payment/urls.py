from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.home, name='home'),
]