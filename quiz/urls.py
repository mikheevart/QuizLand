from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='quiz_index'),
    path('ajax/login/', views.ajax_login, name='ajax_login'),
    path('ajax/register/', views.ajax_register, name='ajax_register'),
    path('ajax/quiz/<int:quiz_id>/start/', views.get_quiz_card, name='get_quiz_card'),
    path('ajax/quiz/next/', views.ajax_next_question, name='ajax_next_question'),
]
