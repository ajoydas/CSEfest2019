from django.urls import path
from . import views

app_name = 'quiz'

# urlpatterns = [
#     path('modal/', views.modal, name='register'),
#     path('comment/', views.comment, name='comment'),
#     path('comments/', views.comments, name='comment'),
# ]


urlpatterns = [
    path('questions/<int:pk>', views.questions, name='question'),
    path('end/questions/<int:pk>', views.ended, name='ended'),
    path('questions/<int:pk>/<int:pk2>', views.questions, name='other_question'),

    path('gen_pdf/', views.gen_pdf, name='gen_pdf'),
    path('submissions/', views.submissions, name='submissions'),
    path('submission/<int:pk>', views.submission, name='submission'),

]