# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('delete_account/', views.delete_user, name='delete_user'),
    path('send/', views.send_message, name='send_message'),
    path('', views.message_list, name='message_list'),
]
