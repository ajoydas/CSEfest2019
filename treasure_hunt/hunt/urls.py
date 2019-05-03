from django.urls import path
from . import views

app_name = 'hunt'

urlpatterns = [
    path('hunt/', views.hunt, name='hunt'),
    # path('hunt/verify', views.hunt_verify, name='hunt_verify'),
    path('leader_board/', views.leader_board, name='leader_board'),
    path('gen_data/', views.gen_data, name='gen_data'),
]