from django.urls import path, include, re_path
from . import views


app_name = 'puzzle'


urlpatterns = [
    path('puzzle/<int:pk>/', views.puzzle, name='show_puzzle'),
    path('hacker_man/', views.hacker_man, name='hacker_man'),
    path('submit_puzzle/<int:pk>/', views.submit_puzzle, name="submit_puzzle"),
    path('leader_board', views.leader_board, name="leader_board")

]
