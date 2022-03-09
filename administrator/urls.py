from os import name
from django.urls import path
from .views import *

app_name = "administrator"
urlpatterns = [
    path('', posts, name="posts"),
    path('shop/<slug:slug>', detail, name="detail"),
    path('category/<slug:slug>', categry, name="category"),
]
