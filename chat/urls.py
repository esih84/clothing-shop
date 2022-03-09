from django.urls import path
from .views import *

app_name='chat'

urlpatterns = [
    path('', index, name='Chat'),
    path('<str:room_name>/', room, name='room'),
    path('edit_chat/<int:pk>/', edit_chat.as_view(), name='edit'),
]