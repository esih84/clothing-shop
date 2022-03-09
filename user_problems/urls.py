from django.urls import path
from .views import *

urlpatterns =[
    path('problem/', problem_view, name='problem'),
    path('answer/', answer, name='answer_q'),
    path('loginapi/', api_login, name='api_login'),
    path('compelte_profile/', profile_api, name='compelte_profile')
]

1